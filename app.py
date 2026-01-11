import streamlit as st
from loaders.document_loader import load_documents
from rag.vectorstore import build_vectorstore
from qa.rag_qa import answer_question

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

    st.success(f"Vector store ready ({n_chunks} chunks).")

    st.divider()

    question = st.text_input(
        "Ask a question based on the uploaded documents",
        placeholder="e.g. What mechanism of action is proposed by the authors?"
    )

    if question:
        with st.spinner("Searching documents and generating answer..."):
            answer, sources = answer_question(vectorstore, question)

        st.subheader("Answer (with inline citations)")
        st.markdown(answer)


        with st.expander("Retrieved source fragments"):
            for i, doc in enumerate(sources):
                st.markdown(f"**Source {i+1}**")
                st.write(doc.page_content[:1000])
