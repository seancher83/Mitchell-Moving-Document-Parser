#!/usr/bin/env python3
"""Check which PDF library is being used."""

import sys
sys.path.insert(0, 'src')

try:
    import pdfplumber
    print("pdfplumber is available")
    PDF_LIBRARY = "pdfplumber"
except ImportError:
    print("pdfplumber is NOT available")
    try:
        from PyPDF2 import PdfReader
        print("PyPDF2 is available - will be used as fallback")
        PDF_LIBRARY = "pypdf2"
    except ImportError:
        print("Neither pdfplumber nor PyPDF2 is available!")
        PDF_LIBRARY = None

print(f"\nPDF Library that will be used: {PDF_LIBRARY}")

# Check what the parser thinks
from parsers import gbl_parser
print(f"Parser's PDF_LIBRARY setting: {gbl_parser.PDF_LIBRARY}")
