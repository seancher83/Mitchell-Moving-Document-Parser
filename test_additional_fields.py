#!/usr/bin/env python3
"""Test extraction of additional fields."""

import sys
sys.path.insert(0, 'src')

from PyPDF2 import PdfReader
from utils.text_utils import (
    extract_scac_code,
    extract_service_code_gbl,
    extract_zip_codes,
    extract_tariff_rates
)

print("\n" + "="*70)
print("TESTING ADDITIONAL FIELD EXTRACTION - GBL Sample 1")
print("="*70)

sample = 'data/input/GBL Sample.pdf'
reader = PdfReader(sample)
text = ""
for page in reader.pages:
    text += page.extract_text()

# Test SCAC
scac = extract_scac_code(text)
print(f"\nSCAC Code:           {scac}")
print(f"  Expected: SDDA     {'✓' if scac == 'SDDA' else '✗'}")

# Test Service Code
service_code = extract_service_code_gbl(text)
print(f"\nService Code:        {service_code}")
print(f"  Expected: D        {'✓' if service_code == 'D' else '✗'}")

# Test Zip Codes
zips = extract_zip_codes(text)
print(f"\nOrigin Zip:          {zips['origin_zip']}")
print(f"  Expected: 92507    {'✓' if zips['origin_zip'] == '92507' else '✗'}")

print(f"\nDestination Zip:     {zips['destination_zip']}")
print(f"  Expected: 98438    {'✓' if zips['destination_zip'] == '98438' else '✗'}")

# Test Tariff Rates
rates = extract_tariff_rates(text)
print(f"\nTariff LH Rate:      {rates['lh_rate']}")
print(f"  Expected: 67%      {'✓' if rates['lh_rate'] == '67%' else '✗'}")

print(f"\nTariff SIT Rate:     {rates['sit_rate']}")
print(f"  Expected: 63%      {'✓' if rates['sit_rate'] == '63%' else '✗'}")

print("\n" + "="*70)

# Summary
all_correct = (
    scac == 'SDDA' and
    service_code == 'D' and
    zips['origin_zip'] == '92507' and
    zips['destination_zip'] == '98438' and
    rates['lh_rate'] == '67%' and
    rates['sit_rate'] == '63%'
)

if all_correct:
    print("✓ ALL FIELDS EXTRACTED CORRECTLY!")
else:
    print("✗ Some fields need adjustment")

print("="*70 + "\n")
