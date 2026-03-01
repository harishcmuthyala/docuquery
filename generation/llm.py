"""Groq LLM API integration"""

from typing import Tuple, List


class GroqTimeoutError(Exception):
    """Raised when Groq API call exceeds timeout"""
    pass


class GroqRateLimitError(Exception):
    """Raised when Groq rate limit is hit"""
    pass


class GroqAuthError(Exception):
    """Raised when API key is invalid"""
    pass


def generate_answer(question: str, retrieved_chunks: List) -> Tuple[str, float]:
    """
    Generate answer from question and retrieved context via Groq API.
    
    Returns:
        Tuple of (answer_text, latency_seconds)
        
    Raises:
        GroqTimeoutError: If API call exceeds 15 seconds
        GroqRateLimitError: If rate limit is hit
        GroqAuthError: If API key is invalid
    """
    # TODO: Implement LLM call
    pass
