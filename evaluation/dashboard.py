"""Evaluation dashboard and metrics aggregation"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class QueryResult:
    query_id: str
    timestamp: str
    question: str
    answer: str
    retrieved_chunks: List
    source_document: str
    chunking_strategy: str
    latency_seconds: float
    evaluation: Optional[object] = None


def aggregate_metrics(query_results: List[QueryResult]) -> dict:
    """
    Aggregate evaluation metrics across multiple queries.
    
    Returns:
        Dictionary with mean, min, max for each metric
    """
    # TODO: Implement metrics aggregation
    pass
