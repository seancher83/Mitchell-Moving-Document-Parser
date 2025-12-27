#!/usr/bin/env python3
"""Debug samples with 0% extraction."""

import sys
sys.path.insert(0, 'src')

from PyPDF2 import PdfReader

samples = [
    "data/input/GBL Sample 8.pdf",
    "data/input/GBL Sample 10.pdf"
]

for sample_path in samples:
    print("\n" + "="*70)
    print(f"DEBUGGING: {sample_path}")
    print("="*70)

    try:
        reader = PdfReader(sample_path)
        print(f"Number of pages: {len(reader.pages)}")

        text = ""
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            print(f"\nPage {i+1} text length: {len(page_text)} characters")
            text += page_text

        print(f"\nTotal text length: {len(text)} characters")
        print(f"\nFirst 1000 characters:")
        print("-"*70)
        print(text[:1000])
        print("-"*70)

        # Look for key markers
        print(f"\nKey markers found:")
        print(f"  'B/L' found: {'B/L' in text}")
        print(f"  'BILL' found: {'BILL' in text}")
        print(f"  'LADING' found: {'LADING' in text}")
        print(f"  'SCAC' found: {'SCAC' in text}")
        print(f"  '4 letters + 7 digits' pattern: ", end="")

        import re
        match = re.search(r'\b([A-Z]{4}\d{7})\b', text)
        if match:
            print(f"Found: {match.group(1)}")
        else:
            print("NOT FOUND")

    except Exception as e:
        print(f"ERROR: {e}")
