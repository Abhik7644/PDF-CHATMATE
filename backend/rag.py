import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction


# -----------------------------
# Configuration
# -----------------------------

CHROMA_PATH = "data/chroma"


# -----------------------------
# ChromaDB Setup
# -----------------------------

chroma_client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

embedding_function = DefaultEmbeddingFunction()

collection = chroma_client.get_or_create_collection(
    name="pdf_documents",
    embedding_function=embedding_function
)


# -----------------------------
# Text Chunking
# -----------------------------

def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> list[str]:

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size"
        )

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - chunk_overlap

    return chunks


# -----------------------------
# Store Document
# -----------------------------

def add_document(
    pdf_id: str,
    chunks: list[str]
):

    ids = [
        f"{pdf_id}_{i}"
        for i in range(len(chunks))
    ]

    metadatas = [
        {
            "pdf_id": pdf_id,
            "chunk_index": i
        }
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        metadatas=metadatas
    )


# -----------------------------
# Search Documents
# -----------------------------

def search_documents(
    query: str,
    pdf_id: str,
    top_k: int = 5
):

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        where={
            "pdf_id": pdf_id
        }
    )

    return results