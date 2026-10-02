import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="PDF ChatMate",
    page_icon="📄",
    layout="wide"
)


st.title("📄 PDF ChatMate")
st.write("Upload a PDF and ask questions about it.")


# --------------------------------
# Session State
# --------------------------------

if "pdf_id" not in st.session_state:
    st.session_state.pdf_id = None

if "filename" not in st.session_state:
    st.session_state.filename = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------
# PDF Upload
# --------------------------------

st.header("Upload PDF")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)


if uploaded_file is not None:

    if st.button("Upload PDF"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf"
            )
        }

        with st.spinner("Processing PDF..."):

            response = requests.post(
                f"{API_URL}/upload",
                files=files
            )

        if response.status_code == 200:

            data = response.json()

            st.session_state.pdf_id = data["pdf_id"]
            st.session_state.filename = data["filename"]
            st.session_state.messages = []

            st.success(
                f"PDF uploaded successfully! "
                f"{data['chunks_created']} chunks created."
            )

        else:

            st.error(
                f"Upload failed: {response.text}"
            )


# --------------------------------
# Uploaded PDF Information
# --------------------------------

if st.session_state.pdf_id:

    st.divider()

    st.subheader("Current Document")

    st.info(
        f"📄 {st.session_state.filename}"
    )


# --------------------------------
# Chat
# --------------------------------

if st.session_state.pdf_id:

    st.header("Chat with your PDF")

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    question = st.chat_input(
        "Ask something about your PDF..."
    )


    if question:

        # Display user question
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)


        # Ask backend
        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                response = requests.post(
                    f"{API_URL}/chat",
                    json={
                        "pdf_id": st.session_state.pdf_id,
                        "question": question
                    }
                )


            if response.status_code == 200:

                data = response.json()

                answer = data["answer"]

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            else:

                error_message = (
                    f"Error: {response.text}"
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message
                    }
                )