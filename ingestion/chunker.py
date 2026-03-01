"""Text chunking strategies: fixed-size and semantic"""

from typing import List
from dataclasses import dataclass
import uuid
import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ingestion.pdf_parser import Page


@dataclass
class Chunk:
    chunk_id: str
    source_file: str
    page_number: int
    chunk_index: int
    text: str
    token_count: int
    strategy: str  # "fixed" | "semantic"


def chunk_fixed(pages: List[Page], chunk_size: int = 500, overlap: int = 50) -> List[Chunk]:
    """
    Fixed-size token chunking with overlap using LangChain.
    
    Args:
        pages: List of Page objects from PDF extraction
        chunk_size: Target size in tokens (default 500)
        overlap: Overlap between chunks in tokens (default 50)
        
    Returns:
        List of Chunk objects
    """
    # LangChain splitter with character-based splitting
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size * 4,  # Approximate: 1 token ≈ 4 chars
        chunk_overlap=overlap * 4,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    encoding = tiktoken.get_encoding("cl100k_base")
    chunks = []
    chunk_index = 0
    
    for page in pages:
        # Split text using LangChain
        text_chunks = splitter.split_text(page.text)
        
        for chunk_text in text_chunks:
            # Count actual tokens
            token_count = len(encoding.encode(chunk_text))
            
            # Skip very small chunks (< 100 tokens)
            if token_count < 100:
                continue
            
            chunks.append(Chunk(
                chunk_id=str(uuid.uuid4()),
                source_file=page.source_file,
                page_number=page.page_number,
                chunk_index=chunk_index,
                text=chunk_text,
                token_count=token_count,
                strategy="fixed"
            ))
            
            chunk_index += 1
    
    return chunks


def chunk_semantic(pages: List[Page], max_chunk_size: int = 600) -> List[Chunk]:
    """
    Paragraph-boundary semantic chunking using LangChain.
    
    Args:
        pages: List of Page objects from PDF extraction
        max_chunk_size: Maximum chunk size in tokens (default 600)
        
    Returns:
        List of Chunk objects
    """
    # LangChain splitter prioritizing paragraph boundaries
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=max_chunk_size * 4,  # Approximate: 1 token ≈ 4 chars
        chunk_overlap=0,  # No overlap for semantic chunks
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]  # Prioritize paragraphs
    )
    
    encoding = tiktoken.get_encoding("cl100k_base")
    chunks = []
    chunk_index = 0
    
    for page in pages:
        # Split text using LangChain
        text_chunks = splitter.split_text(page.text)
        
        for chunk_text in text_chunks:
            # Count actual tokens
            token_count = len(encoding.encode(chunk_text))
            
            # Skip very small chunks (< 80 tokens)
            if token_count < 80:
                continue
            
            chunks.append(Chunk(
                chunk_id=str(uuid.uuid4()),
                source_file=page.source_file,
                page_number=page.page_number,
                chunk_index=chunk_index,
                text=chunk_text,
                token_count=token_count,
                strategy="semantic"
            ))
            
            chunk_index += 1
    
    return chunks


def chunk(pages: List[Page], strategy: str, **kwargs) -> List[Chunk]:
    """Dispatcher - calls chunk_fixed or chunk_semantic based on strategy string"""
    if strategy == "fixed":
        return chunk_fixed(pages, **kwargs)
    elif strategy == "semantic":
        return chunk_semantic(pages, **kwargs)
    else:
        raise ValueError(f"Unknown chunking strategy: {strategy}")
