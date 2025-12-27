#!/usr/bin/env python3
"""Test specific patterns on Sample 3."""

import sys
import re
sys.path.insert(0, 'src')

from PyPDF2 import PdfReader
from utils.text_utils import extract_service_code_gbl, extract_gbl_dates

sample_path = "data/input/GBL Sample 3.pdf"

reader = PdfReader(sample_path)
text = ""
for page in reader.pages:
    text += page.extract_text()

print("\n" + "="*80)
print("SAMPLE 3 - SPECIFIC PATTERN TESTING")
print("="*80)

# Test service code extraction
print("\nService Code Extraction:")
service_code = extract_service_code_gbl(text)
print(f"  Result: {service_code}")

# Manually test the pattern
pattern_pipe = r'\|\s*([A-Z])\s*\|\s*\d+/\d+'
match = re.search(pattern_pipe, text)
if match:
    print(f"  Manual pattern match: {match.group(1)}")
    print(f"  Full match: {match.group(0)}")
else:
    print("  Manual pattern: NO MATCH")

# Show context where "| D |" should be
for line in text.split('\n'):
    if '|' in line and 'D' in line:
        print(f"  Line with | and D: {repr(line)}")

# Test date extraction
print("\n" + "="*80)
print("Date Extraction:")
dates = extract_gbl_dates(text)
for key, value in dates.items():
    print(f"  {key}: {value}")

# Manually test the three-dates pattern
print("\n" + "="*80)
print("Manual Three-Dates Pattern Test:")
pattern_three_dates = r'[A-Z]{4}\s*\|\s*(\d{8})\s*\|\s*(\d{8})\s*\|\s*(\d{8})'
match = re.search(pattern_three_dates, text)
if match:
    print(f"  FOUND!")
    print(f"  Packing: {match.group(1)}")
    print(f"  Pickup: {match.group(2)}")
    print(f"  Delivery: {match.group(3)}")
    print(f"  Full match: {match.group(0)}")
else:
    print("  NOT FOUND")
    # Show lines with potential date patterns
    print("\n  Lines with '|' and 8 digits:")
    for line in text.split('\n'):
        if '|' in line and re.search(r'\d{8}', line):
            print(f"    {repr(line)}")

# Test B/L printed date pattern
print("\n" + "="*80)
print("B/L Printed Date Pattern Test:")
pattern_bl_date = r'(\d{8})[^\d]{0,30}\d+/\d+'
match = re.search(pattern_bl_date, text)
if match:
    print(f"  FOUND: {match.group(1)}")
    print(f"  Full match: {match.group(0)}")
else:
    print("  NOT FOUND")
    # Show lines with fraction patterns
    print("\n  Lines with 'x/y' pattern:")
    for line in text.split('\n'):
        if re.search(r'\d+/\d+', line):
            print(f"    {repr(line)}")
