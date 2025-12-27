"""PDF Document Type Detection."""

from typing import Tuple
from PyPDF2 import PdfReader
import re


def detect_pdf_type(pdf_path: str) -> Tuple[str, dict]:
    """
    Detect whether a PDF is a scanned image or text-based document.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Tuple of (pdf_type, metadata) where pdf_type is 'scanned' or 'text-based'
        metadata includes: text_length, has_images, page_count
    """
    metadata = {
        'text_length': 0,
        'has_images': False,
        'page_count': 0,
        'avg_chars_per_page': 0,
        'confidence': 'high'
    }

    try:
        reader = PdfReader(pdf_path)
        metadata['page_count'] = len(reader.pages)

        # Extract text from all pages
        total_text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                total_text += page_text

        metadata['text_length'] = len(total_text)
        metadata['avg_chars_per_page'] = len(total_text) / len(reader.pages) if reader.pages else 0

        # Check for images in the PDF
        for page in reader.pages:
            if '/XObject' in page.get('/Resources', {}):
                xobjects = page['/Resources']['/XObject'].get_object()
                for obj in xobjects:
                    if xobjects[obj]['/Subtype'] == '/Image':
                        metadata['has_images'] = True
                        break

        # Decision logic:
        # - If very little or no text extracted, it's likely a scanned image
        # - Threshold: < 100 characters per page suggests scanned image
        # - GBL documents typically have 2000-5000 characters when text-based

        if metadata['avg_chars_per_page'] < 100:
            # Very little text - definitely scanned
            pdf_type = 'scanned'
            metadata['confidence'] = 'high'
        elif metadata['avg_chars_per_page'] < 500:
            # Some text but not much - likely scanned with poor OCR or partial text layer
            pdf_type = 'scanned'
            metadata['confidence'] = 'medium'
        else:
            # Sufficient text - text-based PDF
            pdf_type = 'text-based'
            metadata['confidence'] = 'high'

            # Additional check: look for GBL-specific markers
            if any(marker in total_text for marker in ['BILL OF LADING', 'B/L NO', 'SCAC', 'JPPSO']):
                metadata['confidence'] = 'very-high'
                metadata['gbl_detected'] = True
            else:
                metadata['gbl_detected'] = False

        return pdf_type, metadata

    except Exception as e:
        return 'unknown', {'error': str(e)}


def is_scanned_pdf(pdf_path: str) -> bool:
    """
    Simple boolean check if PDF is scanned.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        True if scanned, False if text-based
    """
    pdf_type, _ = detect_pdf_type(pdf_path)
    return pdf_type == 'scanned'
