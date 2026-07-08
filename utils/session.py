import streamlit as st


DEFAULT_SESSION = {
    "parsed": False,
    "response": None,
    "markdown": "",
    "chunks": [],
    "extract_result": None,
    "selected_chunk": 0,
    "document_path": None,
    "fields": [
        {
            "name": "",
            "description": "",
        }
    ],
}


def initialize_session():

    for key, value in DEFAULT_SESSION.items():

        if key not in st.session_state:
            st.session_state[key] = value


def reset_document():

    st.session_state.parsed = False
    st.session_state.response = None
    st.session_state.markdown = ""
    st.session_state.chunks = []
    st.session_state.extract_result = None
    st.session_state.selected_chunk = 0
    st.session_state.document_path = None