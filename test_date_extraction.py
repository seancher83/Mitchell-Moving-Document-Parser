#!/usr/bin/env python3
"""Test improved date extraction."""

import sys
sys.path.insert(0, 'src')

from PyPDF2 import PdfReader
from utils.text_utils import extract_gbl_dates

samples = [
    ("GBL Sample.pdf", {
        "expected_packing": "20251216",
        "expected_pickup": "20251216",
        "expected_delivery": "20260113",
        "expected_order": "20230320",
        "expected_bl_printed": "20251212",
    }),
    ("GBL Sample 2.pdf", {
        "expected_packing": "20251215",
        "expected_pickup": "20251215",
    }),
    ("GBL Sample 3.pdf", {
        "expected_packing": "20251201",
        "expected_pickup": "20251201",
        "expected_delivery": "20251223",
    }),
]

print("\n" + "="*70)
print("TESTING DATE EXTRACTION")
print("="*70)

for filename, expected in samples:
    filepath = f"data/input/{filename}"
    print(f"\n{filename}")
    print("-"*70)

    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    dates = extract_gbl_dates(text)

    print(f"Requested Packing Date:  {dates['requested_packing_date']}", end="")
    if 'expected_packing' in expected:
        status = "✓" if dates['requested_packing_date'] == expected['expected_packing'] else "✗"
        print(f"  {status} (expected: {expected['expected_packing']})")
    else:
        print()

    print(f"Requested Pickup Date:   {dates['requested_pickup_date']}", end="")
    if 'expected_pickup' in expected:
        status = "✓" if dates['requested_pickup_date'] == expected['expected_pickup'] else "✗"
        print(f"  {status} (expected: {expected['expected_pickup']})")
    else:
        print()

    print(f"Required Delivery Date:  {dates['required_delivery_date']}", end="")
    if 'expected_delivery' in expected:
        status = "✓" if dates['required_delivery_date'] == expected['expected_delivery'] else "✗"
        print(f"  {status} (expected: {expected['expected_delivery']})")
    else:
        print()

    print(f"Date of Order:           {dates['date_of_order']}", end="")
    if 'expected_order' in expected:
        status = "✓" if dates['date_of_order'] == expected['expected_order'] else "✗"
        print(f"  {status} (expected: {expected['expected_order']})")
    else:
        print()

    print(f"Date B/L Printed:        {dates['date_bl_printed']}", end="")
    if 'expected_bl_printed' in expected:
        status = "✓" if dates['date_bl_printed'] == expected['expected_bl_printed'] else "✗"
        print(f"  {status} (expected: {expected['expected_bl_printed']})")
    else:
        print()

print("\n" + "="*70)
