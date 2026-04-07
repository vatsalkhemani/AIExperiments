# Technical Deep-Dive: Multimodal RAG

## Why Gemini Embedding 2 matters

Previous multimodal embedding approaches either used separate encoders per modality (like CLIP for images and a text model for text) aligned into a shared space via contrastive training, or required converting all content to text before embedding. Gemini Embedding 2 is a single model trained natively across all modalities. Text, images, video, audio, and PDFs go in as raw bytes and come out as vectors in one unified semantic space.

This means a text query like "architecture diagram" can match directly against an image of that diagram through cosine similarity. No captioning step, no information bottleneck.

## How the pipeline works

**Indexing.** Each uploaded file is read as raw bytes and sent directly to the embedding model with its MIME type. The model returns a 768-dimensional vector. That vector and the file metadata go into a single ChromaDB collection. There is no text extraction, no frame extraction, no transcription. The embedding model processes raw content natively.

**Retrieval.** The user's text query is embedded using the same model into the same vector space. ChromaDB returns the top-K most similar items by cosine distance, regardless of whether they were originally images, audio, video, PDFs, or text.

**Generation.** Retrieved files (images, PDFs) are passed as raw bytes to Gemini 3.1 Flash Lite alongside the query. The generation model sees the actual content, not a text summary of it. For video and audio, the prompt references the file name since streaming large media inline is impractical.

## Design decisions

**No text extraction pipeline.** The entire point of this project is to test whether multimodal embeddings make the traditional "convert everything to text" step unnecessary. If we OCR'd PDFs or captioned images before embedding, we'd be testing text embeddings with extra steps, not multimodal embeddings.

**Single collection for all modalities.** Everything lives in one ChromaDB collection. Retrieval naturally ranks the most semantically relevant content regardless of type. A query about a chart retrieves the chart image, not a transcript that happens to mention charts.

**Same provider for embedding and generation.** Both use Gemini. The embedding model understands how Gemini "sees" content, so retrieved results align well with what the generation model can reason about.

**768 dimensions with Matryoshka support.** The model outputs 3,072 dimensions by default but we use 768 as a practical tradeoff between quality and storage. Matryoshka means you can truncate embeddings to lower dimensions without recomputing them.

## Gemini Embedding 2 constraints

| Modality | Limit |
|----------|-------|
| Images | Up to 6 per request (PNG, JPEG, WebP) |
| Video | Up to 120s without audio, 80s with audio (MP4, MOV) |
| Audio | Up to 80 seconds (MP3, WAV) |
| PDFs | Up to 6 pages per request |
| Text | 8,192 tokens |
| Total | 8,192 token-equivalent cap across all modalities |

These are hard limits from the model. Longer videos, larger PDFs, and bigger documents need chunking. That segmentation logic is your responsibility, not the model's.

## What I learned

- The conversion pipeline (OCR, captioning, transcription) isn't just extra work, it's an information bottleneck. Multimodal embeddings bypass it entirely and retrieval quality improves because you're matching against the real content, not a text proxy
- Cross-modal retrieval actually works. A text query finds relevant images without any intermediate text description. This felt like magic the first time it worked
- The model's constraints (120s video, 6-page PDF) mean chunking is still necessary for large content. The model eliminates the *conversion* step, not the *segmentation* step
- Embedding cost varies dramatically by modality. Video is 60x more expensive per token than text. For large corpora, this matters
