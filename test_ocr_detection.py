#!/usr/bin/env python3
"""Test OCR detection and extraction capabilities."""

import sys
sys.path.insert(0, 'src')

from utils.pdf_detector import detect_pdf_type, is_scanned_pdf
from utils.ocr_extractor import check_ocr_availability
from pathlib import Path

samples = [
    "data/input/GBL Sample.pdf",
    "data/input/GBL Sample 2.pdf",
    "data/input/GBL Sample 3.pdf",
    "data/input/GBL Sample 4.pdf",
    "data/input/GBL Sample 5.pdf",
    "data/input/GBL Sample 6.pdf",
    "data/input/GBL Sample 7.pdf",
    "data/input/GBL Sample 8.pdf",
    "data/input/GBL Sample 9.pdf",
    "data/input/GBL Sample 10.pdf",
]

print("\n" + "="*80)
print("PDF TYPE DETECTION TEST")
print("="*80)

# Check OCR availability
ocr_status = check_ocr_availability()
print(f"\nOCR Status:")
print(f"  Available: {ocr_status['ocr_available']}")
if not ocr_status['ocr_available']:
    print(f"  Missing packages: {', '.join(ocr_status['missing_packages'])}")
    print(f"\n  To enable OCR:")
    print(f"    1. Install Python packages: pip install pytesseract pdf2image Pillow")
    print(f"    2. Install Tesseract OCR:")
    print(f"       - macOS: brew install tesseract")
    print(f"       - Ubuntu/Debian: sudo apt-get install tesseract-ocr")
    print(f"       - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")

print("\n" + "="*80)
print("DETECTION RESULTS")
print("="*80)

text_based = []
scanned = []

for sample_path in samples:
    if not Path(sample_path).exists():
        print(f"\n⚠️  {Path(sample_path).name}: FILE NOT FOUND")
        continue

    pdf_type, metadata = detect_pdf_type(sample_path)

    sample_name = Path(sample_path).name
    status_icon = "📄" if pdf_type == "text-based" else "🖼️"

    print(f"\n{status_icon} {sample_name}")
    print(f"  Type: {pdf_type.upper()}")
    print(f"  Confidence: {metadata.get('confidence', 'unknown')}")
    print(f"  Text Length: {metadata.get('text_length', 0)} chars")
    print(f"  Avg Chars/Page: {metadata.get('avg_chars_per_page', 0):.0f}")
    print(f"  Pages: {metadata.get('page_count', 0)}")

    if pdf_type == 'text-based':
        text_based.append(sample_name)
        if metadata.get('gbl_detected'):
            print(f"  GBL Markers: ✓ Detected")
    else:
        scanned.append(sample_name)
        print(f"  → Requires OCR extraction")

# Summary
print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"\nText-based PDFs ({len(text_based)}):")
for name in text_based:
    print(f"  ✓ {name}")

print(f"\nScanned PDFs ({len(scanned)}):")
for name in scanned:
    print(f"  🖼️  {name}")

print(f"\nTotal: {len(text_based) + len(scanned)} samples")
print(f"  - Text-based: {len(text_based)} ({len(text_based)/(len(text_based)+len(scanned))*100:.0f}%)")
print(f"  - Scanned: {len(scanned)} ({len(scanned)/(len(text_based)+len(scanned))*100:.0f}%)")

print("\n" + "="*80)
