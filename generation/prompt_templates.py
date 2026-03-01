"""Prompt templates for answer generation"""

SYSTEM_PROMPT = """You are a precise document assistant. Answer the user's question using ONLY the 
information provided in the context below. Do not use any external knowledge.
If the answer is not in the context, say "The document does not contain information 
about this topic." Do not speculate or infer beyond what is explicitly stated."""


def build_prompt(question: str, retrieved_chunks) -> str:
    """
    Construct full prompt with system message, context chunks, and question.
    
    Args:
        question: User's question
        retrieved_chunks: List of RetrievedChunk objects
        
    Returns:
        Formatted prompt string
    """
    # TODO: Implement prompt construction
    pass
