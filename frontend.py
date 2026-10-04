import streamlit as st
import requests


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="PDF ChatMate",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "http://127.0.0.1:8000"


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

/* Main title */
.hero-title {
    font-size: 2.8rem;
    font-weight: 700;
    margin-bottom: 0.2rem;
}

.hero-subtitle {
    color: #94a3b8;
    font-size: 1.05rem;
    margin-bottom: 2rem;
}

/* Cards */
.info-card {
    padding: 1.3rem;
    border-radius: 14px;
    border: 1px solid rgba(148, 163, 184, 0.18);
    background: rgba(30, 41, 59, 0.35);
    margin-bottom: 1rem;
}

/* Upload section */
.upload-section {
    padding: 1.5rem;
    border-radius: 16px;
    border: 1px solid rgba(148, 163, 184, 0.2);
    margin-bottom: 1.5rem;
}

/* Section headings */
.section-title {
    font-size: 1.45rem;
    font-weight: 650;
    margin-bottom: 0.3rem;
}

.section-description {
    color: #94a3b8;
    font-size: 0.9rem;
    margin-bottom: 1rem;
}

/* Summary */
.summary-card {
    padding: 1.5rem;
    border-radius: 14px;
    border: 1px solid rgba(148, 163, 184, 0.2);
    background: rgba(30, 41, 59, 0.4);
    line-height: 1.7;
}

/* Sidebar */
.sidebar-label {
    color: #94a3b8;
    font-size: 0.85rem;
}

.document-name {
    font-weight: 600;
    word-break: break-word;
}

/* Footer */
.footer {
    text-align: center;
    color: #64748b;
    font-size: 0.8rem;
    margin-top: 3rem;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "pdf_id": None,
    "filename": None,
    "summary": None,
    "chunks_created": None,
    "messages": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 📄 PDF ChatMate")

    st.caption(
        "Your AI-powered PDF assistant using RAG."
    )

    st.divider()

    if st.session_state.pdf_id:

        st.markdown("### 📑 Current Document")

        st.success("Document ready")

        st.markdown(
            f"**{st.session_state.filename}**"
        )

        if st.session_state.chunks_created:
            st.caption(
                f"🔹 {st.session_state.chunks_created} chunks indexed"
            )

        st.caption(
            f"ID: {st.session_state.pdf_id[:12]}..."
        )

        st.divider()

        if st.button(
            "🗑️ Clear Document",
            use_container_width=True
        ):

            st.session_state.pdf_id = None
            st.session_state.filename = None
            st.session_state.summary = None
            st.session_state.chunks_created = None
            st.session_state.messages = []

            st.rerun()

    else:

        st.info(
            "Upload a PDF to start chatting."
        )

    st.divider()

    st.caption(
        "FastAPI • ChromaDB • Groq • Streamlit"
    )


# =========================================================
# HERO
# =========================================================

st.markdown(
    '<div class="hero-title">📄 PDF ChatMate</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero-subtitle">
    Upload a PDF, generate an AI summary, and ask questions
    using Retrieval-Augmented Generation.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# UPLOAD SECTION
# =========================================================

st.markdown(
    '<div class="section-title">📤 Upload Document</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Upload a PDF to extract, chunk, embed and index its content.'
    '</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Choose a PDF document",
    type=["pdf"],
    label_visibility="collapsed"
)

if uploaded_file:

    st.caption(
        f"📎 {uploaded_file.name} "
        f"• {uploaded_file.size / 1024:.1f} KB"
    )

    if st.button(
        "🚀 Upload & Process PDF",
        type="primary",
        use_container_width=True
    ):

        with st.spinner(
            "Processing PDF and building the knowledge base..."
        ):

            try:

                response = requests.post(
                    f"{API_URL}/upload",
                    files={
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "application/pdf"
                        )
                    }
                )

                if response.status_code == 200:

                    data = response.json()

                    st.session_state.pdf_id = data["pdf_id"]
                    st.session_state.filename = data["filename"]
                    st.session_state.chunks_created = data["chunks_created"]

                    st.session_state.summary = None
                    st.session_state.messages = []

                    st.success(
                        "✅ PDF uploaded and indexed successfully."
                    )

                    st.rerun()

                else:

                    st.error(
                        f"Upload failed: {response.text}"
                    )

            except requests.exceptions.RequestException:

                st.error(
                    "❌ Could not connect to the FastAPI backend. "
                    "Make sure the backend is running."
                )


# =========================================================
# DOCUMENT STATUS
# =========================================================

if st.session_state.pdf_id:

    st.markdown("---")

    st.markdown(
        '<div class="section-title">📊 Document Status</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Document",
            "Ready"
        )

    with col2:
        st.metric(
            "Chunks",
            st.session_state.chunks_created
            if st.session_state.chunks_created
            else "-"
        )

    with col3:
        st.metric(
            "Chat",
            "Available"
        )


# =========================================================
# DOCUMENT TOOLS
# =========================================================

if st.session_state.pdf_id:

    st.markdown("---")

    st.markdown(
        '<div class="section-title">🛠️ Document Tools</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Generate a summary or clear the current conversation.'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    # -----------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------

    with col1:

        if st.button(
            "📝 Generate Summary",
            use_container_width=True
        ):

            if uploaded_file is None:

                st.warning(
                    "Please select the PDF again to generate its summary."
                )

            else:

                with st.spinner(
                    "Generating document summary..."
                ):

                    try:

                        response = requests.post(
                            f"{API_URL}/summarize",
                            files={
                                "file": (
                                    uploaded_file.name,
                                    uploaded_file.getvalue(),
                                    "application/pdf"
                                )
                            }
                        )

                        if response.status_code == 200:

                            st.session_state.summary = (
                                response.json()["summary"]
                            )

                            st.success(
                                "✅ Summary generated."
                            )

                        else:

                            st.error(
                                f"Summary generation failed: "
                                f"{response.text}"
                            )

                    except requests.exceptions.RequestException:

                        st.error(
                            "❌ Could not connect to the backend."
                        )

    # -----------------------------------------------------
    # RESET CHAT
    # -----------------------------------------------------

    with col2:

        if st.button(
            "🔄 Reset Chat",
            use_container_width=True
        ):

            st.session_state.messages = []

            st.rerun()


# =========================================================
# SUMMARY
# =========================================================

if st.session_state.summary:

    st.markdown("---")

    st.markdown(
        '<div class="section-title">📝 AI Summary</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'A concise summary generated from your uploaded document.'
        '</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):

        st.markdown(
            st.session_state.summary
        )


# =========================================================
# CHAT
# =========================================================

if st.session_state.pdf_id:

    st.markdown("---")

    st.markdown(
        '<div class="section-title">💬 Chat with your PDF</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Ask questions about the document. '
        'Answers are generated using retrieved document context.'
        '</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # CHAT HISTORY
    # -----------------------------------------------------

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(
                message["content"]
            )

    # -----------------------------------------------------
    # CHAT INPUT
    # -----------------------------------------------------

    question = st.chat_input(
        "Ask something about your PDF..."
    )

    if question:

        # User message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        # Assistant
        with st.chat_message("assistant"):

            with st.spinner(
                "Searching the document..."
            ):

                try:

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
                            f"Backend error: {response.text}"
                        )

                        st.error(error_message)

                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "content": error_message
                            }
                        )

                except requests.exceptions.RequestException:

                    error_message = (
                        "❌ Could not connect to the FastAPI backend."
                    )

                    st.error(error_message)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": error_message
                        }
                    )


# =========================================================
# EMPTY STATE
# =========================================================

else:

    st.markdown(
        """
        <div class="info-card" style="text-align:center;">

        <h2>👋 Welcome to PDF ChatMate</h2>

        <p style="color:#94a3b8;">
        Upload a PDF above to get started.
        </p>

        <p>
        📄 Upload &nbsp; → &nbsp;
        🔎 Retrieve &nbsp; → &nbsp;
        🤖 Ask
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
    PDF ChatMate • RAG-powered document assistant
    </div>
    """,
    unsafe_allow_html=True
)