#!/usr/bin/env python3
"""Compare text extraction methods."""

import sys
sys.path.insert(0, 'src')

from PyPDF2 import PdfReader
from parsers.gbl_parser import GBLParser

print("\n" + "="*70)
print("COMPARING TEXT EXTRACTION METHODS")
print("="*70)

# Method 1: Direct PyPDF2
reader = PdfReader("data/input/GBL Sample.pdf")
direct_text = ""
for page in reader.pages:
    direct_text += page.extract_text()

# Method 2: Through GBLParser
parser = GBLParser("data/input/GBL Sample.pdf")
result = parser.parse()
parser_text = result.get('raw_text', '')

print(f"\nDirect text length: {len(direct_text)}")
print(f"Parser text length: {len(parser_text)}")
print(f"Texts are identical: {direct_text == parser_text}")

# Show first 500 chars of each
print("\n" + "-"*70)
print("First 500 chars of direct text:")
print("-"*70)
print(direct_text[:500])

print("\n" + "-"*70)
print("First 500 chars of parser text:")
print("-"*70)
print(parser_text[:500])

# Check if the parser text includes page markers
print("\n" + "-"*70)
print("Parser text has page markers:", "--- Page" in parser_text)
print("Direct text has page markers:", "--- Page" in direct_text)
print("-"*70)
