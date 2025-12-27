#!/usr/bin/env python3
"""Analyze zip code patterns in GBL samples."""

import sys
import re
sys.path.insert(0, 'src')

from PyPDF2 import PdfReader
from pathlib import Path

samples = [
    ("Sample 1", "data/input/GBL Sample.pdf", "92507", "98438"),
    ("Sample 2", "data/input/GBL Sample 2.pdf", "79934", "98433"),
    ("Sample 4", "data/input/GBL Sample 4.pdf", "?", "?"),
    ("Sample 5", "data/input/GBL Sample 5.pdf", "?", "98433"),
    ("Sample 6", "data/input/GBL Sample 6.pdf", "?", "98433"),
]

print("\n" + "="*80)
print("ZIP CODE PATTERN ANALYSIS")
print("="*80)

for sample_name, sample_path, expected_origin, expected_dest in samples:
    if not Path(sample_path).exists():
        continue

    print(f"\n{'='*80}")
    print(f"{sample_name}")
    print(f"Expected: Origin={expected_origin}, Dest={expected_dest}")
    print("="*80)

    # Extract text
    reader = PdfReader(sample_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    # Find all 5-digit numbers that could be zip codes
    zip_pattern = r'\b(\d{5})\b'
    zips_found = re.findall(zip_pattern, text)
    print(f"\nAll 5-digit numbers found ({len(zips_found)}): {zips_found}")

    # Find context around each zip code
    for zip_code in set(zips_found):
        # Find the position and show surrounding text
        pos = text.find(zip_code)
        if pos != -1:
            start = max(0, pos - 80)
            end = min(len(text), pos + 85)
            context = text[start:end].replace('\n', ' | ')
            print(f"\n  {zip_code}: ...{context}...")

    # Look for specific markers
    print(f"\nMarkers found:")
    print(f"  'FROM:' found: {'FROM:' in text}")
    print(f"  'TO:' found: {'TO:' in text}")
    print(f"  'ORIGIN' found: {'ORIGIN' in text}")
    print(f"  'DESTINATION' found: {'DESTINATION' in text}")
    print(f"  'SHIP FROM' found: {'SHIP FROM' in text}")
    print(f"  'SHIP TO' found: {'SHIP TO' in text}")
