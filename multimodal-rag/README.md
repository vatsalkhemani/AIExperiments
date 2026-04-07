# Multimodal RAG

Exploring what becomes possible when your embedding model natively understands images, video, audio, and PDFs, not just text.

## The problem

Traditional RAG over non-text content requires converting everything to text first. OCR your PDFs, transcribe your audio, caption your images, describe your video frames, then embed the text. Every conversion step is lossy. A chart becomes a text description that misses spatial relationships. An audio clip loses tone and non-speech sounds. A video frame loses everything the captioning model didn't mention. You end up searching over degraded proxies of the original content.

## What this project does

Uses Google's Gemini Embedding 2 (`gemini-embedding-2-preview`) to embed files directly as raw bytes. Images, videos, audio, PDFs, and text all go into the same vector space with no intermediate conversion. A text query retrieves the most relevant content regardless of its original modality. Retrieved files are then passed to Gemini 3.1 Flash Lite for grounded answer generation.

Upload a mix of files, index them, and ask questions across all of it through a chat interface.

## Stack

| Component | Detail |
|-----------|--------|
| Embeddings | `gemini-embedding-2-preview` (multimodal, 768d) |
| Generation | `gemini-3.1-flash-lite-preview` (multimodal) |
| Vector DB | ChromaDB (local, cosine similarity) |
| UI | Streamlit |

## Setup

```bash
cd multimodal-rag
pip install -r requirements.txt
cp .env.example .env
# Add your GOOGLE_API_KEY to .env (free from https://aistudio.google.com/apikey)
```

## Run

```bash
streamlit run app.py
```

Upload files through the sidebar (images, videos up to 2 min, audio up to 80s, PDFs up to 6 pages, text files), click "Index all files", then ask questions in the chat.

## Structure

```
multimodal-rag/
├── app.py              # Streamlit interface
├── config.py           # Models, limits, supported types
├── index.py            # Direct multimodal embedding and ChromaDB indexing
├── retrieve.py         # Query, retrieval, and grounded generation
├── requirements.txt
├── .env.example
└── TECHNICAL.md
```

For architecture decisions, design rationale, and learnings, see [TECHNICAL.md](./TECHNICAL.md).
