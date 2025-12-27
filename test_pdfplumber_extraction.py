#!/usr/bin/env python3
"""Test pdfplumber on failed samples."""

import pdfplumber

samples = [
    "data/input/GBL Sample 8.pdf",
    "data/input/GBL Sample 10.pdf"
]

for sample_path in samples:
    print("\n" + "="*70)
    print(f"TESTING PDFPLUMBER: {sample_path}")
    print("="*70)

    try:
        with pdfplumber.open(sample_path) as pdf:
            print(f"Number of pages: {len(pdf.pages)}")

            text = ""
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    print(f"\nPage {i+1} text length: {len(page_text)} characters")
                    text += page_text
                else:
                    print(f"\nPage {i+1}: NO TEXT EXTRACTED")

            print(f"\nTotal text length: {len(text)} characters")

            if text:
                print(f"\nFirst 1000 characters:")
                print("-"*70)
                print(text[:1000])
                print("-"*70)

                # Look for key markers
                print(f"\nKey markers found:")
                print(f"  'B/L' found: {'B/L' in text}")
                print(f"  'SCAC' found: {'SCAC' in text}")

                import re
                match = re.search(r'\b([A-Z]{4}\d{7})\b', text)
                if match:
                    print(f"  B/L Number: {match.group(1)}")
            else:
                print("\n⚠️ NO TEXT EXTRACTED - These PDFs are likely scanned images")
                print("   Solution: These require OCR (Optical Character Recognition)")

    except Exception as e:
        print(f"ERROR: {e}")
