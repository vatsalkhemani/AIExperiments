# AI Experiments

Self-contained experiments across the AI stack. Each folder is a standalone build exploring a different concept (embeddings, retrieval, evaluation, fine-tuning) with its own code, dependencies, and documentation.

## Experiments

| Experiment | What it explores | Tech |
|-----------|-----------------|------|
| [Multimodal RAG](./multimodal-rag/) | RAG over images, video, audio, and PDFs using native multimodal embeddings | Gemini Embedding 2, ChromaDB, Streamlit |
| Eval Harness | Running identical prompts across models, scoring and comparing outputs | Coming soon |
| Fine-Tuning | LoRA fine-tuning on a classification task | Coming soon |

### Multimodal RAG

**Input:** Any mix of images, videos, audio, PDFs, and text files

Traditional RAG over non-text content requires lossy conversion: OCR your PDFs, transcribe audio, caption images, then embed the resulting text. Gemini Embedding 2 embeds raw bytes directly, so all modalities live in one vector space with no intermediate text step. This project uploads mixed content, indexes it through native multimodal embeddings, and lets you ask questions across all of it.

**Output:** Conversational answers grounded in retrieved content, with source files and similarity scores.

## Context

My other repos go deep on specific areas: [Agent-Factory](https://github.com/vatsalkhemani/Agent-Factory) for agentic patterns across different LLMs and tools, [Multi-Agent-Systems](https://github.com/vatsalkhemani/Multi-Agent-Systems) for orchestration patterns like collaborative synthesis, adversarial debate, and critique-driven revision. This repo goes wide. Each experiment answers a specific question I had about how something works under the hood.

## Structure

```
AI-Experiments/
├── multimodal-rag/
├── eval-harness/          # coming soon
├── fine-tuning/           # coming soon
└── README.md
```

Each experiment has its own README and a technical doc explaining architecture decisions. All code is self-contained with instructions to run locally.
