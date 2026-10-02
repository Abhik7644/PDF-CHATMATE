import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def get_groq_client():
    return Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )



def summarize_text(text: str) -> str:

    prompt = f"""
You are a document summarization assistant.

Summarize the following PDF content clearly and concisely.

Focus on:
- Main topic
- Important points
- Key findings
- Important conclusions

Do not invent information that is not present in the document.

PDF CONTENT:
{text}
"""
    client=get_groq_client()
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

def answer_question(question: str, context: str) -> str:

    prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the provided document context.

Rules:
- Do not use outside knowledge.
- Do not invent information.
- If the answer is not present in the context, say:
  "The answer is not available in the document."
- Give a clear and concise answer.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}
"""
    client=get_groq_client()
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content