"""LLM utilities for RAG"""

from typing import List
import logging

logger = logging.getLogger(__name__)


def format_context(retrieved_chunks: List) -> str:
    """Format retrieved chunks into context string"""
    if not retrieved_chunks:
        return ""
    
    context_parts = []
    for i, retrieved in enumerate(retrieved_chunks, 1):
        chunk = retrieved.chunk
        context_parts.append(
            f"[CHUNK {i}] (Source: {chunk.source_file}, Page {chunk.page_number})\n{chunk.text}"
        )
    
    return "\n\n".join(context_parts)
