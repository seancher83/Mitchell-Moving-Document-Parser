#!/usr/bin/env python3
"""Compare text extraction between pdfplumber and PyPDF2."""

from PyPDF2 import PdfReader
import pdfplumber

file_path = "data/input/GBL Sample.pdf"

print("\n" + "="*70)
print("COMPARING PDF LIBRARY TEXT EXTRACTION")
print("="*70)

# PyPDF2 extraction
print("\nPyPDF2 Extraction:")
print("-"*70)
reader = PdfReader(file_path)
pypdf2_text = reader.pages[0].extract_text()
print(f"Length: {len(pypdf2_text)}")
print("\nFirst 600 chars:")
print(pypdf2_text[:600])

# pdfplumber extraction
print("\n" + "="*70)
print("pdfplumber Extraction:")
print("-"*70)
with pdfplumber.open(file_path) as pdf:
    pdfplumber_text = pdf.pages[0].extract_text()
print(f"Length: {len(pdfplumber_text)}")
print("\nFirst 600 chars:")
print(pdfplumber_text[:600])

print("\n" + "="*70)
print(f"Texts are identical: {pypdf2_text == pdfplumber_text}")
print("="*70)

# Test extraction functions on both
print("\nTesting extraction functions on both texts:")
print("="*70)

import sys
sys.path.insert(0, 'src')
from utils.text_utils import extract_scac_code, extract_service_code_gbl, extract_gbl_dates

print("\nOn PyPDF2 text:")
print(f"  SCAC: {extract_scac_code(pypdf2_text)}")
print(f"  Service Code: {extract_service_code_gbl(pypdf2_text)}")
dates = extract_gbl_dates(pypdf2_text)
print(f"  Packing Date: {dates['requested_packing_date']}")
print(f"  Date B/L Printed: {dates['date_bl_printed']}")

print("\nOn pdfplumber text:")
print(f"  SCAC: {extract_scac_code(pdfplumber_text)}")
print(f"  Service Code: {extract_service_code_gbl(pdfplumber_text)}")
dates = extract_gbl_dates(pdfplumber_text)
print(f"  Packing Date: {dates['requested_packing_date']}")
print(f"  Date B/L Printed: {dates['date_bl_printed']}")
