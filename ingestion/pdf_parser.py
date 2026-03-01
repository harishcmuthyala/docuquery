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
    pages = []
    
    try:
        doc = fitz.open(file_path)
    except fitz.FileDataError as e:
        if "password" in str(e).lower():
            raise PDFPasswordProtectedError("This PDF is password protected and cannot be processed")
        raise PDFCorruptedError("Could not read this file. Please check the file is a valid PDF")
    except Exception:
        raise PDFCorruptedError("Could not read this file. Please check the file is a valid PDF")
    
    # Check if document is encrypted
    if doc.is_encrypted:
        doc.close()
        raise PDFPasswordProtectedError("This PDF is password protected and cannot be processed")
    
    # Extract filename from path
    import os
    source_filename = os.path.basename(file_path)
    
    # Extract text from each page
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        
        # Clean text
        text = _clean_text(text)
        
        # Skip image-only pages (less than 50 characters)
        if len(text) < 50:
            continue
        
        pages.append(Page(
            source_file=source_filename,
            page_number=page_num + 1,  # 1-indexed
            text=text,
            char_count=len(text)
        ))
    
    doc.close()
    
    # Check if any text was extracted
    if not pages:
        raise PDFNoTextError("No text found in this PDF. OCR is not currently supported")
    
    return pages


def _clean_text(text: str) -> str:
    """
    Clean extracted text by removing null bytes, excessive whitespace,
    and non-printable characters.
    """
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Remove other non-printable characters except newlines and tabs
    text = ''.join(char for char in text if char.isprintable() or char in '\n\t')
    
    # Normalize whitespace - replace multiple spaces with single space
    import re
    text = re.sub(r' +', ' ', text)
    
    # Normalize newlines - replace 3+ newlines with 2
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text
