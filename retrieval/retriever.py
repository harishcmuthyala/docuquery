"""Top-k similarity retrieval"""

from typing import List
from dataclasses import dataclass
import numpy as np
from ingestion.chunker import Chunk


@dataclass
class RetrievedChunk:
    chunk: Chunk
    similarity_score: float
    rank: int


def query(collection, query_embedding: np.ndarray, top_k: int = 5) -> List[RetrievedChunk]:
    """Query collection and return ranked RetrievedChunk list."""
    # TODO: Implement retrieval logic
    pass
