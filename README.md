# DocuQuery — RAG System with ReAct Agent

Upload a PDF. Ask questions. Get intelligent answers powered by a ReAct agent that reasons before acting.

---

## What It Does

DocuQuery is a RAG system with an intelligent ReAct agent. Upload any PDF and ask questions. The agent analyzes each question, decides if it needs division into sub-questions, retrieves targeted chunks, and generates comprehensive answers.

---

## Features

- PDF upload and intelligent text chunking (fixed-size or semantic)
- Local embeddings with sentence-transformers — no OpenAI API needed
- **ReAct Agent (Reasoning + Acting)** that decides optimal search strategy
- Smart question analysis: divides complex questions, keeps simple ones intact
- Efficient retrieval: 1 search for simple questions, 2 targeted searches for complex
- Visible reasoning trace showing agent's decision-making process
- LangSmith tracing for complete observability (optional)
- FAISS vector store for fast similarity search

---

## Architecture

```
PDF Upload
    │
    ▼
PyMuPDF (text extraction)
    │
    ▼
Chunker ──────────────────── Fixed-size (500 tokens, 50 overlap)
    │                         Semantic (paragraph boundaries)
    ▼
sentence-transformers (all-MiniLM-L6-v2) — local, free
    │
    ▼
FAISS (vector store) — fast, local
    │
    ▼
ReAct Agent (LangGraph)
    │
    ├─ Reason: Analyze question → decide division
    │
    ├─ Act: Search (1 or 2 queries based on reasoning)
    │
    └─ Generate: Synthesize answer from chunks
    │
    ▼
Groq API — llama-3.1-8b-instant (free tier)
    │
    ▼
Answer + Reasoning Trace + Actions
```

---

## Tech Stack

| Component | Tool | Why |
|---|---|---|
| LLM | Groq (llama-3.1-8b-instant) | Free tier, fast inference |
| Embeddings | sentence-transformers | Runs locally, no API cost |
| Vector DB | FAISS | Fast, lightweight, local |
| Agent | LangGraph + ReAct | Reasoning + Acting pattern |
| Observability | LangSmith (optional) | Complete tracing of all operations |
| Frontend | Streamlit | Fast to build and deploy |

---

## Getting Started

**Prerequisites:** Python 3.10+, a free [Groq API key](https://console.groq.com), optional [LangSmith API key](https://smith.langchain.com)

```bash
git clone https://github.com/harishcmuthyala/docuquery
cd docuquery

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Add your Groq API key to .env
# Optionally add LANGSMITH_API_KEY for tracing

streamlit run app.py
```

---

## ReAct Agent Flow

The agent uses a 3-step process for every question:

1. **Reason**: LLM analyzes the question
   - Simple question → use original query
   - Complex question → divide into 2 sub-questions

2. **Act**: Retrieve chunks based on reasoning
   - 1 query → retrieve 5 chunks
   - 2 queries → retrieve 3 chunks each, deduplicate

3. **Generate**: Synthesize final answer
   - Uses all retrieved chunks
   - Merges results for divided questions

**Examples:**
- "What is the decoder stack?" → 1 search, 5 chunks
- "Compare encoder vs decoder" → 2 searches, 6 chunks

**Efficiency:**
- Simple questions: 2 LLM calls, 1 search
- Complex questions: 2 LLM calls, 2 searches

---

## Project Structure

```
docuquery/
├── app.py                  # Streamlit entry point
├── ingestion/
│   ├── pdf_parser.py       # Text extraction
│   └── chunker.py          # Fixed-size and semantic chunking
├── retrieval/
│   ├── vector_store.py     # FAISS operations
│   └── retriever.py        # Top-k similarity retrieval
├── generation/
│   ├── prompt_templates.py # System prompts
│   ├── llm.py              # Groq LLM integration
│   └── agent.py            # ReAct agent (LangGraph)
├── evaluation/
│   └── langsmith_tracing.py # LangSmith observability (optional)
├── tests/                  # Unit tests
├── .env.example
├── requirements.txt
├── REQUIREMENTS.md         # Full technical requirements
└── SETUP.md                # Quick setup guide
```

---

## Status

✅ Core features complete

- [x] Requirements defined
- [x] PDF ingestion pipeline
- [x] Chunking strategies (fixed-size, semantic)
- [x] FAISS vector store integration
- [x] Groq LLM integration (llama-3.1-8b-instant)
- [x] LangSmith tracing (optional)
- [x] ReAct agent with smart question division
- [x] Efficient retrieval (retrieve after reasoning)
- [x] Duplicate response fix
- [ ] Comprehensive testing
- [ ] Deployment

---

## License

MIT
