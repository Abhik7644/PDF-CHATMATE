import os
import psutil

from pydantic import BaseModel
from backend.rag import (
  search_documents,
  add_document,
  chunk_text
)
from backend.llm import (
  answer_question,
  summarize_text,
)
from uuid import uuid4
from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
from backend.pdf_processor import extract_text_from_pdf

process = psutil.Process(os.getpid())

def log_memory(label):
    memory_mb = process.memory_info().rss / (1024 * 1024)
    print(f"[MEMORY] {label}: {memory_mb:.2f} MB")

    

app = FastAPI(title="PDF ChatMate")

log_memory("Backend startup")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

class ChatRequest(BaseModel):
    pdf_id: str
    question: str


@app.get("/")
def home():
    return {"message": "PDF ChatMate API is running"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    log_memory("Upload - start")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    pdf_id = str(uuid4())

    file_path = UPLOAD_DIR / f"{pdf_id}_{file.filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())


    # Extract text
    text = extract_text_from_pdf(str(file_path))

    log_memory("Upload - after PDF extraction")

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from PDF"
        )

    # Create chunks
    chunks = chunk_text(text)

    log_memory("Upload - after chunking")

    # Store chunks and embeddings
    add_document(
        pdf_id=pdf_id,
        chunks=chunks
    )
    log_memory("Upload - after RAG indexing")

    return {
        "pdf_id": pdf_id,
        "filename": file.filename,
        "chunks_created": len(chunks)
    }

@app.post("/summarize")
async def summarize_pdf(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    text = extract_text_from_pdf(str(file_path))

    log_memory("Summarize - after PDF extraction")

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from PDF"
        )

    summary = summarize_text(text)

    log_memory("Summarize - after Groq response")

    return {
        "filename": file.filename,
        "summary": summary
    }

@app.post("/chat")
async def chat(request: ChatRequest):

    # Retrieve relevant chunks
    results = search_documents(
        query=request.question,
        pdf_id=request.pdf_id,
        top_k=5
    )

    log_memory("Chat - after RAG retrieval")
    

    documents = results["documents"][0]

    if not documents:
        raise HTTPException(
            status_code=404,
            detail="No relevant information found in the document"
        )

    # Combine retrieved chunks
    context = "\n\n".join(documents)

    # Generate answer using LLM
    answer = answer_question(
        question=request.question,
        context=context
    )
    log_memory("Chat - after Groq response")

    return {
        "pdf_id": request.pdf_id,
        "question": request.question,
        "answer": answer,
        "sources": documents
    }