#!/usr/bin/env python3
"""Comprehensive test of all 10 GBL samples."""

import sys
sys.path.insert(0, 'src')

from PyPDF2 import PdfReader
from utils.text_utils import (
    extract_bl_number,
    extract_scac_code,
    extract_service_code_gbl,
    extract_gbl_dates,
    extract_zip_codes,
    extract_tariff_rates
)
from pathlib import Path

samples = [
    ("Sample 1", "data/input/GBL Sample.pdf"),
    ("Sample 2", "data/input/GBL Sample 2.pdf"),
    ("Sample 3", "data/input/GBL Sample 3.pdf"),
    ("Sample 4", "data/input/GBL Sample 4.pdf"),
    ("Sample 5", "data/input/GBL Sample 5.pdf"),
    ("Sample 6", "data/input/GBL Sample 6.pdf"),
    ("Sample 7", "data/input/GBL Sample 7.pdf"),
    ("Sample 8", "data/input/GBL Sample 8.pdf"),
    ("Sample 9", "data/input/GBL Sample 9.pdf"),
    ("Sample 10", "data/input/GBL Sample 10.pdf"),
]

print("\n" + "="*85)
print("COMPREHENSIVE GBL EXTRACTION TEST - ALL 10 SAMPLES")
print("="*85)

results = []

for sample_name, sample_path in samples:
    if not Path(sample_path).exists():
        print(f"\n⚠️  {sample_name}: FILE NOT FOUND")
        continue

    # Extract text
    reader = PdfReader(sample_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    # Extract fields
    bl_number = extract_bl_number(text)
    scac = extract_scac_code(text)
    service_code = extract_service_code_gbl(text)
    dates = extract_gbl_dates(text)
    zips = extract_zip_codes(text)
    rates = extract_tariff_rates(text)

    # Count successes
    fields = {
        'bl_number': bl_number,
        'scac': scac,
        'service_code': service_code,
        'packing_date': dates['requested_packing_date'],
        'pickup_date': dates['requested_pickup_date'],
        'delivery_date': dates['required_delivery_date'],
        'order_date': dates['date_of_order'],
        'bl_printed': dates['date_bl_printed'],
        'origin_zip': zips['origin_zip'],
        'dest_zip': zips['destination_zip'],
        'lh_rate': rates['lh_rate'],
        'sit_rate': rates['sit_rate']
    }

    success_count = sum(1 for v in fields.values() if v is not None)
    total_fields = len(fields)
    success_rate = (success_count / total_fields) * 100

    results.append({
        'name': sample_name,
        'fields': fields,
        'success': success_count,
        'total': total_fields,
        'rate': success_rate
    })

    status_icon = "✓" if success_rate >= 90 else "⚠️" if success_rate >= 70 else "❌"
    print(f"\n{status_icon} {sample_name}: {success_count}/{total_fields} ({success_rate:.0f}%)")
    print("-"*85)
    print(f"  B/L Number:       {bl_number or 'NULL':20s}  |  Packing Date:   {dates['requested_packing_date'] or 'NULL'}")
    print(f"  SCAC:             {scac or 'NULL':20s}  |  Pickup Date:    {dates['requested_pickup_date'] or 'NULL'}")
    print(f"  Service Code:     {service_code or 'NULL':20s}  |  Delivery Date:  {dates['required_delivery_date'] or 'NULL'}")
    print(f"  Origin Zip:       {zips['origin_zip'] or 'NULL':20s}  |  Order Date:     {dates['date_of_order'] or 'NULL'}")
    print(f"  Dest Zip:         {zips['destination_zip'] or 'NULL':20s}  |  B/L Printed:    {dates['date_bl_printed'] or 'NULL'}")
    print(f"  LH Rate:          {rates['lh_rate'] or 'NULL':20s}  |  SIT Rate:       {rates['sit_rate'] or 'NULL'}")

# Summary
print("\n" + "="*85)
print("OVERALL SUMMARY")
print("="*85)
avg_rate = sum(r['rate'] for r in results) / len(results) if results else 0
print(f"Average Success Rate:    {avg_rate:.1f}%")
print(f"Samples Tested:          {len(results)}")
print(f"Samples @ 100%:          {sum(1 for r in results if r['rate'] == 100)} ({sum(1 for r in results if r['rate'] == 100)/len(results)*100:.0f}%)")
print(f"Samples @ 90%+:          {sum(1 for r in results if r['rate'] >= 90)} ({sum(1 for r in results if r['rate'] >= 90)/len(results)*100:.0f}%)")
print(f"Samples @ 70-89%:        {sum(1 for r in results if 70 <= r['rate'] < 90)} ({sum(1 for r in results if 70 <= r['rate'] < 90)/len(results)*100:.0f}%)")
print(f"Samples < 70%:           {sum(1 for r in results if r['rate'] < 70)} ({sum(1 for r in results if r['rate'] < 70)/len(results)*100:.0f}%)")

# Field-level analysis
print("\n" + "="*85)
print("FIELD-LEVEL SUCCESS RATES")
print("="*85)
field_labels = {
    'bl_number': 'B/L Number',
    'scac': 'SCAC Code',
    'service_code': 'Service Code',
    'packing_date': 'Packing Date',
    'pickup_date': 'Pickup Date',
    'delivery_date': 'Delivery Date',
    'order_date': 'Order Date',
    'bl_printed': 'B/L Printed',
    'origin_zip': 'Origin Zip',
    'dest_zip': 'Dest Zip',
    'lh_rate': 'LH Rate',
    'sit_rate': 'SIT Rate'
}

for field_name, field_label in field_labels.items():
    success_count = sum(1 for r in results if r['fields'][field_name] is not None)
    rate = (success_count / len(results)) * 100 if results else 0
    status = "✓" if rate >= 80 else "⚠️" if rate >= 50 else "❌"
    print(f"{status} {field_label:20s}: {success_count:2d}/{len(results):2d} ({rate:5.1f}%)")

# List problem fields
print("\n" + "="*85)
print("FIELDS NEEDING IMPROVEMENT (< 80% success)")
print("="*85)
for field_name, field_label in field_labels.items():
    success_count = sum(1 for r in results if r['fields'][field_name] is not None)
    rate = (success_count / len(results)) * 100 if results else 0
    if rate < 80:
        print(f"❌ {field_label:20s}: {rate:5.1f}% - Missing in {len(results) - success_count} samples")
        # Show which samples are missing this field
        missing_samples = [r['name'] for r in results if r['fields'][field_name] is None]
        print(f"   Missing in: {', '.join(missing_samples)}")

print("\n" + "="*85)
