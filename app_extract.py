import os
from pathlib import Path
import json

import streamlit as st
from dotenv import load_dotenv

from services.extractor import ExtractorService
from services.parser import ParserService
from services.visualizer import Visualizer

from utils.file import (
    ensure_directory,
    get_file_size_kb,
    save_uploaded_file,
)

from utils.session import (
    initialize_session,
    reset_document,
)

# ==========================================================
# Configuration
# ==========================================================

load_dotenv()

API_KEY = os.getenv("LANDINGAI_API_KEY")

if not API_KEY:
    st.error("LANDINGAI_API_KEY is missing in .env")
    st.stop()

UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("output")

ensure_directory(UPLOAD_DIR)
ensure_directory(OUTPUT_DIR)

parser = ParserService(API_KEY)
extractor = ExtractorService(API_KEY)

initialize_session()

# ==========================================================
# Page Config
# ==========================================================

st.set_page_config(
    page_title="LandingAI Document Extractor",
    page_icon="⚜️",
    layout="wide",
)

st.title("⚜️ LandingAI Document Extractor ⚜️")

st.caption(
    "Parse documents with LandingAI and extract structured information."
)

# ==========================================================
# Sidebar
# ==========================================================

with st.sidebar:

    st.header("Document")

    uploaded_file = st.file_uploader(
        "Upload",
        type=[
            "pdf",
            "png",
            "jpg",
            "jpeg",
            "bmp",
            "tiff",
        ],
    )

    st.divider()

    if st.button(
        "Reset Session",
        use_container_width=True,
    ):
        reset_document()
        st.rerun()

# ==========================================================
# Upload
# ==========================================================

if uploaded_file is not None:

    file_path = save_uploaded_file(
        uploaded_file,
        UPLOAD_DIR,
    )

    st.session_state.document_path = file_path

# ==========================================================
# Parse
# ==========================================================

if (
    uploaded_file is not None
    and not st.session_state.parsed
):

    if st.button(
        "🚀 Parse Document",
        type="primary",
        use_container_width=True,
    ):

        with st.spinner("Parsing document..."):

            result = parser.parse(
                document_path=file_path,
                output_dir=OUTPUT_DIR,
            )

        st.session_state.response = result["response"]
        st.session_state.markdown = result["markdown"]
        st.session_state.chunks = result["chunks"]
        st.session_state.parsed = True

        st.success("Document parsed successfully.")

# ==========================================================
# Preview
# ==========================================================

if uploaded_file is not None:

    left, right = st.columns(
        [1, 2]
    )

    with left:

        st.subheader("Uploaded Document")

        if uploaded_file.type.startswith("image"):

            st.image(
                uploaded_file,
                use_container_width=True,
            )

        else:

            st.info(uploaded_file.name)

        st.write(
            f"**Filename:** {uploaded_file.name}"
        )

        st.write(
            f"**Size:** {get_file_size_kb(file_path)} KB"
        )

    with right:

        if st.session_state.parsed:

            st.success(
                "OCR parsing completed."
            )

        else:

            st.info(
                "Click 'Parse Document' to begin."
            )


# ==========================================================
# OCR Result Viewer
# ==========================================================

if st.session_state.parsed:

    chunks = st.session_state.chunks
    markdown = st.session_state.markdown

    left, right = st.columns([1.2, 1.8])

    # ------------------------------------------------------
    # Left Panel
    # ------------------------------------------------------

    with left:

        st.subheader("Document Viewer")

        if len(chunks):

            selected_chunk = st.selectbox(
                "Chunk",
                range(len(chunks)),
                index=st.session_state.selected_chunk,
                format_func=lambda i: f"{i+1}. {chunks[i].type}",
            )

            st.session_state.selected_chunk = selected_chunk

            image = Visualizer.draw_chunk_box(
                st.session_state.document_path,
                chunks[selected_chunk],
            )

            st.image(
                image,
                use_container_width=True,
            )

            chunk = chunks[selected_chunk]

            st.caption(
                f"Page {chunk.grounding.page + 1}"
            )

            st.write("### Chunk Type")

            st.code(chunk.type)

        else:

            st.warning("No OCR chunks found.")

    # ------------------------------------------------------
    # Right Panel
    # ------------------------------------------------------

    with right:

        markdown_tab, chunk_tab, extract_tab = st.tabs(
            [
                "Markdown",
                "Chunks",
                "Extraction",
            ]
        )

        # --------------------------------------------------
        # Markdown
        # --------------------------------------------------

        with markdown_tab:

            st.markdown(markdown)

        # --------------------------------------------------
        # Chunks
        # --------------------------------------------------

        with chunk_tab:

            st.write(
                f"Total Chunks: {len(chunks)}"
            )

            for idx, chunk in enumerate(chunks):

                with st.expander(
                    f"Chunk {idx+1} ({chunk.type})"
                ):

                    st.markdown(chunk.markdown)

                    if st.button(
                        "View Bounding Box",
                        key=f"view_{idx}",
                    ):

                        st.session_state.selected_chunk = idx

                        st.rerun()

        # --------------------------------------------------
        # Extraction
        # --------------------------------------------------

        with extract_tab:

            st.subheader(
                "Extraction Configuration"
            )

            extraction_summary = st.text_area(
                "Summary / Instructions",
                placeholder="""
Example:

Extract all requested fields.

Return null if unavailable.

Do not infer information.
Only use the document.
""",
                height=150,
            )

            st.divider()

            st.write("### Fields")

            remove_index = None

            for idx, field in enumerate(
                st.session_state.fields
            ):

                col1, col2, col3 = st.columns(
                    [2, 5, 1]
                )

                with col1:

                    field["name"] = st.text_input(
                        "Field Name",
                        value=field["name"],
                        key=f"name_{idx}",
                    )

                with col2:

                    field["description"] = st.text_input(
                        "Description",
                        value=field["description"],
                        key=f"description_{idx}",
                    )

                with col3:

                    st.write("")

                    if st.button(
                        "🗑️",
                        key=f"delete_{idx}",
                    ):

                        remove_index = idx

            if remove_index is not None:

                st.session_state.fields.pop(
                    remove_index
                )

                st.rerun()

            left_btn, right_btn = st.columns(2)

            with left_btn:

                if st.button(
                    "➕ Add Field",
                    use_container_width=True,
                ):

                    st.session_state.fields.append(
                        {
                            "name": "",
                            "description": "",
                        }
                    )

                    st.rerun()

            with right_btn:

                run_extract = st.button(
                    "✨ Extract",
                    type="primary",
                    use_container_width=True,
                )



# ==========================================================
# Run Extraction
# ==========================================================

if (
    st.session_state.parsed
    and "run_extract" in locals()
    and run_extract
):

    valid_fields = []

    for field in st.session_state.fields:

        if field["name"].strip():

            valid_fields.append(field)

    if len(valid_fields) == 0:

        st.warning(
            "Please add at least one extraction field."
        )

        st.stop()

    with st.spinner(
        "Extracting structured information..."
    ):

        try:

            result = extractor.extract(
                markdown=st.session_state.markdown,
                fields=valid_fields,
                instructions=extraction_summary,
                output_dir=OUTPUT_DIR,
            )

            st.session_state.extract_result = result

        except Exception as e:

            st.exception(e)

            st.stop()

# ==========================================================
# Extraction Result
# ==========================================================

if st.session_state.extract_result is not None:

    st.divider()
    st.header("Extraction Result")

    result = st.session_state.extract_result

    tab1, tab2, tab3 = st.tabs(
        [
            "Extraction",
            "References",
            "Metadata",
        ]
    )

    with tab1:

        extraction = result.extraction

        st.json(extraction)

        st.download_button(
            "📥 Download JSON",
            data=json.dumps(
                extraction,
                indent=2,
                default=str,
            ),
            file_name="extraction.json",
            mime="application/json",
        )

    with tab2:

        st.json(result.extraction_metadata)

    with tab3:

        st.json(result.metadata)
