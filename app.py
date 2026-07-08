from PIL import Image, ImageDraw
from pdf2image import convert_from_path

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from landingai_ade import LandingAIADE

# ----------------------------------------------------
# Configuration
# ----------------------------------------------------

load_dotenv()

API_KEY = os.getenv("LANDINGAI_API_KEY")

if not API_KEY:
    st.error("LANDINGAI_API_KEY not found in .env")
    st.stop()

client = LandingAIADE(apikey=API_KEY)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

st.set_page_config(
    page_title="LandingAI OCR",
    page_icon="📄",
    layout="wide"
)


# ----------------------------------------------------
# Helper Function
# ----------------------------------------------------

def draw_chunk_box(file_path, chunk):
    """
    Draw the bounding box for one LandingAI chunk.
    Supports images and PDFs.
    """

    ext = file_path.suffix.lower()

    # Convert PDF page to image
    if ext == ".pdf":
        image = convert_from_path(
            file_path,
            first_page=chunk.grounding.page + 1,
            last_page=chunk.grounding.page + 1
        )[0]

    else:
        image = Image.open(file_path).convert("RGB")

    draw = ImageDraw.Draw(image)

    w, h = image.size

    box = chunk.grounding.box

    x1 = box.left * w
    y1 = box.top * h
    x2 = box.right * w
    y2 = box.bottom * h

    draw.rectangle(
        [x1, y1, x2, y2],
        outline="red",
        width=5
    )

    return image


# ----------------------------------------------------
# Title
# ----------------------------------------------------

st.title("⚜️ LandingAI ADE OCR")
st.caption("Upload a PDF or image and extract OCR using LandingAI.")

# ----------------------------------------------------
# Upload
# ----------------------------------------------------

uploaded_file = st.file_uploader(
    "Choose a document",
    type=[
        "pdf",
        "png",
        "jpg",
        "jpeg",
        "tiff",
        "bmp"
    ]
)

if uploaded_file is not None:

    file_path = UPLOAD_DIR / uploaded_file.name

    # Save uploaded file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    left, right = st.columns([1, 2])

    with left:

        st.subheader("Preview")

        if uploaded_file.type.startswith("image"):
            st.image(uploaded_file, use_container_width=True)
        else:
            st.info("PDF uploaded")

        st.write("**Filename:**", uploaded_file.name)
        st.write("**Saved to:**", file_path)
        st.write("**Size:**", f"{file_path.stat().st_size / 1024:.2f} KB")

    with right:

        if st.button("🚀 Run OCR", use_container_width=True):

            with st.spinner("Running LandingAI OCR..."):

                try:

                    response = client.parse(
                        document=file_path,
                        model="dpt-2-latest",
                        save_to=OUTPUT_DIR
                    )

                    st.success("OCR completed successfully!")

                except Exception as e:

                    st.exception(e)
                    st.stop()

            # ------------------------------------------------
            # Tabs
            # ------------------------------------------------

            tab1, tab2, tab3 = st.tabs(
                [
                    "Markdown",
                    "Chunks",
                    "Raw Response"
                ]
            )

            # --------------------------------------------
            # Markdown
            # --------------------------------------------

            with tab1:

                markdown = ""

                if hasattr(response, "markdown"):
                    markdown = response.markdown

                elif hasattr(response, "chunks"):
                    markdown = "\n\n".join(
                        chunk.text for chunk in response.chunks
                    )

                if markdown:

                    st.markdown(markdown)

                    st.download_button(
                        "Download Markdown",
                        markdown,
                        file_name="ocr.md",
                        mime="text/markdown"
                    )

                else:

                    st.warning("No markdown returned.")

            # --------------------------------------------
            # Chunks
            # --------------------------------------------
            with tab2:

                if hasattr(response, "chunks"):

                    st.write(f"Total Chunks: {len(response.chunks)}")

                    for i, chunk in enumerate(response.chunks):

                        with st.expander(f"Chunk {i+1} ({chunk.type})"):

                            st.markdown(chunk.markdown)

                            image = draw_chunk_box(
                                file_path,
                                chunk
                            )

                            st.image(
                                image,
                                use_container_width=True
                            )

                else:

                    st.warning("No chunks found.")

            # --------------------------------------------
            # Raw Response
            # --------------------------------------------

            with tab3:

                st.write(response)

                if hasattr(response, "__dict__"):
                    st.json(response.__dict__)