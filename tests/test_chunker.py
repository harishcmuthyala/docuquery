"""Tests for chunking functionality"""

import pytest
from ingestion.chunker import chunk_fixed, chunk_semantic, chunk
from ingestion.pdf_parser import Page


def test_chunk_fixed_basic():
    """Test fixed-size chunking with simple text"""
    pages = [
        Page(
            source_file="test.pdf",
            page_number=1,
            text="This is a test document. " * 100,  # Long enough to create multiple chunks
            char_count=2500
        )
    ]
    
    chunks = chunk_fixed(pages, chunk_size=500, overlap=50)
    
    assert len(chunks) > 0
    assert all(chunk.strategy == "fixed" for chunk in chunks)
    assert all(chunk.source_file == "test.pdf" for chunk in chunks)
    # Token counts should be reasonable (not exact due to char approximation)
    assert all(chunk.token_count >= 100 for chunk in chunks)


def test_chunk_fixed_minimum_size():
    """Test that chunks below minimum size are discarded"""
    pages = [
        Page(
            source_file="test.pdf",
            page_number=1,
            text="Short text.",
            char_count=11
        )
    ]
    
    chunks = chunk_fixed(pages, chunk_size=500, overlap=50)
    
    # Very short text should be filtered out
    assert len(chunks) == 0


def test_chunk_semantic_basic():
    """Test semantic chunking with paragraph boundaries"""
    text = """This is the first paragraph. It has multiple sentences.

This is the second paragraph. It also has content.

This is the third paragraph."""
    
    pages = [
        Page(
            source_file="test.pdf",
            page_number=1,
            text=text,
            char_count=len(text)
        )
    ]
    
    chunks = chunk_semantic(pages, max_chunk_size=600)
    
    assert len(chunks) > 0
    assert all(chunk.strategy == "semantic" for chunk in chunks)
    # Chunks should respect token limits reasonably
    assert all(chunk.token_count >= 80 for chunk in chunks)


def test_chunk_dispatcher():
    """Test chunk dispatcher function"""
    pages = [
        Page(
            source_file="test.pdf",
            page_number=1,
            text="Test content " * 50,
            char_count=650
        )
    ]
    
    fixed_chunks = chunk(pages, strategy="fixed")
    assert all(c.strategy == "fixed" for c in fixed_chunks)
    
    semantic_chunks = chunk(pages, strategy="semantic")
    assert all(c.strategy == "semantic" for c in semantic_chunks)
    
    # Test invalid strategy
    with pytest.raises(ValueError):
        chunk(pages, strategy="invalid")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
