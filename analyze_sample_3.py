#!/usr/bin/env python3
"""Analyze Sample 3 to improve extraction."""

import sys
import re
sys.path.insert(0, 'src')

from PyPDF2 import PdfReader

sample_path = "data/input/GBL Sample 3.pdf"

reader = PdfReader(sample_path)
text = ""
for page in reader.pages:
    text += page.extract_text()

print("\n" + "="*80)
print("SAMPLE 3 TEXT ANALYSIS")
print("="*80)

print(f"\nText length: {len(text)} characters")

# Show first 2000 characters
print("\nFirst 2000 characters:")
print("-"*80)
print(text[:2000])
print("-"*80)

# Look for service code markers
print("\n" + "="*80)
print("SERVICE CODE ANALYSIS")
print("="*80)
print(f"'SERVICE CODE' found: {'SERVICE CODE' in text}")
print(f"'SERVICE' found: {'SERVICE' in text}")
print(f"'CODE' found: {'CODE' in text}")

# Look for lines with 'SERVICE'
print("\nLines containing 'SERVICE':")
for line in text.split('\n'):
    if 'SERVICE' in line.upper():
        print(f"  {repr(line)}")

# Look for date markers
print("\n" + "="*80)
print("DATE MARKERS ANALYSIS")
print("="*80)
print(f"'ORIGINAL' found: {'ORIGINAL' in text}")
print(f"'LOT' found: {'LOT' in text}")
print(f"'WOD' found: {'WOD' in text}")
print(f"'WD' found: {'WD' in text}")

# Find all 8-digit sequences (potential dates)
dates = re.findall(r'\b(\d{8})\b', text)
print(f"\nAll 8-digit sequences found ({len(dates)}): {dates}")

# Show context around each date
for date in set(dates):
    pos = text.find(date)
    if pos != -1:
        start = max(0, pos - 60)
        end = min(len(text), pos + 68)
        context = text[start:end].replace('\n', ' | ')
        print(f"\n  {date}: ...{context}...")

# Look for packing/pickup/delivery markers
print("\n" + "="*80)
print("PACKING/PICKUP/DELIVERY MARKERS")
print("="*80)
print(f"'PACKING' found: {'PACKING' in text}")
print(f"'PICKUP' found: {'PICKUP' in text}")
print(f"'DELIVERY' found: {'DELIVERY' in text}")
print(f"'REQUESTED' found: {'REQUESTED' in text}")
print(f"'REQUIRED' found: {'REQUIRED' in text}")

# Show lines with these keywords
print("\nLines with date-related keywords:")
for line in text.split('\n'):
    if any(kw in line.upper() for kw in ['PACK', 'PICKUP', 'DELIVERY', 'REQUESTED', 'REQUIRED']):
        print(f"  {repr(line)}")
