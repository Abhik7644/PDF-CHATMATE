import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def get_groq_client():
    return Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )



def summarize_text(text: str) -> str:
    client = get_groq_client()

    # Keep the request safely below Groq's token limit.
    # Approx. 4 characters ≈ 1 token.
    max_chars = 18000
    text = text[:max_chars]

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a document summarization assistant. "
                    "Summarize the provided document clearly and concisely. "
                    "Focus on the main topics, key concepts, and important details."
                )
            },
            {
                "role": "user",
                "content": f"Summarize this document:\n\n{text}"
            }
        ]
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