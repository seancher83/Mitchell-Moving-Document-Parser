#!/usr/bin/env python3
"""Comprehensive test showing all extracted fields from GBL Sample 1."""

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
    extract_code_field,
)
import re

print("\n" + "="*70)
print("COMPLETE GBL EXTRACTION - Sample 1")
print("="*70)

sample = 'data/input/GBL Sample.pdf'
reader = PdfReader(sample)
text = ""
for page in reader.pages:
    text += page.extract_text()

# Extract all fields
bl_number = extract_bl_number(text)
scac = extract_scac_code(text)
service_code = extract_service_code_gbl(text)
dates = extract_gbl_dates(text)
zips = extract_zip_codes(text)
rates = extract_tariff_rates(text)
rank, pay_grade = extract_rank_and_grade(text)

# Extract customer name
name_match = re.search(r'(BLYTHE,\s*NICHOLAS)', text)
customer_name = name_match.group(1) if name_match else None

# Extract service branch
service_branch = "USAF" if "United States Air Force" in text else None

# Extract transportation company
company_match = re.search(r'Suddath Relocation Systems[^\n]+', text)
company = company_match.group(0).strip() if company_match else None

# Extract codes
sdn = extract_code_field(text, "SDN")
ain = extract_code_field(text, "AIN")
tac = extract_code_field(text, "TAC")

print("\n" + "-"*70)
print("CRITICAL FIELDS (User Requirements)")
print("-"*70)
print(f"B/L Number:                    {bl_number}")
print(f"SCAC:                          {scac}")
print(f"Service Code:                  {service_code}")
print(f"Requested Packing Date:        {dates['requested_packing_date']}")
print(f"Requested Pickup Date:         {dates['requested_pickup_date']}")
print(f"Required Delivery Date:        {dates['required_delivery_date']}")
print(f"Origin Zip:                    {zips['origin_zip']}")
print(f"Destination Zip:               {zips['destination_zip']}")
print(f"Tariff LH Rate:                {rates['lh_rate']}")
print(f"Tariff SIT Rate:               {rates['sit_rate']}")

print("\n" + "-"*70)
print("ADDITIONAL FIELDS")
print("-"*70)
print(f"Date of Order:                 {dates['date_of_order']}")
print(f"Date B/L Printed:              {dates['date_bl_printed']}")
print(f"Customer Name:                 {customer_name}")
print(f"Rank/Grade:                    {rank}/{pay_grade}")
print(f"Service Branch:                {service_branch}")
print(f"Transportation Company:        {company}")
print(f"SDN:                           {sdn}")
print(f"AIN:                           {ain}")
print(f"TAC:                           {tac}")

print("\n" + "="*70)
print("VALIDATION SUMMARY")
print("="*70)

validations = {
    "B/L Number": (bl_number, "LKNQ0540823"),
    "SCAC": (scac, "SDDA"),
    "Service Code": (service_code, "D"),
    "Requested Packing Date": (dates['requested_packing_date'], "20251216"),
    "Requested Pickup Date": (dates['requested_pickup_date'], "20251216"),
    "Required Delivery Date": (dates['required_delivery_date'], "20260113"),
    "Origin Zip": (zips['origin_zip'], "92507"),
    "Destination Zip": (zips['destination_zip'], "98438"),
    "Tariff LH": (rates['lh_rate'], "67%"),
    "Tariff SIT": (rates['sit_rate'], "63%"),
}

all_pass = True
for field_name, (actual, expected) in validations.items():
    status = "✓" if actual == expected else "✗"
    if actual != expected:
        all_pass = False
    print(f"{status} {field_name:<30} {actual:<15} (expected: {expected})")

print("="*70)
if all_pass:
    print("✅ ALL CRITICAL FIELDS VALIDATED SUCCESSFULLY!")
else:
    print("⚠️  Some fields need attention")
print("="*70 + "\n")
