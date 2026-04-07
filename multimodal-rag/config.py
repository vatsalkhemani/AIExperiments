"""Configuration for multimodal RAG."""

import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Models
EMBEDDING_MODEL = "gemini-embedding-2-preview"
GENERATION_MODEL = "gemini-3.1-flash-lite-preview"

# Embeddings
EMBEDDING_DIMENSION = 768

# ChromaDB
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "multimodal"

# Retrieval
TOP_K = 5

# Limits (per Gemini Embedding 2 docs)
MAX_VIDEO_SECONDS = 120
MAX_PDF_PAGES = 6
SUPPORTED_TYPES = {
    "image": [".png", ".jpg", ".jpeg", ".webp"],
    "video": [".mp4", ".mov"],
    "audio": [".mp3", ".wav"],
    "pdf": [".pdf"],
    "text": [".txt", ".md"],
}
