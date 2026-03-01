"""PDF text extraction with PyMuPDF"""

from dataclasses import dataclass
from typing import List
import fitz  # PyMuPDF


class PDFPasswordProtectedError(Exception):
    """Raised when PDF requires a password"""
    pass


class PDFCorruptedError(Exception):
    """Raised when PDF file cannot be read"""
    pass


class PDFNoTextError(Exception):
    """Raised when no text is extractable from PDF"""
    pass


@dataclass
class Page:
    source_file: str
    page_number: int
    text: str
    char_count: int


def extract_pages(file_path: str) -> List[Page]:
    """
    Extract text from all pages of a PDF file.
    
    Args:
        file_path: Absolute path to PDF file
        
    Returns:
        List of Page objects, one per text-bearing page
        
    Raises:
        PDFPasswordProtectedError: If PDF requires a password
        PDFCorruptedError: If file cannot be read
        PDFNoTextError: If no text is extractable from any page
    """
    # TODO: Implement PDF extraction logic
    pass
