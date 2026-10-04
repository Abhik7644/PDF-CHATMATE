import os

import chromadb
import cohere
from dotenv import load_dotenv

load_dotenv()


CHROMA_PATH = "data/chroma"

chroma_client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = chroma_client.get_or_create_collection(
    name="pdf_documents_cohere",
    configuration={
        "hnsw": {
            "space": "cosine"
        }
    }
)


cohere_client = None


def get_cohere_client():
    global cohere_client

    if cohere_client is None:
        api_key = os.getenv("COHERE_API_KEY")

        if not api_key:
            raise RuntimeError(
                "COHERE_API_KEY is not configured."
            )

        cohere_client = cohere.ClientV2(
            api_key=api_key
        )

    return cohere_client

EMBEDDING_MODEL = "embed-v4.0"
EMBEDDING_DIMENSION = 1024
BATCH_SIZE = 96


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


def generate_embeddings(
    texts: list[str],
    input_type: str
) -> list[list[float]]:

    embeddings = []

    client = get_cohere_client()

    for i in range(0, len(texts), BATCH_SIZE):

        batch = texts[i:i + BATCH_SIZE]

        

        response = client.embed(
            model=EMBEDDING_MODEL,
            texts=batch,
            input_type=input_type,
            output_dimension=EMBEDDING_DIMENSION,
            embedding_types=["float"]
        )

        embeddings.extend(response.embeddings.float)

    return embeddings


def add_document(
    pdf_id: str,
    chunks: list[str]
):

    embeddings = generate_embeddings(
        chunks,
        input_type="search_document"
    )

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


def search_documents(
    query: str,
    pdf_id: str,
    top_k: int = 5
):

    query_embedding = generate_embeddings(
        [query],
        input_type="search_query"
    )[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where={
            "pdf_id": pdf_id
        }
    )

    return results