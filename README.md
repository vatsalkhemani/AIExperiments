# AI Experiments

A collection of AI experiments that excite me. New embedding model, new retrieval pattern, new training technique. Each folder is a standalone project with its own stack, setup, and writeup.

## Experiments

| Experiment | What it explores | Tech |
|-----------|-----------------|------|
| [Multimodal RAG](./multimodal-rag/) | RAG using native multimodal embeddings over images, video, audio, and PDFs | Gemini Embedding 2, Gemini 3.1 Flash Lite, ChromaDB, Streamlit |
| Eval Harness | Same prompt across models, scored and compared | Coming soon |
| Fine-Tuning | LoRA fine-tuning on a classification task | Coming soon |

---

### Multimodal RAG

**Input:** Any mix of images, videos, audio, PDFs, and text files

Traditional RAG converts everything to text before embedding: OCR your PDFs, transcribe audio, caption images. Every conversion is lossy. Gemini Embedding 2 skips all of that. It embeds raw bytes directly, so a text query matches against an image of a diagram without ever describing that diagram in words.

This project:
- Embeds files as raw bytes into a single ChromaDB collection using `gemini-embedding-2-preview`
- Puts all modalities (images, video, audio, PDFs, text) in the same vector space
- Retrieves the most relevant files for a text query regardless of their original type
- Passes retrieved files to Gemini 3.1 Flash Lite, which reads the actual content (not a text summary) and generates a grounded answer

**Output:** Conversational answers about your content, with retrieved source files and similarity scores

---

## Structure

Each experiment is a silo with its own deps, README, and technical doc.

```
AI-Experiments/
├── multimodal-rag/
├── eval-harness/          # coming soon
├── fine-tuning/           # coming soon
└── README.md
```
