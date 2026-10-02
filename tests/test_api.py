from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_upload_rejects_non_pdf():

    files = {
        "file": (
            "test.txt",
            b"This is not a PDF",
            "text/plain"
        )
    }

    response = client.post(
        "/upload",
        files=files
    )

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "Only PDF files are allowed"
    )

def test_upload_pdf(monkeypatch):

    monkeypatch.setattr(
        "backend.main.extract_text_from_pdf",
        lambda file_path: "This is test PDF content."
    )

    monkeypatch.setattr(
        "backend.main.chunk_text",
        lambda text: [
            "This is chunk one.",
            "This is chunk two."
        ]
    )

    monkeypatch.setattr(
        "backend.main.add_document",
        lambda pdf_id, chunks: None
    )

    files = {
        "file": (
            "test.pdf",
            b"fake pdf content",
            "application/pdf"
        )
    }

    response = client.post(
        "/upload",
        files=files
    )

    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == "test.pdf"
    assert data["chunks_created"] == 2
    assert "pdf_id" in data

def test_summarize_pdf(monkeypatch):

    monkeypatch.setattr(
        "backend.main.extract_text_from_pdf",
        lambda file_path: "This is document content."
    )

    monkeypatch.setattr(
        "backend.main.summarize_text",
        lambda text: "This is the summary."
    )

    files = {
        "file": (
            "test.pdf",
            b"fake pdf content",
            "application/pdf"
        )
    }

    response = client.post(
        "/summarize",
        files=files
    )

    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == "test.pdf"
    assert data["summary"] == "This is the summary."

def test_chat(monkeypatch):

    monkeypatch.setattr(
        "backend.main.search_documents",
        lambda query, pdf_id, top_k: {
            "documents": [
                [
                    "Python is required.",
                    "Linux knowledge is preferred."
                ]
            ]
        }
    )

    monkeypatch.setattr(
        "backend.main.answer_question",
        lambda question, context: (
            "Python and Linux knowledge are required."
        )
    )

    response = client.post(
        "/chat",
        json={
            "pdf_id": "test-pdf-123",
            "question": "What skills are required?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["pdf_id"] == "test-pdf-123"

    assert data["question"] == (
        "What skills are required?"
    )

    assert data["answer"] == (
        "Python and Linux knowledge are required."
    )

    assert len(data["sources"]) == 2