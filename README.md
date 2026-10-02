# 📄 PDF ChatMate

### 🤖 Chat with your PDFs using RAG + LLMs

<p align="center">
  <b>Upload a PDF → Index it → Ask questions → Get context-aware answers</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?logo=python" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi" />
  <img src="https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?logo=streamlit" />
  <img src="https://img.shields.io/badge/RAG-ChromaDB-purple" />
  <img src="https://img.shields.io/badge/LLM-Groq-orange" />
  <img src="https://img.shields.io/badge/Testing-Pytest-green?logo=pytest" />
  <img src="https://img.shields.io/badge/Automation-Selenium-43B02A?logo=selenium" />
</p>

---

## 🌟 Overview

**PDF ChatMate** is a full-stack AI application that allows users to upload PDF documents, generate summaries, and ask natural-language questions about their documents.

Instead of sending an entire PDF to an LLM for every question, the application uses a **Retrieval-Augmented Generation (RAG)** pipeline.

The system:

```text
📄 PDF
   ↓
🔍 Text Extraction
   ↓
✂️ Chunking
   ↓
🧠 Embeddings
   ↓
🗄️ ChromaDB
   ↓
🔎 Semantic Retrieval
   ↓
🤖 Groq LLM
   ↓
💬 Answer


                         ┌─────────────────────┐
                         │        👤 User      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    🖥️ Streamlit     │
                         │      Frontend       │
                         └──────────┬──────────┘
                                    │
                                  HTTP
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      ⚡ FastAPI      │
                         │       Backend       │
                         └──────────┬──────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
       ┌─────────────┐       ┌─────────────┐       ┌─────────────┐
       │  📄 PyMuPDF │       │  🔎 RAG     │       │ 🤖 Groq LLM │
       │ PDF Extract │       │  Pipeline   │       │             │
       └─────────────┘       └──────┬──────┘       └─────────────┘
                                    │
                         ┌──────────┴──────────┐
                         │                     │
                         ▼                     ▼
                  ┌──────────────┐     ┌──────────────┐
                  │ 🧠 Sentence  │     │ 🗄️ ChromaDB  │
                  │ Transformers │     │ Vector Store │
                  └──────────────┘     └──────────────┘


🛠️ Tech Stack
Backend
🐍 Python
⚡ FastAPI
🚀 Uvicorn
📄 PyMuPDF
RAG
🧠 Sentence Transformers
🔢 all-MiniLM-L6-v2
🗄️ ChromaDB
🔎 Semantic similarity search
LLM
🤖 Groq
openai/gpt-oss-120b
Frontend
🎨 Streamlit
Testing
🧪 Pytest
🌐 Selenium
FastAPI TestClient
Configuration
🔐 python-dotenv
.env


                   🧪 Testing
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
       Unit Tests    API Tests    RAG Tests
          │            │            │
          └────────────┼────────────┘
                       │
                       ▼
                🌐 Selenium E2E


## ⚙️ Setup

1. Clone the repository and navigate to the project directory.
2. Create and activate a Python virtual environment.
3. Install dependencies using `pip install -r requirements.txt`.
4. Create a `.env` file and add your `GROQ_API_KEY`.
5. Start the FastAPI backend with `python -m uvicorn backend.main:app --reload` and the Streamlit frontend with `streamlit run frontend.py`.