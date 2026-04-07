# Multimodal RAG

RAG over images, video, audio, and PDFs using Gemini Embedding 2. No OCR, no transcription, no captioning. Files go in as raw bytes and get embedded directly into a single vector space.

## How it works

**Input:** Upload any mix of files (images, videos up to 2 min, audio up to 80s, PDFs up to 6 pages, text)

The system:
- Reads each file as raw bytes and embeds it directly using `gemini-embedding-2-preview`
- Stores all vectors in one ChromaDB collection, all modalities sharing the same space
- Embeds your text query with the same model, retrieves the top 5 most similar files by cosine distance
- Passes the actual retrieved files (not text descriptions) to `gemini-3.1-flash-lite-preview` for answer generation

**Output:** Grounded answers referencing specific files, with similarity scores and source previews

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

## Structure

```
multimodal-rag/
├── app.py              # Streamlit interface
├── config.py           # Models, limits, supported types
├── index.py            # Multimodal embedding and ChromaDB indexing
├── retrieve.py         # Retrieval and grounded generation
├── requirements.txt
├── .env.example
└── TECHNICAL.md
```

For architecture decisions and what I learned, see [TECHNICAL.md](./TECHNICAL.md).
