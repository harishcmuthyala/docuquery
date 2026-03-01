"""Embedding generation using sentence-transformers"""

from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from ingestion.chunker import Chunk


def load_model() -> SentenceTransformer:
    """Load and return the embedding model. Cache in session state."""
    # TODO: Implement model loading
    pass


def embed_chunks(chunks: List[Chunk], model: SentenceTransformer) -> np.ndarray:
    """
    Embed list of chunks. Returns array of shape (len(chunks), 384).
    """
    # TODO: Implement chunk embedding
    pass


def embed_query(query: str, model: SentenceTransformer) -> np.ndarray:
    """
    Embed a single query string. Returns array of shape (384,).
    """
    # TODO: Implement query embedding
    pass
