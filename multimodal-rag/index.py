"""Embed and index files directly using Gemini multimodal embeddings."""

import os
import mimetypes
import chromadb
from google import genai
from google.genai import types

import config


client = genai.Client(api_key=config.GOOGLE_API_KEY)

MIME_MAP = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".mp4": "video/mp4",
    ".mov": "video/quicktime",
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".pdf": "application/pdf",
    ".txt": "text/plain",
    ".md": "text/plain",
}


def get_collection() -> chromadb.Collection:
    db = chromadb.PersistentClient(path=config.CHROMA_DB_PATH)
    return db.get_or_create_collection(
        name=config.COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def embed_file(file_path: str) -> list[float]:
    """Embed any supported file directly — no text conversion."""
    ext = os.path.splitext(file_path)[1].lower()
    mime_type = MIME_MAP.get(ext)
    if not mime_type:
        raise ValueError(f"Unsupported file type: {ext}")

    with open(file_path, "rb") as f:
        data = f.read()

    response = client.models.embed_content(
        model=config.EMBEDDING_MODEL,
        contents=types.Content(
            parts=[types.Part.from_bytes(data=data, mime_type=mime_type)]
        ),
        config=types.EmbedContentConfig(
            output_dimensionality=config.EMBEDDING_DIMENSION
        ),
    )
    return response.embeddings[0].values


def embed_text(text: str) -> list[float]:
    """Embed a text query."""
    response = client.models.embed_content(
        model=config.EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            output_dimensionality=config.EMBEDDING_DIMENSION
        ),
    )
    return response.embeddings[0].values


def get_content_type(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    for content_type, extensions in config.SUPPORTED_TYPES.items():
        if ext in extensions:
            return content_type
    return "unknown"


def index_file(file_path: str) -> str:
    """Embed and store a single file. Returns the item ID."""
    collection = get_collection()
    file_name = os.path.basename(file_path)
    item_id = file_name

    # Skip if already indexed
    existing = collection.get(ids=[item_id])
    if existing["ids"]:
        return item_id

    embedding = embed_file(file_path)
    content_type = get_content_type(file_path)

    collection.add(
        ids=[item_id],
        embeddings=[embedding],
        documents=[file_name],
        metadatas=[{
            "file_name": file_name,
            "content_type": content_type,
            "file_path": os.path.abspath(file_path),
        }],
    )
    return item_id


def index_files(file_paths: list[str], progress_callback=None) -> int:
    """Index multiple files. Returns count of newly indexed items."""
    count = 0
    for i, path in enumerate(file_paths):
        if progress_callback:
            progress_callback(f"Indexing {os.path.basename(path)} ({i+1}/{len(file_paths)})")
        index_file(path)
        count += 1
    return count


def clear_index():
    db = chromadb.PersistentClient(path=config.CHROMA_DB_PATH)
    try:
        db.delete_collection(config.COLLECTION_NAME)
    except ValueError:
        pass
