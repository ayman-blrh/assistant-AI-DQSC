import os, shutil, hashlib
from langchain_community.document_loaders import (
    PyPDFLoader, UnstructuredFileLoader, DirectoryLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from fastapi import UploadFile , File
from datetime import datetime

UPLOAD_DIR = "data2"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def upload_file(file: UploadFile = File(...)):
    
    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"{ts}_{file.filename}"
    save_path = os.path.join(UPLOAD_DIR, filename)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ingest_document(save_path)

def _hash_id(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def load_any(path: str):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        # ⚠️ pour les PDF scannés, remplacer par Unstructured + OCR si besoin
        try:
            return PyPDFLoader(path).load()
        except Exception:
            return UnstructuredFileLoader(path, mode="elements").load()
    else:
        return UnstructuredFileLoader(path, mode="elements").load()

def ingest_document(path: str, collection_name: str = "vector_db"):
    docs = load_any(path)
    ingest_DATA(docs, collection_name=collection_name, source_path=path)

def ingest_folder(folder: str, collection_name: str = "vector_db"):
    loader = DirectoryLoader(folder, glob=["**/*.txt", "**/*.pdf", "**/*.docx", "**/*.pptx"])
    docs = loader.load()
    ingest_DATA(docs, collection_name=collection_name)

def create_collection_if_not_exists(client: QdrantClient, name: str, vector_size: int = 768):
    if name not in [c.name for c in client.get_collections().collections]:
        client.create_collection(name, vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE))

def ingest_DATA(docs, collection_name: str = "vector_db", source_path: str | None = None):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(docs)

    # Ajout d’une source lisible
    for d in chunks:
        d.metadata = d.metadata or {}
        d.metadata.setdefault("source", d.metadata.get("source") or source_path or "unknown")

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    client = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"), prefer_grpc=False)
    create_collection_if_not_exists(client, collection_name, vector_size=768)

    vs = Qdrant(client=client, embeddings=embeddings, collection_name=collection_name)

    # IDs stables pour éviter les doublons à la réingestion
    ids = []
    for i, d in enumerate(chunks):
        base = f"{d.metadata.get('source','unknown')}|{i}|{d.page_content[:64]}"
        ids.append(_hash_id(base))

    vs.add_documents(chunks, ids=ids)
    print(f"Ingestion OK: {len(chunks)} chunks → {collection_name}")
