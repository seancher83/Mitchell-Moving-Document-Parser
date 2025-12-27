#!/usr/bin/env python3
"""Debug OCR SCAC extraction."""

import sys
sys.path.insert(0, 'src')

from utils.ocr_extractor import GBLFormExtractor

samples = [
    ("Sample 8", "data/input/GBL Sample 8.pdf", "NFWD"),
    ("Sample 10", "data/input/GBL Sample 10.pdf", "NFWD"),
]

print("\n" + "="*80)
print("OCR SCAC EXTRACTION DEBUG")
print("="*80)

for sample_name, sample_path, expected_scac in samples:
    print(f"\n{sample_name}: {sample_path}")
    print(f"Expected SCAC: {expected_scac}")
    print("-"*80)

    extractor = GBLFormExtractor(sample_path)
    result = extractor.extract_with_ocr(dpi=300, enhance=True)

    if result.get('success'):
        ocr_text = extractor.full_text

        print(f"\nOCR SCAC Extracted: {result.get('scac', 'NULL')}")
        print(f"✓ Correct: {result.get('scac') == expected_scac}")

        # Show lines containing potential SCAC codes
        print(f"\nLines containing 'SCAC' or 4-letter codes:")
        for i, line in enumerate(ocr_text.split('\n')[:100], 1):
            if 'SCAC' in line or 'NFWD' in line or (len(line.strip()) == 4 and line.strip().isupper()):
                print(f"  Line {i}: {repr(line)}")

        # Show first 1000 chars of OCR text
        print(f"\nFirst 1000 chars of OCR text:")
        print("-"*80)
        print(ocr_text[:1000])
        print("-"*80)
    else:
        print(f"OCR failed: {result.get('error')}")

print("\n" + "="*80)
