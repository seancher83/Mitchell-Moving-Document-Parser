#!/usr/bin/env python3
"""Test all samples with OCR enabled."""

import sys
sys.path.insert(0, 'src')

from parsers.gbl_parser import GBLParser
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
print("COMPREHENSIVE TEST - ALL 10 SAMPLES WITH OCR")
print("="*85)

results = []

for sample_name, sample_path in samples:
    if not Path(sample_path).exists():
        continue

    parser = GBLParser(sample_path)
    result = parser.parse()

    # Count non-null fields
    header = result.get('header', {})
    shipment = result.get('shipment', {})

    fields = {
        'bl_number': header.get('gbl_number'),
        'scac': header.get('scac_code'),
        'service_code': header.get('service_code'),
        'packing_date': shipment.get('requested_packing_date'),
        'pickup_date': shipment.get('requested_pickup_date'),
        'delivery_date': shipment.get('required_delivery_date'),
        'order_date': shipment.get('date_of_order'),
        'bl_printed': header.get('date_bl_printed'),
        'origin_zip': shipment.get('origin_zip'),
        'dest_zip': shipment.get('destination_zip'),
        'lh_rate': shipment.get('tariff_lh_rate'),
        'sit_rate': shipment.get('tariff_sit_rate')
    }

    success_count = sum(1 for v in fields.values() if v is not None)
    total_fields = len(fields)
    success_rate = (success_count / total_fields) * 100

    pdf_type = result.get('pdf_type', 'unknown')
    method = result.get('extraction_method', 'unknown')

    results.append({
        'name': sample_name,
        'fields': fields,
        'success': success_count,
        'total': total_fields,
        'rate': success_rate,
        'pdf_type': pdf_type,
        'method': method
    })

    status_icon = "✓" if success_rate >= 90 else "⚠️" if success_rate >= 30 else "❌"
    print(f"\n{status_icon} {sample_name}: {success_count}/{total_fields} ({success_rate:.0f}%) [{pdf_type.upper()}/{method.upper()}]")
    print("-"*85)
    print(f"  B/L: {fields['bl_number'] or 'NULL':20s} | Packing: {fields['packing_date'] or 'NULL'}")
    print(f"  SCAC: {fields['scac'] or 'NULL':19s} | Pickup: {fields['pickup_date'] or 'NULL'}")
    print(f"  Service: {fields['service_code'] or 'NULL':16s} | Delivery: {fields['delivery_date'] or 'NULL'}")
    print(f"  Origin Zip: {fields['origin_zip'] or 'NULL':12s} | Order: {fields['order_date'] or 'NULL'}")
    print(f"  Dest Zip: {fields['dest_zip'] or 'NULL':14s} | B/L Printed: {fields['bl_printed'] or 'NULL'}")
    print(f"  LH: {fields['lh_rate'] or 'NULL':18s} | SIT: {fields['sit_rate'] or 'NULL'}")

# Summary
print("\n" + "="*85)
print("OVERALL SUMMARY")
print("="*85)
avg_rate = sum(r['rate'] for r in results) / len(results) if results else 0
print(f"Average Success Rate:    {avg_rate:.1f}%")
print(f"Samples Tested:          {len(results)}")
print(f"Samples @ 100%:          {sum(1 for r in results if r['rate'] == 100)} ({sum(1 for r in results if r['rate'] == 100)/len(results)*100:.0f}%)")
print(f"Samples @ 90%+:          {sum(1 for r in results if r['rate'] >= 90)} ({sum(1 for r in results if r['rate'] >= 90)/len(results)*100:.0f}%)")
print(f"Samples @ 30-89%:        {sum(1 for r in results if 30 <= r['rate'] < 90)} ({sum(1 for r in results if 30 <= r['rate'] < 90)/len(results)*100:.0f}%)")
print(f"Samples < 30%:           {sum(1 for r in results if r['rate'] < 30)} ({sum(1 for r in results if r['rate'] < 30)/len(results)*100:.0f}%)")

# Method breakdown
text_based = [r for r in results if r['pdf_type'] == 'text-based']
scanned = [r for r in results if r['pdf_type'] == 'scanned']

print(f"\nText-based samples:      {len(text_based)} (avg: {sum(r['rate'] for r in text_based)/len(text_based):.1f}%)")
print(f"Scanned samples (OCR):   {len(scanned)} (avg: {sum(r['rate'] for r in scanned)/len(scanned):.1f}%)")

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

print("\n" + "="*85)
