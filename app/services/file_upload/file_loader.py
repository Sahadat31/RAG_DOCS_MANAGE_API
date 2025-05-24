from langchain_community.document_loaders.word_document import UnstructuredWordDocumentLoader
from langchain_community.document_loaders.text import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import tempfile

def load_and_chunk_documents(filename, content_bytes):
    ext = filename.lower().split(".")[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
        tmp.write(content_bytes)
        tmp.flush()
        path = tmp.name

    if ext == "pdf":
        loader = PyPDFLoader(path)
    elif ext in ["doc", "docx"]:
        loader = UnstructuredWordDocumentLoader(path)
    elif ext == "txt":
        loader = TextLoader(path)
    else:
        os.remove(path)
        raise ValueError(f"Unsupported file type: {ext}")

    docs = loader.load()
    os.remove(path)

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(docs)
