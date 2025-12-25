#!/usr/bin/env python3
"""Debug script to trace parser execution."""

import sys
sys.path.insert(0, 'src')

from PyPDF2 import PdfReader
from parsers.gbl_parser import GBLParser

print("\n" + "="*70)
print("DEBUGGING PARSER EXECUTION")
print("="*70)

# Parse using GBLParser class
parser = GBLParser("data/input/GBL Sample.pdf")
result = parser.parse()

print("\nHeader Data:")
print(f"  gbl_number: {result['header']['gbl_number']}")
print(f"  date_bl_printed: {result['header']['date_bl_printed']}")
print(f"  scac_code: {result['header']['scac_code']}")
print(f"  service_code: {result['header']['service_code']}")

print("\nShipment Data:")
print(f"  origin_zip: {result['shipment']['origin_zip']}")
print(f"  destination_zip: {result['shipment']['destination_zip']}")
print(f"  requested_packing_date: {result['shipment']['requested_packing_date']}")
print(f"  requested_pickup_date: {result['shipment']['requested_pickup_date']}")
print(f"  required_delivery_date: {result['shipment']['required_delivery_date']}")
print(f"  date_of_order: {result['shipment']['date_of_order']}")
print(f"  tariff_lh_rate: {result['shipment']['tariff_lh_rate']}")
print(f"  tariff_sit_rate: {result['shipment']['tariff_sit_rate']}")

print("\n" + "="*70)

# Now test extraction functions directly on the same text
print("\nTesting extraction functions directly on same text:")
print("="*70)

reader = PdfReader("data/input/GBL Sample.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text()

from utils.text_utils import (
    extract_bl_number,
    extract_scac_code,
    extract_service_code_gbl,
    extract_gbl_dates,
    extract_zip_codes,
    extract_tariff_rates
)

print(f"\nextract_bl_number(): {extract_bl_number(text)}")
print(f"extract_scac_code(): {extract_scac_code(text)}")
print(f"extract_service_code_gbl(): {extract_service_code_gbl(text)}")

dates = extract_gbl_dates(text)
print(f"\nextract_gbl_dates():")
for key, value in dates.items():
    print(f"  {key}: {value}")

zips = extract_zip_codes(text)
print(f"\nextract_zip_codes():")
for key, value in zips.items():
    print(f"  {key}: {value}")

rates = extract_tariff_rates(text)
print(f"\nextract_tariff_rates():")
for key, value in rates.items():
    print(f"  {key}: {value}")

print("\n" + "="*70)
