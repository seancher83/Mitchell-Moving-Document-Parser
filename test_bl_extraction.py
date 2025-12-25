#!/usr/bin/env python3
"""Test B/L number extraction with updated pattern."""

import sys
sys.path.insert(0, 'src')

from PyPDF2 import PdfReader
from utils.text_utils import extract_bl_number

# Test with GBL Sample
pdf_path = "data/input/GBL Sample.pdf"

print("Testing B/L Number Extraction")
print("=" * 50)

reader = PdfReader(pdf_path)
full_text = ""
for page in reader.pages:
    full_text += page.extract_text()

bl_number = extract_bl_number(full_text)

print(f"File: {pdf_path}")
print(f"Extracted B/L Number: {bl_number}")
print(f"Expected: LKNQ0540823")
print(f"Match: {'✓ YES' if bl_number == 'LKNQ0540823' else '✗ NO'}")
print("=" * 50)
