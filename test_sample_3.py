#!/usr/bin/env python3
"""Test extraction on GBL Sample 3."""

import sys
sys.path.insert(0, 'src')

from PyPDF2 import PdfReader
from utils.text_utils import (
    extract_bl_number,
    extract_scac_code,
    extract_service_code_gbl,
    extract_gbl_dates,
    extract_zip_codes,
    extract_tariff_rates,
    extract_rank_and_grade,
    extract_code_field
)

print("\n" + "="*70)
print("GBL SAMPLE 3 - EXTRACTION TEST")
print("="*70)

sample = 'data/input/GBL Sample 3.pdf'
reader = PdfReader(sample)
text = ""
for page in reader.pages:
    text += page.extract_text()

print("\n" + "-"*70)
print("CRITICAL FIELDS")
print("-"*70)

# B/L Number
bl_number = extract_bl_number(text)
print(f"B/L Number:              {bl_number}")

# SCAC
scac = extract_scac_code(text)
print(f"SCAC Code:               {scac}")

# Service Code
service_code = extract_service_code_gbl(text)
print(f"Service Code:            {service_code}")

# Dates
dates = extract_gbl_dates(text)
print(f"\nRequested Packing Date:  {dates['requested_packing_date']}")
print(f"Requested Pickup Date:   {dates['requested_pickup_date']}")
print(f"Required Delivery Date:  {dates['required_delivery_date']}")
print(f"Date of Order:           {dates['date_of_order']}")
print(f"Date B/L Printed:        {dates['date_bl_printed']}")

# Zip Codes
zips = extract_zip_codes(text)
print(f"\nOrigin Zip:              {zips['origin_zip']}")
print(f"Destination Zip:         {zips['destination_zip']}")

# Tariff Rates
rates = extract_tariff_rates(text)
print(f"\nTariff LH Rate:          {rates['lh_rate']}")
print(f"Tariff SIT Rate:         {rates['sit_rate']}")

# Rank and Grade
rank, grade = extract_rank_and_grade(text)
print(f"\nRank:                    {rank}")
print(f"Pay Grade:               {grade}")

# Administrative Codes
print(f"\n" + "-"*70)
print("ADMINISTRATIVE CODES")
print("-"*70)
print(f"SDN:                     {extract_code_field(text, 'SDN')}")
print(f"AIN:                     {extract_code_field(text, 'AIN')}")
print(f"TAC:                     {extract_code_field(text, 'TAC')}")

print("\n" + "="*70)
