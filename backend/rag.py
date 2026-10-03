import chromadb
from sentence_transformers import SentenceTransformer


# -----------------------------
# Configuration
# -----------------------------

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

CHROMA_PATH = "data/chroma"

from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

embedding_model = None


def get_embedding_model():
    global embedding_model

    if embedding_model is None:
        embedding_model = SentenceTransformer(
            MODEL_NAME,
            device="cpu"
        )

    return embedding_model

chroma_client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = chroma_client.get_or_create_collection(
    name="pdf_documents"
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
# Generate Embeddings
# -----------------------------

def generate_embeddings(texts: list[str]):

    embeddings = get_embedding_model().encode(
        texts,
        normalize_embeddings=True
    )

    return embeddings.tolist()


# -----------------------------
# Store Document
# -----------------------------

def add_document(
    pdf_id: str,
    chunks: list[str]
):

    embeddings = generate_embeddings(chunks)

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
        embeddings=embeddings,
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

    query_embedding = generate_embeddings([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where={
            "pdf_id": pdf_id
        }
    )

    return results