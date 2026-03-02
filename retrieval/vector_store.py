"""FAISS vector storage operations"""

from typing import List, Optional
import os
import logging
import pickle
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from ingestion.chunker import Chunk

logger = logging.getLogger(__name__)


def get_embeddings() -> HuggingFaceEmbeddings:
    """Get HuggingFace embeddings model"""
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )


def get_persist_directory() -> str:
    """Get persist directory path"""
    persist_path = os.getenv("FAISS_PERSIST_PATH", "./faiss_db")
    os.makedirs(persist_path, exist_ok=True)
    return persist_path


def create_vectorstore(
    chunks: List[Chunk],
    collection_name: str,
    embeddings: Optional[HuggingFaceEmbeddings] = None
) -> FAISS:
    """Create FAISS vector store from chunks"""
    if embeddings is None:
        embeddings = get_embeddings()
    
    # Convert chunks to Documents
    documents = [
        Document(
            page_content=chunk.text,
            metadata={
                "chunk_id": chunk.chunk_id,
                "source_file": chunk.source_file,
                "page_number": chunk.page_number,
                "chunk_index": chunk.chunk_index,
                "strategy": chunk.strategy,
                "token_count": chunk.token_count
            }
        )
        for chunk in chunks
    ]
    
    logger.info(f"Creating FAISS index with {len(documents)} documents")
    
    # Create FAISS index
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    # Save to disk
    persist_dir = get_persist_directory()
    index_path = os.path.join(persist_dir, f"{collection_name}.faiss")
    vectorstore.save_local(index_path)
    
    logger.info(f"FAISS index saved: {index_path}")
    return vectorstore


def load_vectorstore(
    collection_name: str,
    embeddings: Optional[HuggingFaceEmbeddings] = None
) -> Optional[FAISS]:
    """Load existing FAISS vector store"""
    if embeddings is None:
        embeddings = get_embeddings()
    
    try:
        persist_dir = get_persist_directory()
        index_path = os.path.join(persist_dir, f"{collection_name}.faiss")
        
        if not os.path.exists(index_path):
            return None
        
        vectorstore = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
        logger.info(f"Loaded FAISS index: {collection_name}")
        return vectorstore
        
    except Exception as e:
        logger.error(f"Failed to load FAISS index: {e}")
        return None


def delete_vectorstore(collection_name: str) -> bool:
    """Delete FAISS vector store"""
    try:
        persist_dir = get_persist_directory()
        index_path = os.path.join(persist_dir, f"{collection_name}.faiss")
        
        if os.path.exists(index_path):
            import shutil
            shutil.rmtree(index_path)
            logger.info(f"Deleted FAISS index: {collection_name}")
            return True
        return False
        
    except Exception as e:
        logger.error(f"Failed to delete FAISS index: {e}")
        return False


def list_collections() -> List[str]:
    """List all FAISS collections"""
    try:
        persist_dir = get_persist_directory()
        if not os.path.exists(persist_dir):
            return []
        
        collections = [
            d.replace('.faiss', '')
            for d in os.listdir(persist_dir)
            if os.path.isdir(os.path.join(persist_dir, d)) and d.endswith('.faiss')
        ]
        return collections
        
    except Exception as e:
        logger.error(f"Failed to list collections: {e}")
        return []


def generate_collection_name(filename: str, strategy: str, file_hash: str) -> str:
    """Generate collection name from filename, strategy, and hash"""
    import re
    name = os.path.splitext(filename)[0]
    name = re.sub(r'[^a-zA-Z0-9_-]', '_', name).lower()
    return f"{name}_{strategy}_{file_hash[:8]}"
