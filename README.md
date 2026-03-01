# DocuQuery — RAG System with Automatic Evaluation

Upload a PDF. Ask questions. See exactly how well the system answered.

**[Live Demo](#)**

---

## What It Does

DocuQuery lets you upload any PDF document and ask natural language questions against it. Unlike most RAG demos, it doesn't just return an answer — it automatically scores every response on three quality metrics so you can see whether the system is hallucinating, retrieving the wrong context, or answering off-topic.

---

## Features

- PDF upload and intelligent text chunking (fixed-size or semantic)
- Local embeddings — no OpenAI API needed
- Sourced answers with page-level citations
- Automatic RAGAS evaluation on every query (faithfulness, relevancy, context precision)
- Evaluation dashboard with session history and chunking strategy comparison
- Batch evaluation mode — upload a CSV of questions, get scores for all of them

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
ChromaDB (vector store)
    │
    ▼
Groq API — llama3-8b-8192 (free tier)
    │
    ▼
Answer + Citations
    │
    ▼
RAGAS Evaluator → Faithfulness · Relevancy · Context Precision
```

---

## Tech Stack

| Component | Tool | Why |
|---|---|---|
| LLM | Groq (llama3-8b-8192) | Free tier, fast inference |
| Embeddings | sentence-transformers | Runs locally, no API cost |
| Vector DB | ChromaDB | Local, no infrastructure needed |
| Evaluation | RAGAS | Industry-standard RAG metrics |
| Frontend | Streamlit | Fast to build and deploy |
| Hosting | Hugging Face Spaces | Free permanent deployment |

---

## Getting Started

**Prerequisites:** Python 3.10+, a free [Groq API key](https://console.groq.com)

```bash
git clone https://github.com/harishcmuthyala/docuquery
cd docuquery

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Add your Groq API key to .env

streamlit run app.py
```

---

## Project Structure

```
docuquery/
├── app.py                  # Streamlit entry point
├── ingestion/
│   ├── pdf_parser.py       # Text extraction
│   ├── chunker.py          # Fixed-size and semantic chunking
│   └── embedder.py         # sentence-transformers embedding
├── retrieval/
│   ├── vector_store.py     # ChromaDB operations
│   └── retriever.py        # Top-k similarity retrieval
├── generation/
│   ├── prompt_templates.py
│   └── llm.py              # Groq API calls
├── evaluation/
│   ├── ragas_eval.py       # RAGAS scoring
│   └── dashboard.py        # Metrics aggregation
├── tests/
│   ├── fixtures/           # Sample PDFs for testing
│   └── sample_questions.csv
├── .env.example
├── requirements.txt
└── REQUIREMENTS.md         # Full technical requirements
```

---

## Status

🚧 In active development

- [x] Requirements defined
- [ ] PDF ingestion pipeline
- [ ] Chunking strategies
- [ ] ChromaDB integration
- [ ] Groq LLM integration
- [ ] RAGAS evaluation layer
- [ ] Evaluation dashboard
- [ ] Batch evaluation mode
- [ ] Deployment

---

## License

MIT
