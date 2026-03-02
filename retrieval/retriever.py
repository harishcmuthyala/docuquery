"""Top-k similarity retrieval"""

from typing import List
from dataclasses import dataclass
import logging
from langchain_community.vectorstores import FAISS
from ingestion.chunker import Chunk

logger = logging.getLogger(__name__)


@dataclass
class RetrievedChunk:
    chunk: Chunk
    similarity_score: float
    rank: int


def query(vectorstore: FAISS, query_text: str, top_k: int = 5) -> List[RetrievedChunk]:
    """Query FAISS vector store and return top-k chunks"""
    try:
        results = vectorstore.similarity_search_with_score(query_text, k=top_k)
        retrieved_chunks = []
        
        for rank, (doc, distance) in enumerate(results, start=1):
            similarity = 1 / (1 + distance)
            
            chunk = Chunk(
                chunk_id=doc.metadata.get("chunk_id", "unknown"),
                source_file=doc.metadata["source_file"],
                page_number=doc.metadata["page_number"],
                chunk_index=doc.metadata["chunk_index"],
                text=doc.page_content,
                token_count=doc.metadata["token_count"],
                strategy=doc.metadata["strategy"]
            )
            
            retrieved_chunks.append(RetrievedChunk(
                chunk=chunk,
                similarity_score=similarity,
                rank=rank
            ))
        
        logger.info(f"Retrieved {len(retrieved_chunks)} chunks")
        return retrieved_chunks
        
    except Exception as e:
        logger.error(f"Failed to query vector store: {e}")
        raise


def format_context_for_prompt(retrieved_chunks: List[RetrievedChunk]) -> str:
    """Format retrieved chunks into context string (for tests)"""
    if not retrieved_chunks:
        return ""
    
    return "\n\n".join([
        f"[CHUNK {i}] (Source: {chunk.chunk.source_file}, Page {chunk.chunk.page_number})\n{chunk.chunk.text}"
        for i, chunk in enumerate(retrieved_chunks, start=1)
    ])