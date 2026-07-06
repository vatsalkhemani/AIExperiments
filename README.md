# AI Experiments

A collection of AI experiments that excite me. Each folder is a standalone project with its own stack, setup, and README.

## Projects

| Project | What it is | Tech |
|---------|-----------|------|
| [Multimodal RAG](./multimodal-rag/) | RAG using native multimodal embeddings over images, video, audio, and PDFs — no lossy text conversion | Gemini Embedding 2, Gemini 3.1 Flash Lite, ChromaDB, Streamlit |
| [Road Clash](./road-rash-game/) | A Road Rash–style 3D motorcycle combat racer in the browser — procedural valley landscape, rival riders you can punch, 3-lap races | Three.js, WebAudio, vanilla JS (no build step) |
| [Nightflight](./nightflight/) | First-person broom flight over a night-time Hogwarts — Great Hall under floating candles, live Quidditch match, sun cycle, collision, all procedural with zero downloaded assets | Three.js + UnrealBloom, WebAudio, vanilla JS (no build step) |

## Structure

Each project is a silo with its own deps and README:

```
AIExperiments/
├── multimodal-rag/     # multimodal retrieval + grounded answers
├── road-rash-game/     # browser motorcycle combat racer
├── nightflight/        # first-person broom flight over Hogwarts
└── README.md
```

See each project's README for setup and details.
