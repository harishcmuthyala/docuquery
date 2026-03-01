"""Text chunking strategies: fixed-size and semantic"""

from typing import List
from dataclasses import dataclass
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
    """Fixed-size token chunking with overlap"""
    # TODO: Implement fixed-size chunking
    pass


def chunk_semantic(pages: List[Page], max_chunk_size: int = 600) -> List[Chunk]:
    """Paragraph-boundary semantic chunking"""
    # TODO: Implement semantic chunking
    pass


def chunk(pages: List[Page], strategy: str, **kwargs) -> List[Chunk]:
    """Dispatcher - calls chunk_fixed or chunk_semantic based on strategy string"""
    if strategy == "fixed":
        return chunk_fixed(pages, **kwargs)
    elif strategy == "semantic":
        return chunk_semantic(pages, **kwargs)
    else:
        raise ValueError(f"Unknown chunking strategy: {strategy}")
