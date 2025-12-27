#!/usr/bin/env python3
"""Test all samples and display results in a table format."""

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

print("\n" + "="*150)
print("COMPREHENSIVE TEST RESULTS - ALL 10 SAMPLES")
print("="*150)
print("\nProcessing samples with automatic detection (text-based vs scanned)...\n")

results = []

for sample_name, sample_path in samples:
    if not Path(sample_path).exists():
        continue

    parser = GBLParser(sample_path)
    result = parser.parse()

    # Extract fields
    header = result.get('header', {})
    shipment = result.get('shipment', {})

    results.append({
        'sample': sample_name,
        'pdf_type': result.get('pdf_type', 'unknown'),
        'method': result.get('extraction_method', 'unknown'),
        'bl_number': header.get('gbl_number') or 'NULL',
        'scac': header.get('scac_code') or 'NULL',
        'service_code': header.get('service_code') or 'NULL',
        'packing_date': shipment.get('requested_packing_date') or 'NULL',
        'pickup_date': shipment.get('requested_pickup_date') or 'NULL',
        'delivery_date': shipment.get('required_delivery_date') or 'NULL',
        'order_date': shipment.get('date_of_order') or 'NULL',
        'bl_printed': header.get('date_bl_printed') or 'NULL',
        'origin_zip': shipment.get('origin_zip') or 'NULL',
        'dest_zip': shipment.get('destination_zip') or 'NULL',
        'lh_rate': shipment.get('tariff_lh_rate') or 'NULL',
        'sit_rate': shipment.get('tariff_sit_rate') or 'NULL',
        'company': header.get('transportation_company') or 'N/A'
    })

# Print main extraction table
print("\n" + "="*150)
print("EXTRACTED FIELDS - ALL SAMPLES")
print("="*150)
print(f"\n{'Sample':<12} {'Type':<10} {'B/L Number':<15} {'SCAC':<6} {'Service':<8} {'Origin':<8} {'Dest':<8} {'Company':<30}")
print("-"*150)

for r in results:
    print(f"{r['sample']:<12} {r['pdf_type']:<10} {r['bl_number']:<15} {r['scac']:<6} {r['service_code']:<8} {r['origin_zip']:<8} {r['dest_zip']:<8} {r['company']:<30}")

# Print dates table
print("\n" + "="*150)
print("DATE FIELDS - ALL SAMPLES")
print("="*150)
print(f"\n{'Sample':<12} {'Packing Date':<15} {'Pickup Date':<15} {'Delivery Date':<15} {'Order Date':<15} {'B/L Printed':<15}")
print("-"*150)

for r in results:
    print(f"{r['sample']:<12} {r['packing_date']:<15} {r['pickup_date']:<15} {r['delivery_date']:<15} {r['order_date']:<15} {r['bl_printed']:<15}")

# Print tariff rates table
print("\n" + "="*150)
print("TARIFF RATES - ALL SAMPLES")
print("="*150)
print(f"\n{'Sample':<12} {'LH Rate':<10} {'SIT Rate':<10} {'Method':<15}")
print("-"*150)

for r in results:
    method_display = f"{r['pdf_type']}/{r['method']}"
    print(f"{r['sample']:<12} {r['lh_rate']:<10} {r['sit_rate']:<10} {method_display:<15}")

# Summary statistics
print("\n" + "="*150)
print("SUMMARY STATISTICS")
print("="*150)

# Count success per sample
for r in results:
    fields = [r['bl_number'], r['scac'], r['service_code'], r['packing_date'],
              r['pickup_date'], r['delivery_date'], r['order_date'], r['bl_printed'],
              r['origin_zip'], r['dest_zip'], r['lh_rate'], r['sit_rate']]
    success_count = sum(1 for f in fields if f != 'NULL')
    r['success_count'] = success_count
    r['success_rate'] = (success_count / 12) * 100

avg_rate = sum(r['success_rate'] for r in results) / len(results)
text_based = [r for r in results if r['pdf_type'] == 'text-based']
scanned = [r for r in results if r['pdf_type'] == 'scanned']

print(f"\nOverall Average Success Rate:    {avg_rate:.1f}%")
print(f"Samples Tested:                  {len(results)}")
print(f"Samples @ 100%:                  {sum(1 for r in results if r['success_rate'] == 100)} ({sum(1 for r in results if r['success_rate'] == 100)/len(results)*100:.0f}%)")
print(f"Text-based samples:              {len(text_based)} (avg: {sum(r['success_rate'] for r in text_based)/len(text_based):.1f}%)")
print(f"Scanned samples (OCR):           {len(scanned)} (avg: {sum(r['success_rate'] for r in scanned)/len(scanned):.1f}% if scanned else 0)%)")

print("\n" + "="*150)
print("PER-SAMPLE SUCCESS RATES")
print("="*150)
print(f"\n{'Sample':<12} {'Fields Extracted':<20} {'Success Rate':<15} {'Status':<10}")
print("-"*150)

for r in results:
    status = "✓ Perfect" if r['success_rate'] == 100 else "⚠️ Partial" if r['success_rate'] >= 30 else "❌ Poor"
    print(f"{r['sample']:<12} {r['success_count']:>2}/12{'':<15} {r['success_rate']:>5.1f}%{'':<9} {status:<10}")

print("\n" + "="*150)
