
import sys
from importlib import import_module
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))
load_uploaded_files = import_module("document_loader").load_uploaded_files

st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🤖"
)

st.title("Multi-Agent Research System")

uploaded_files = st.file_uploader(
    "Upload PDF, TXT or MD files",
    type=["pdf", "txt", "md"],
    accept_multiple_files=True
)

if uploaded_files:
    try:
        documents = load_uploaded_files(uploaded_files)

        st.success(
            f"Successfully loaded {len(documents)} document pages."
        )

        for doc in documents:
            st.write(doc.metadata)
            st.write(doc.page_content[:500])

    except Exception as e:
        st.error(str(e))
