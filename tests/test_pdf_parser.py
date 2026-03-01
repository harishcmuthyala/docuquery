"""Tests for PDF parsing functionality"""

import pytest
from ingestion.pdf_parser import (
    extract_pages,
    PDFPasswordProtectedError,
    PDFCorruptedError,
    PDFNoTextError,
    _clean_text
)


def test_clean_text():
    """Test text cleaning function"""
    # Test null byte removal
    assert _clean_text("Hello\x00World") == "Hello World"
    
    # Test excessive whitespace normalization
    assert _clean_text("Hello    World") == "Hello World"
    
    # Test newline normalization
    assert _clean_text("Hello\n\n\n\nWorld") == "Hello\n\nWorld"
    
    # Test stripping
    assert _clean_text("  Hello World  ") == "Hello World"


def test_extract_pages_basic():
    """Test basic PDF extraction - requires a test PDF file"""
    # This test requires a sample PDF in tests/fixtures/
    # Uncomment when you have a test PDF
    pass
    # pages = extract_pages("tests/fixtures/sample.pdf")
    # assert len(pages) > 0
    # assert all(page.char_count >= 50 for page in pages)
    # assert all(page.page_number > 0 for page in pages)


def test_extract_pages_corrupted():
    """Test handling of corrupted PDF"""
    # This would require a corrupted test file
    pass


def test_extract_pages_password_protected():
    """Test handling of password-protected PDF"""
    # This would require a password-protected test file
    pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
