#!/usr/bin/env python3
"""Show actual text from Sample 3."""

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
print("SAMPLE 3 - ACTUAL EXTRACTED TEXT")
print("="*80)

# Show text around where dates should be
print("\nSearching for date sequences:")
all_dates = re.findall(r'\d{8}', text)
print(f"All 8-digit dates found: {all_dates}")

# Show context around the three dates that should be packing/pickup/delivery
target_dates = ['20251201', '20251223']
for date in target_dates:
    idx = text.find(date)
    if idx != -1:
        start = max(0, idx - 150)
        end = min(len(text), idx + 150)
        context = text[start:end]
        print(f"\nContext around {date}:")
        print("-"*80)
        print(context)
        print("-"*80)

# Look for lines with "KKFA" or other B/L-like codes
print("\n" + "="*80)
print("Lines with 4-letter codes:")
for line in text.split('\n'):
    if re.search(r'\b[A-Z]{4}\b', line):
        codes = re.findall(r'\b([A-Z]{4})\b', line)
        if any(len(set(c)) > 1 for c in codes):  # Not like "AAAA"
            print(f"  {repr(line)}")

# Show lines around "United States Navy"
print("\n" + "="*80)
print("Context around 'United States Navy':")
idx = text.find('United States Navy')
if idx != -1:
    start = max(0, idx - 100)
    end = min(len(text), idx + 300)
    context = text[start:end]
    print(context)
