import uuid
import chromadb

import backend.rag as rag
from backend.rag import chunk_text, add_document, search_documents

def fake_embeddings(texts, input_type):
    embeddings = []

    for text in texts:
        vector = [0.0] * 1024

        text_lower = text.lower()

        if "selenium" in text_lower or "browser automation" in text_lower:
            vector[0] = 1.0

        if "docker" in text_lower or "containerization" in text_lower:
            vector[1] = 1.0

        if "python" in text_lower or "backend" in text_lower:
            vector[2] = 1.0

        if "chromadb" in text_lower or "vector database" in text_lower:
            vector[3] = 1.0

        embeddings.append(vector)

    return embeddings


def test_chunk_text():
    text = "A" * 2500

    chunks = chunk_text(
        text,
        chunk_size=1000,
        chunk_overlap=200
    )

    assert len(chunks) > 1

    for chunk in chunks:
        assert len(chunk) <= 1000


def test_invalid_chunk_overlap():
    import pytest

    with pytest.raises(ValueError):
        chunk_text(
            "some text",
            chunk_size=100,
            chunk_overlap=100
        )


def test_retrieval_returns_relevant_chunk(monkeypatch):
    # Create temporary in-memory ChromaDB
    client = chromadb.Client()

    collection = client.get_or_create_collection(
        name=f"test_{uuid.uuid4().hex}"
    )

    # Replace production collection with test collection
    monkeypatch.setattr(rag, "collection", collection)

    chunks = [
        "Python is used for backend development.",
        "Selenium is used for browser automation.",
        "ChromaDB is used as a vector database."
    ]
    monkeypatch.setattr(
        rag,
        "generate_embeddings",
        fake_embeddings
    )

    add_document(
        pdf_id="test-doc",
        chunks=chunks
    )

    results = search_documents(
        query="What is used for browser automation?",
        pdf_id="test-doc",
        top_k=1
    )

    retrieved_documents = results["documents"][0]

    assert len(retrieved_documents) == 1
    assert "Selenium" in retrieved_documents[0]


def test_retrieval_filters_by_pdf_id(monkeypatch):
    # Create temporary in-memory ChromaDB
    client = chromadb.Client()

    collection = client.get_or_create_collection(
        name=f"test_{uuid.uuid4().hex}"
    )

    monkeypatch.setattr(rag, "collection", collection)
    monkeypatch.setattr(
        rag,
        "generate_embeddings",
        fake_embeddings
    )

    add_document(
        pdf_id="pdf-1",
        chunks=[
            "Selenium is used for browser automation."
        ]
    )

    add_document(
        pdf_id="pdf-2",
        chunks=[
            "Docker is used for containerization."
        ]
    )

    results = search_documents(
        query="What is used for containerization?",
        pdf_id="pdf-2",
        top_k=1
    )

    retrieved_documents = results["documents"][0]
    retrieved_metadata = results["metadatas"][0]

    assert len(retrieved_documents) == 1
    assert "Docker" in retrieved_documents[0]
    assert retrieved_metadata[0]["pdf_id"] == "pdf-2"