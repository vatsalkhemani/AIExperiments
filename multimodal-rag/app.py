"""Streamlit app for multimodal RAG."""

import os
import tempfile
import streamlit as st

from index import index_files, clear_index, get_collection
from retrieve import answer
import config


st.set_page_config(page_title="Multimodal RAG", layout="wide")
st.title("Multimodal RAG")
st.caption(
    "Upload images, videos, audio, PDFs, or text. "
    "Everything gets embedded directly — no text conversion. "
    "Then ask questions across all of it."
)

# Flatten supported extensions
ALL_EXTENSIONS = []
for exts in config.SUPPORTED_TYPES.values():
    ALL_EXTENSIONS.extend([e.lstrip(".") for e in exts])

# --- Sidebar ---
with st.sidebar:
    st.header("Content")

    uploaded_files = st.file_uploader(
        "Upload files",
        type=ALL_EXTENSIONS,
        accept_multiple_files=True,
        help="Images, videos (≤2min), audio (≤80s), PDFs (≤6 pages), text files",
    )

    if uploaded_files:
        if st.button("Index all files", type="primary", use_container_width=True):
            # Save to temp directory
            temp_dir = os.path.join(tempfile.gettempdir(), "multimodal_rag")
            os.makedirs(temp_dir, exist_ok=True)

            paths = []
            for f in uploaded_files:
                path = os.path.join(temp_dir, f.name)
                with open(path, "wb") as out:
                    out.write(f.read())
                paths.append(path)

            progress = st.empty()
            with st.spinner("Embedding..."):
                count = index_files(paths, progress_callback=lambda msg: progress.text(msg))
            progress.empty()
            st.success(f"Indexed {count} files")

    # Status
    collection = get_collection()
    count = collection.count()
    if count > 0:
        st.divider()
        st.metric("Indexed files", count)
        if st.button("Clear index"):
            clear_index()
            st.rerun()

# --- Chat ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("Ask something about your content...")

if query:
    st.session_state["messages"].append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = answer(query)

        st.markdown(result["answer"])

        if result["sources"]:
            with st.expander("Retrieved sources", expanded=False):
                for i, src in enumerate(result["sources"]):
                    meta = src["metadata"]
                    sim = f"{src['similarity']:.0%}"
                    st.markdown(f"**{src['file_name']}** ({meta['content_type']}) — {sim} match")

                    # Show preview for images
                    file_path = meta.get("file_path", "")
                    if meta["content_type"] == "image" and os.path.exists(file_path):
                        st.image(file_path, width=320)

                    if i < len(result["sources"]) - 1:
                        st.divider()

    st.session_state["messages"].append({
        "role": "assistant",
        "content": result["answer"],
    })
