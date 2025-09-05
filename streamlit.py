import streamlit as st
import requests

API_BASE = "https://3ca0a3e92209.ngrok-free.app/api"  # FastAPI backend base URL

st.set_page_config(page_title="PDF RAG Assistant", page_icon="📚", layout="wide")

st.title("📚 PDF RAG Assistant")
st.markdown("Easily upload your PDFs and chat with them.")

# ==================================================
# Sidebar navigation
# ==================================================
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to:", ["📤 Upload PDF", "💬 Chat with PDFs"])

# ==================================================
# Upload PDF Page
# ==================================================
if page == "📤 Upload PDF":
    st.header("📤 Upload a PDF")

    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    if uploaded_file is not None:
        if st.button("Upload PDF"):
            with st.spinner("Uploading and processing..."):
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                try:
                    response = requests.post(f"{API_BASE}/upload-pdf", files=files)
                    if response.status_code == 200:
                        st.success("✅ PDF uploaded successfully!")
                        st.json(response.json())
                    else:
                        st.error(f"❌ Failed: {response.json().get('detail')}")
                except Exception as e:
                    st.error(f"❌ Request failed: {str(e)}")

# ==================================================
# Chat Page
# ==================================================
elif page == "💬 Chat with PDFs":
    # st.header("💬 Chat with your PDFs")

    if "messages" not in st.session_state:
        st.session_state.messages = []  # reset each refresh

    # ---------------------------
    # Display chat history in order
    # ---------------------------
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ---------------------------
    # Input box at bottom
    # ---------------------------
    if prompt := st.chat_input("Ask a question about your PDFs..."):
        # 1. Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. Query FastAPI backend
        try:
            response = requests.post(f"{API_BASE}/query", data={"question": prompt})
            if response.status_code == 200:
                answer = response.json().get("answer", "⚠️ No response.")
            else:
                answer = f"❌ Error: {response.json().get('detail')}"
        except Exception as e:
            answer = f"❌ Request failed: {str(e)}"

        # 3. Add assistant reply
        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)

