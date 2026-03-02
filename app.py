"""DocuQuery - RAG System with ReAct Agent"""

import streamlit as st
import os
from dotenv import load_dotenv
import hashlib
import tempfile
import logging

load_dotenv()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

from evaluation.langsmith_tracing import setup_langsmith_tracing, get_tracing_status
setup_langsmith_tracing(project_name="docuquery-rag")

from ingestion.pdf_parser import extract_pages, PDFPasswordProtectedError, PDFCorruptedError, PDFNoTextError
from ingestion.chunker import chunk
from retrieval.vector_store import create_vectorstore, delete_vectorstore, generate_collection_name, get_embeddings
from generation.agent import run_react_agent

st.set_page_config(page_title="DocuQuery", page_icon="📄", layout="wide")

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "current_collection" not in st.session_state:
    st.session_state.current_collection = None
if "query_history" not in st.session_state:
    st.session_state.query_history = []
if "embeddings" not in st.session_state:
    st.session_state.embeddings = None


def check_api_key():
    api_key = os.getenv("GROQ_API_KEY")
    return api_key and api_key != "gsk_your_key_here"


def compute_file_hash(file_bytes):
    return hashlib.md5(file_bytes).hexdigest()


def process_pdf(uploaded_file, strategy):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        with st.spinner("Extracting text from PDF..."):
            pages = extract_pages(tmp_path)
            st.success(f"✓ Extracted {len(pages)} pages")
        
        with st.spinner(f"Chunking text ({strategy} strategy)..."):
            chunks = chunk(pages, strategy=strategy)
            st.success(f"✓ Created {len(chunks)} chunks")
        
        file_hash = compute_file_hash(uploaded_file.getvalue())
        collection_name = generate_collection_name(uploaded_file.name, strategy, file_hash)
        
        with st.spinner("Creating embeddings and vector store..."):
            if st.session_state.embeddings is None:
                st.session_state.embeddings = get_embeddings()
            
            vectorstore = create_vectorstore(chunks, collection_name, st.session_state.embeddings)
            st.success(f"✓ Vector store created: {collection_name}")
        
        os.unlink(tmp_path)
        return vectorstore, collection_name
        
    except PDFPasswordProtectedError:
        st.error("❌ This PDF is password protected and cannot be processed")
    except PDFCorruptedError:
        st.error("❌ Could not read this file. Please check the file is a valid PDF")
    except PDFNoTextError:
        st.error("❌ No text found in this PDF. OCR is not currently supported")
    except Exception as e:
        st.error(f"❌ Error processing PDF: {e}")
        logger.error(f"PDF processing error: {e}")
    return None, None


def main():
    st.title("📄 DocuQuery")
    st.caption("RAG System with ReAct Agent")
    
    with st.sidebar:
        st.header("Configuration")
        
        if check_api_key():
            st.success("🟢 Groq API key configured")
        else:
            st.error("🔴 Groq API key not configured")
            st.info("Add your GROQ_API_KEY to the .env file")
        
        tracing_status = get_tracing_status()
        if tracing_status["enabled"]:
            st.success(f"🟢 LangSmith tracing enabled")
        else:
            st.info("💡 Add LANGSMITH_API_KEY to .env for tracing")
        
        st.divider()
        
        st.info("🤖 **Smart Agent**")
        st.caption("Automatically decides if questions need division for better results.")
        
        st.divider()
        
        strategy = st.radio(
            "Chunking Strategy",
            options=["fixed", "semantic"],
            help="Fixed: 500 tokens with overlap | Semantic: Paragraph boundaries"
        )
        
        uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
        
        if uploaded_file:
            if st.button("Process Document", type="primary"):
                vectorstore, collection_name = process_pdf(uploaded_file, strategy)
                if vectorstore:
                    st.session_state.vectorstore = vectorstore
                    st.session_state.current_collection = collection_name
                    st.rerun()
        
        st.divider()
        
        if st.session_state.current_collection:
            st.info(f"📚 Active: {st.session_state.current_collection}")
            
            if st.button("Clear Document"):
                delete_vectorstore(st.session_state.current_collection)
                st.session_state.vectorstore = None
                st.session_state.current_collection = None
                st.session_state.query_history = []
                st.rerun()
    
    tab1, tab2 = st.tabs(["Query", "Query History"])
    
    with tab1:
        st.header("Ask Questions")
        
        if not check_api_key():
            st.warning("⚠️ Please configure your Groq API key in the .env file")
            return
        
        if not st.session_state.vectorstore:
            st.info("👆 Upload and process a PDF document to get started")
            return
        
        question = st.text_area("Your Question", placeholder="Ask a question about your document...", height=100)
        
        if st.button("Ask", type="primary", disabled=not question) and question:
            try:
                with st.spinner("Analyzing question and generating answer..."):
                    answer, reasoning_steps, actions_taken = run_react_agent(question, st.session_state.vectorstore)
                
                st.success("Answer")
                st.write(answer)
                
                if reasoning_steps or actions_taken:
                    with st.expander("🧠 Agent Reasoning Trace"):
                        if reasoning_steps:
                            st.markdown("**Reasoning Steps:**")
                            for i, step in enumerate(reasoning_steps, 1):
                                st.markdown(f"{i}. {step}")
                        
                        if actions_taken:
                            st.markdown("**Actions Taken:**")
                            for i, action in enumerate(actions_taken, 1):
                                st.markdown(f"{i}. {action}")
                
                st.session_state.query_history.append({
                    "question": question,
                    "answer": answer,
                    "strategy": st.session_state.current_collection.split("_")[-2] if st.session_state.current_collection else "unknown",
                    "divided": len(actions_taken) > 1
                })
                
                if get_tracing_status()["enabled"]:
                    st.info("🔍 View trace in LangSmith: https://smith.langchain.com")
            
            except Exception as e:
                st.error(f"❌ Error: {e}")
                logger.exception("Query error:")
    
    with tab2:
        st.header("Query History")
        
        if not st.session_state.query_history:
            st.info("Run some queries to see history")
        else:
            history = st.session_state.query_history
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Queries", len(history))
            col2.metric("Avg Chunks", f"{sum(q.get('num_chunks', 0) for q in history) / len(history):.1f}")
            col3.metric("Divided Questions", sum(1 for q in history if q.get("divided")))
            
            st.divider()
            
            for i, q in enumerate(reversed(history), 1):
                with st.expander(f"Query {len(history) - i + 1}: {q['question'][:60]}..."):
                    st.markdown(f"**Question:** {q['question']}")
                    st.markdown(f"**Answer:** {q['answer']}")
                    st.caption(f"Strategy: {q['strategy']} | {'Divided' if q.get('divided') else 'Simple'}")


if __name__ == "__main__":
    main()
