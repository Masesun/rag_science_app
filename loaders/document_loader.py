from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader
)
import tempfile
import os


def load_documents(uploaded_files):
    documents = []

    for uploaded_file in uploaded_files:
        suffix = os.path.splitext(uploaded_file.name)[1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        try:
            if suffix == ".pdf":
                loader = PyPDFLoader(tmp_path)
            elif suffix == ".txt":
                loader = TextLoader(tmp_path, encoding="utf-8")
            elif suffix == ".docx":
                loader = Docx2txtLoader(tmp_path)
            else:
                continue

            documents.extend(loader.load())

        finally:
            os.remove(tmp_path)

    return documents
