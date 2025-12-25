#!/usr/bin/env python3
"""Simple test script for GBL parser using PyPDF2."""

import sys
import json
from PyPDF2 import PdfReader

# Test reading the PDF
pdf_path = "data/input/GBL Sample.pdf"

print("Testing PDF extraction with PyPDF2...")
print("=" * 50)

try:
    reader = PdfReader(pdf_path)
    print(f"Number of pages: {len(reader.pages)}")

    full_text = ""
    for page_num, page in enumerate(reader.pages, 1):
        text = page.extract_text()
        print(f"\n--- Page {page_num} ---")
        print(f"Extracted {len(text)} characters")
        full_text += f"\n--- Page {page_num} ---\n{text}"

    # Test some basic extractions
    import re

    # Extract B/L number
    bl_match = re.search(r'B/L\s*NO\.?\s*([A-Z0-9]+)', full_text)
    if bl_match:
        print(f"\n✓ B/L Number found: {bl_match.group(1)}")

    # Extract SCAC
    scac_match = re.search(r'SCAC\s*[:.]?\s*([A-Z]{2,4})', full_text)
    if scac_match:
        print(f"✓ SCAC Code found: {scac_match.group(1)}")

    # Extract property owner name
    name_match = re.search(r"BLYTHE,\s*NICHOLAS", full_text)
    if name_match:
        print(f"✓ Property owner found: {name_match.group(0)}")

    # Save extracted text for review
    with open("data/output/extracted_text.txt", "w") as f:
        f.write(full_text)
    print(f"\n✓ Full extracted text saved to: data/output/extracted_text.txt")

    print("\n" + "=" * 50)
    print("PDF extraction test completed successfully!")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
