"""Retrieve relevant content and generate answers."""

import os
from google import genai
from google.genai import types

import config
from index import get_collection, embed_text


client = genai.Client(api_key=config.GOOGLE_API_KEY)

MIME_MAP = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".webp": "image/webp", ".pdf": "application/pdf",
    ".mp4": "video/mp4", ".mov": "video/quicktime",
    ".mp3": "audio/mpeg", ".wav": "audio/wav",
}


def retrieve(query: str, top_k: int = None) -> list[dict]:
    """Search the index with a text query. Returns ranked results."""
    top_k = top_k or config.TOP_K
    collection = get_collection()

    if collection.count() == 0:
        return []

    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    retrieved = []
    for i in range(len(results["ids"][0])):
        distance = results["distances"][0][i]
        similarity = 1 - (distance / 2)
        retrieved.append({
            "id": results["ids"][0][i],
            "file_name": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "similarity": round(similarity, 4),
        })
    return retrieved


def answer(query: str) -> dict:
    """Retrieve relevant files and generate an answer using the original media."""
    results = retrieve(query)

    if not results:
        return {"answer": "No content has been indexed yet.", "sources": []}

    # Build multimodal prompt with the actual retrieved files
    parts = []
    for r in results:
        file_path = r["metadata"].get("file_path", "")
        content_type = r["metadata"].get("content_type", "")

        if os.path.exists(file_path) and content_type in ("image", "pdf"):
            with open(file_path, "rb") as f:
                data = f.read()
            ext = os.path.splitext(file_path)[1].lower()
            mime = MIME_MAP.get(ext, "application/octet-stream")
            parts.append(types.Part.from_bytes(data=data, mime_type=mime))
            parts.append(types.Part.from_text(text=f"[Above: {r['file_name']}]"))
        elif os.path.exists(file_path) and content_type == "text":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text_content = f.read()
            parts.append(types.Part.from_text(text=f"[File: {r['file_name']}]\n{text_content}"))
        else:
            parts.append(types.Part.from_text(text=f"[Retrieved file: {r['file_name']} ({content_type})]"))

    parts.append(types.Part.from_text(
        text=f"Based on the retrieved content above, answer this question: {query}\n\n"
        f"Reference specific files when relevant. If the content doesn't contain "
        f"enough information, say so."
    ))

    response = client.models.generate_content(
        model=config.GENERATION_MODEL,
        contents=[types.Content(parts=parts)],
    )

    return {"answer": response.text, "sources": results}
