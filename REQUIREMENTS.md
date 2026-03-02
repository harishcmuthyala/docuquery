# Requirements — DocuQuery RAG System

**Version:** 3.0  
**Status:** Implemented  
**Stack:** Python, LangGraph, Groq, FAISS, Streamlit  

---

## System Overview

RAG system with ReAct agent that analyzes questions, decides optimal search strategy, and generates grounded answers.

**Key Features:**
- ReAct agent (reason → act → generate)
- Smart question division for complex queries
- FAISS vector storage
- Groq LLM (llama-3.1-8b-instant)
- Optional LangSmith tracing

---

## Functional Requirements

### FR-01: PDF Upload
- Accept PDF files via Streamlit uploader
- Extract text with PyMuPDF
- Handle errors: password-protected, corrupted, no text

### FR-02: Text Chunking
- **Fixed**: 500 tokens, 50 overlap
- **Semantic**: paragraph boundaries, max 600 tokens
- User selectable strategy

### FR-03: Embeddings
- Model: sentence-transformers/all-MiniLM-L6-v2 (384 dim)
- Local, no API cost
- Same model for chunks and queries

### FR-04: Vector Storage
- FAISS IndexFlatL2
- Storage: `./faiss_db/{collection_name}/`
- Metadata: source_file, page_number, chunk_index, strategy

### FR-05: ReAct Agent
**Flow:** reason → act → generate

**Reason Phase:**
- LLM analyzes question complexity
- DIVIDE if: comparison (X vs Y), multiple topics (X and Y)
- NO DIVISION if: single concept
- Output: 1 or 2 search queries

**Act Phase:**
- Search each query (top_k=5 for single, 3 for divided)
- Deduplicate chunks
- Log actions

**Generate Phase:**
- Format context from chunks
- Generate answer via Groq LLM
- Return answer + reasoning trace

**Performance:**
- Simple: 2 LLM calls, 1 search
- Complex: 2 LLM calls, 2 searches

### FR-06: LangSmith Tracing (Optional)
- Optional LANGSMITH_API_KEY
- Status indicator in sidebar
- Graceful degradation if disabled

### FR-07: Query History
- Session metrics (total queries, avg chunks, divided count)
- Expandable query list
- Reverse chronological order

### FR-08: Reasoning Trace
- Shows agent's decision (DIVIDE/NO DIVISION)
- Lists search operations
- Displays chunk counts

---

## UI Specification

**Sidebar:**
- PDF uploader
- Chunking strategy selector
- Active document display
- API status indicators

**Main Tabs:**
1. Query — question input, answer, reasoning trace
2. Query History — metrics, query list

---

## Error Handling

| Error | Message |
|-------|---------|
| Password-protected PDF | "This PDF is password protected" |
| Corrupted PDF | "Could not read this file" |
| No text in PDF | "No text found. OCR not supported" |
| Groq timeout | "LLM did not respond in time. Retry." |
| Groq rate limit | "Rate limit reached. Wait 30 seconds." |
| Invalid API key | "Invalid API key. Check .env file." |

---

## Non-Functional Requirements

- **Cost:** $0 (Groq free tier, local models)
- **Performance:** 
  - Simple query: < 5 seconds
  - Complex query: < 7 seconds
  - FAISS retrieval: < 1 second
- **Security:** API keys in .env only, never committed
- **Code Quality:** Docstrings, no hardcoded strings

---

## Environment

```bash
# .env
GROQ_API_KEY=gsk_your_key_here
LANGSMITH_API_KEY=ls_your_key_here  # Optional
LOG_LEVEL=INFO
```

---

## Dependencies

```
langchain==0.3.14
langchain-core==0.3.75
langchain-groq==0.2.1
langgraph==0.2.62
langsmith==0.2.5
groq==0.13.0
faiss-cpu==1.9.0
sentence-transformers==3.3.1
PyMuPDF==1.24.1
streamlit==1.41.1
python-dotenv==1.0.1
```

---

## Test Coverage

✅ Unit tests for all modules (pdf_parser, chunker, vector_store, retriever, llm, prompt_templates)  
✅ Error handling tests  
✅ Sample questions CSV in `/tests/`

---

## Future Enhancements

- Evaluation metrics (RAGAS)
- Batch evaluation via CSV
- OCR for scanned PDFs
- Multi-document querying
- Streaming responses
- Re-ranking with cross-encoder
- Deployment to cloud platforms
