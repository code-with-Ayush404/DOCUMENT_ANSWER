import streamlit as st
from dotenv import load_dotenv

from pdf_qa_backend import (
    create_vector_store,
    load_website,
    load_uploaded_file,
    answer_question
)

load_dotenv()

st.set_page_config(page_title="DocuMind AI", page_icon="🧠", layout="wide")

st.markdown("""
<style>
/* ---------- Force dark theme everywhere ---------- */
:root, .stApp {
    color-scheme: dark only;
}

#MainMenu, footer, header {visibility: hidden;}

:root {
    --bg: #080b14;
    --panel: #111827;
    --panel-soft: #0f172a;
    --border: #243044;
    --text: #f8fafc;
    --muted: #94a3b8;
    --accent: #8b5cf6;
    --accent-2: #06b6d4;
}

html, body, .stApp, [data-testid="stAppViewContainer"] {
    background-color: #020617;
    color: var(--text);
}

.stApp {
    background:
        radial-gradient(circle at 20% 0%, rgba(139,92,246,.20), transparent 32%),
        radial-gradient(circle at 90% 10%, rgba(6,182,212,.15), transparent 30%),
        linear-gradient(180deg, #080b14, #020617);
    color: var(--text);
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 980px;
    padding-top: 32px;
    padding-bottom: 120px;
}

/* Base text colors so nothing inherits a light default */
.stApp, .stApp p, .stApp span, .stApp label, .stApp li,
.stMarkdown, [data-testid="stMarkdownContainer"] {
    color: var(--text);
}

[data-testid="stSidebar"] {
    background: rgba(2, 6, 23, .96);
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] * {
    color: #dbeafe;
}

.brand-card {
    padding: 16px 14px;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(139,92,246,.20), rgba(6,182,212,.10));
    border: 1px solid rgba(148,163,184,.22);
    margin-bottom: 18px;
}

.brand-title {
    font-size: 24px;
    font-weight: 900;
    color: white;
    margin-bottom: 4px;
}

.brand-subtitle {
    font-size: 12px;
    color: var(--muted);
}

.status-box {
    font-size: 13px;
    color: #cbd5e1;
    background: rgba(15, 23, 42, .95);
    border: 1px solid var(--border);
    padding: 14px;
    border-radius: 16px;
    word-break: break-word;
}

.app-title {
    text-align: center;
    font-size: 46px;
    font-weight: 950;
    letter-spacing: -1px;
    margin-bottom: 6px;
    background: linear-gradient(135deg, #ffffff, #a78bfa, #67e8f9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.app-subtitle {
    text-align: center;
    font-size: 15px;
    color: var(--muted);
    margin-bottom: 34px;
}

.empty-box {
    text-align: center;
    margin-top: 95px;
    padding: 46px 36px;
    border: 1px solid rgba(148,163,184,.16);
    border-radius: 28px;
    background: rgba(15, 23, 42, .62);
    box-shadow: 0 24px 80px rgba(0,0,0,.28);
    backdrop-filter: blur(16px);
}

.empty-box h1 {
    font-size: 32px;
    font-weight: 900;
    color: white;
}

.empty-box p {
    color: var(--muted);
    font-size: 15px;
    line-height: 1.7;
}

.empty-icon {
    font-size: 58px;
    margin-bottom: 14px;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, var(--accent), #2563eb);
    color: white;
    border-radius: 14px;
    border: 0;
    height: 44px;
    font-weight: 800;
    box-shadow: 0 10px 28px rgba(37, 99, 235, .20);
}

.stButton > button:hover {
    color: white;
    border: 0;
    transform: translateY(-1px);
    box-shadow: 0 14px 34px rgba(139, 92, 246, .30);
}

.stTextInput input {
    background: rgba(15, 23, 42, .92);
    color: white;
    border: 1px solid var(--border);
    border-radius: 14px;
    height: 42px;
}

.stTextInput input:focus {
    border-color: var(--accent);
}

/* Input labels and placeholders stay readable on dark */
.stTextInput label, [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] * {
    color: #dbeafe;
}

.stTextInput input::placeholder {
    color: #64748b;
}

.stFileUploader {
    background: rgba(15, 23, 42, .9);
    border-radius: 16px;
    padding: 10px;
    border: 1px dashed #475569;
}

/* File uploader inner dropzone + text + browse button -> dark */
[data-testid="stFileUploaderDropzone"] {
    background: rgba(15, 23, 42, .92);
    color: #cbd5e1;
    border: 0;
}

[data-testid="stFileUploaderDropzone"] * {
    color: #cbd5e1;
}

[data-testid="stFileUploaderDropzone"] button {
    background: rgba(30, 41, 59, .95);
    color: #f1f5f9;
    border: 1px solid var(--border);
}

[data-testid="stFileUploaderDropzone"] button:hover {
    background: rgba(51, 65, 85, .95);
    color: white;
    border-color: var(--accent);
}

[data-testid="stFileUploaderFile"] {
    background: rgba(15, 23, 42, .92);
    color: #e2e8f0;
    border-radius: 12px;
}

[data-testid="stFileUploaderFile"] * {
    color: #e2e8f0;
}

div[data-testid="stChatMessage"] {
    padding: 10px 0;
}

div[data-testid="stChatMessageContent"] {
    border-radius: 18px;
    padding: 14px 18px;
    border: 1px solid rgba(148,163,184,.15);
    background: rgba(15, 23, 42, .75);
    box-shadow: 0 12px 30px rgba(0,0,0,.18);
}

div[data-testid="stChatMessageContent"],
div[data-testid="stChatMessageContent"] * {
    color: var(--text);
}

div[data-testid="stChatInput"] {
    max-width: 920px;
    margin: auto;
}

div[data-testid="stChatInput"] > div {
    background: rgba(15, 23, 42, .96);
    border: 1px solid #334155;
    border-radius: 22px;
    box-shadow: 0 18px 60px rgba(0,0,0,.38);
}

div[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: white !important;
    border-radius: 18px !important;
}

div[data-testid="stChatInput"] textarea::placeholder {
    color: #64748b;
}

/* Kill the white bar that wraps the chat input at the bottom */
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
[data-testid="stBottomBlockContainer"],
[data-testid="stBottom"] [data-testid="stVerticalBlock"],
[data-testid="stBottom"] [data-testid="stHorizontalBlock"] {
    background: transparent !important;
}

[data-testid="stBottomBlockContainer"] {
    background: linear-gradient(180deg, rgba(2,6,23,0), #020617 40%) !important;
}

/* Chat input send button -> dark */
div[data-testid="stChatInput"] button {
    background: transparent !important;
    color: #94a3b8 !important;
}

div[data-testid="stChatInput"] button:hover {
    color: var(--accent) !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
    gap: 8px;
}

/* Radio option labels -> dark theme text */
.stRadio label, .stRadio div[role="radiogroup"] label, .stRadio label * {
    color: #dbeafe;
}

[data-testid="stSidebar"] hr {
    border-color: #1e293b;
}

.small-muted {
    color: #94a3b8;
    font-size: 12px;
}

/* ---------- Native widgets forced to dark ---------- */

/* Alerts: success / warning / error / info */
[data-testid="stAlert"], div[role="alert"] {
    background: rgba(15, 23, 42, .92);
    color: #e2e8f0;
    border: 1px solid var(--border);
    border-radius: 14px;
}

[data-testid="stAlert"] *, div[role="alert"] * {
    color: #e2e8f0;
}

/* Captions */
[data-testid="stCaptionContainer"], .stCaption, [data-testid="stCaptionContainer"] * {
    color: var(--muted);
}

/* Spinner text */
[data-testid="stSpinner"], [data-testid="stSpinner"] * {
    color: #cbd5e1;
}

/* Tooltips / popovers / dropdown menus */
[data-baseweb="popover"], [data-baseweb="menu"], [role="listbox"], [role="option"] {
    background: #0f172a;
    color: #e2e8f0;
}

[role="option"]:hover {
    background: #1e293b;
}

/* Inline code and code blocks inside answers */
.stMarkdown code, [data-testid="stMarkdownContainer"] code {
    background: rgba(30, 41, 59, .9);
    color: #e2e8f0;
    border-radius: 6px;
}

.stMarkdown pre, [data-testid="stMarkdownContainer"] pre {
    background: rgba(2, 6, 23, .95);
    border: 1px solid var(--border);
    border-radius: 12px;
    color: #e2e8f0;
}

/* Links */
.stApp a {
    color: #a78bfa;
}

/* Scrollbars */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: #020617;
}

::-webkit-scrollbar-thumb {
    background: #1e293b;
    border-radius: 8px;
}

::-webkit-scrollbar-thumb:hover {
    background: #334155;
}

* {
    scrollbar-color: #1e293b #020617;
}

@media (max-width: 768px) {
    .app-title { font-size: 32px; }
    .empty-box { margin-top: 60px; padding: 28px 18px; }
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="app-title">🧠 DocuMind AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">Professional document intelligence for PDFs, websites, TXT and DOCX files</div>',
    unsafe_allow_html=True
)

for key, value in {
    "vector_store": None,
    "source_type": None,
    "source_name": None,
    "chat_history": [],
    "processed_file_names": [],
    "all_chats": []
}.items():
    if key not in st.session_state:
        st.session_state[key] = value


def save_current_chat():
    if not st.session_state.chat_history:
        return

    title = "New Conversation"
    for msg in st.session_state.chat_history:
        if msg.get("role") == "user":
            title = msg.get("content", "New Conversation")[:45]
            break

    chat_data = {
        "title": title,
        "source_type": st.session_state.source_type,
        "source_name": st.session_state.source_name,
        "messages": st.session_state.chat_history.copy()
    }

    if st.session_state.all_chats:
        st.session_state.all_chats[0] = chat_data
    else:
        st.session_state.all_chats.insert(0, chat_data)


def start_new_chat():
    save_current_chat()
    st.session_state.chat_history = []


def clear_all():
    st.session_state.vector_store = None
    st.session_state.source_type = None
    st.session_state.source_name = None
    st.session_state.chat_history = []
    st.session_state.processed_file_names = []
    st.session_state.all_chats = []


with st.sidebar:
    st.markdown("""
    <div class="brand-card">
        <div class="brand-title">DocuMind</div>
        <div class="brand-subtitle">Knowledge search assistant</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("＋ New Conversation"):
        start_new_chat()
        st.rerun()

    mode = st.radio("Input source", ["Website", "Document"])

    st.markdown("---")

    if mode == "Website":
        st.markdown("### 🌐 Website")
        url = st.text_input("Website URL", placeholder="https://example.com")

        if st.button("Load Source"):
            if not url:
                st.warning("Please enter a website URL.")
            else:
                try:
                    with st.spinner("Loading..."):
                        docs = load_website(url)
                        st.session_state.vector_store = create_vector_store(docs)
                        st.session_state.source_type = "Website"
                        st.session_state.source_name = url
                        st.session_state.chat_history = []
                        st.session_state.processed_file_names = []

                    st.success("Ready.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

    else:
        st.markdown("### 📄 Document")
        uploaded_files = st.file_uploader(
            "Upload PDF, TXT, or DOCX",
            type=["pdf", "txt", "docx"],
            accept_multiple_files=True
        )

        if uploaded_files:
            current_file_names = [file.name for file in uploaded_files]

            if current_file_names != st.session_state.processed_file_names:
                try:
                    with st.spinner("Loading..."):
                        all_docs = []
                        for file in uploaded_files:
                            all_docs.extend(load_uploaded_file(file))

                        st.session_state.vector_store = create_vector_store(all_docs)
                        st.session_state.source_type = "Document"
                        st.session_state.source_name = ", ".join(current_file_names)
                        st.session_state.processed_file_names = current_file_names
                        st.session_state.chat_history = []

                    st.success("Ready.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("---")

    if st.session_state.vector_store:
        st.markdown(
            f"""
            <div class="status-box">
                ✅ <b>Source active</b><br><br>
                <b>Type:</b> {st.session_state.source_type}<br>
                <b>Source:</b> {st.session_state.source_name}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.info("Load a source to begin.")

    st.markdown("---")
    st.markdown("### Recent chats")

    if st.session_state.all_chats:
        for idx, chat in enumerate(st.session_state.all_chats):
            title = chat.get("title", f"Chat {idx + 1}")
            if st.button(title, key=f"chat_history_{idx}", type="secondary"):
                st.session_state.chat_history = chat.get("messages", []).copy()
                st.session_state.source_type = chat.get("source_type")
                st.session_state.source_name = chat.get("source_name")
                st.rerun()
    else:
        st.caption("No saved conversations yet.")

    st.markdown("---")

    if st.button("Clear workspace"):
        clear_all()
        st.rerun()


if len(st.session_state.chat_history) == 0:
    st.markdown("""
    <div class="empty-box">
        <div class="empty-icon">✨</div>
        <h1>Analyze your content instantly</h1>
        <p>Upload a document or load a website, then ask questions in natural language.</p>
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("page_info"):
            st.caption(msg["page_info"])

question = st.chat_input("Ask anything from your selected source...")

if question:
    if st.session_state.vector_store is None:
        st.warning("Please load a website or upload a document first.")
    else:
        st.session_state.chat_history.append({"role": "user", "content": question})

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    answer, page_info = answer_question(
                        st.session_state.vector_store,
                        question,
                        st.session_state.source_type
                    )

                    st.markdown(answer)

                    if page_info:
                        st.caption(page_info)

                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": answer,
                        "page_info": page_info
                    })

                    save_current_chat()

                except Exception as e:
                    st.error(f"Error: {e}")

        st.rerun()