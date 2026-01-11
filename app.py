import streamlit as st
from loaders.document_loader import load_documents
from rag.vectorstore import build_vectorstore

st.set_page_config(page_title="Scientific RAG App", layout="wide")

st.title("Scientific Document Q&A (Local, Free, RAG)")

uploaded_files = st.file_uploader(
    "Upload scientific documents (PDF, DOCX, TXT)",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

if uploaded_files:
    with st.spinner("Loading documents..."):
        documents = load_documents(uploaded_files)

    st.success(f"Loaded {len(documents)} document pages.")

    with st.spinner("Building vector database (FAISS)..."):
        vectorstore, n_chunks = build_vectorstore(documents)

    st.success(f"Created vector store with {n_chunks} chunks.")

    with st.expander("Preview extracted text"):
        for i, doc in enumerate(documents[:3]):
            st.markdown(f"**Document page {i+1}:**")
            st.write(doc.page_content[:800])
