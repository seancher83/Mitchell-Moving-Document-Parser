#!/usr/bin/env python3
"""Test extraction functions on parser text."""

import sys
sys.path.insert(0, 'src')

from parsers.gbl_parser import GBLParser
from utils.text_utils import (
    extract_bl_number,
    extract_scac_code,
    extract_service_code_gbl,
    extract_gbl_dates,
    extract_zip_codes,
    extract_tariff_rates
)

print("\n" + "="*70)
print("TESTING FUNCTIONS ON PARSER TEXT")
print("="*70)

# Get text the way parser extracts it
parser = GBLParser("data/input/GBL Sample.pdf")
result = parser.parse()
parser_text = result['raw_text']

print("\nTesting extraction functions on parser's full_text:")
print("-"*70)

print(f"extract_bl_number(): {extract_bl_number(parser_text)}")
print(f"extract_scac_code(): {extract_scac_code(parser_text)}")
print(f"extract_service_code_gbl(): {extract_service_code_gbl(parser_text)}")

dates = extract_gbl_dates(parser_text)
print(f"\nextract_gbl_dates():")
for key, value in dates.items():
    if value:
        print(f"  {key}: {value}")

zips = extract_zip_codes(parser_text)
print(f"\nextract_zip_codes():")
for key, value in zips.items():
    print(f"  {key}: {value}")

rates = extract_tariff_rates(parser_text)
print(f"\nextract_tariff_rates():")
for key, value in rates.items():
    print(f"  {key}: {value}")

print("\n" + "="*70)

# Show the line with SCAC code
print("\nLooking for SCAC code pattern in parser text:")
print("-"*70)
import re
# Find lines with SDDA
for line in parser_text.split('\n'):
    if 'SDDA' in line or 'SCAC' in line:
        print(repr(line))
