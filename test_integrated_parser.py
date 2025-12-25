#!/usr/bin/env python3
"""Test the integrated GBL parser with all new extraction functions."""

import sys
import json
sys.path.insert(0, 'src')

from parsers.gbl_parser import GBLParser

print("\n" + "="*70)
print("TESTING INTEGRATED GBL PARSER")
print("="*70)

# Test with GBL Sample 1
sample = "data/input/GBL Sample.pdf"
print(f"\nParsing: {sample}")
print("-"*70)

try:
    parser = GBLParser(sample)
    data = parser.parse()

    # Remove raw_text for cleaner output
    if "raw_text" in data:
        del data["raw_text"]

    # Display extracted data
    print("\n📋 HEADER INFORMATION:")
    for key, value in data.get("header", {}).items():
        print(f"  {key:<25} {value}")

    print("\n📦 SHIPMENT DETAILS:")
    for key, value in data.get("shipment", {}).items():
        print(f"  {key:<25} {value}")

    print("\n👤 CUSTOMER INFORMATION:")
    for key, value in data.get("customer", {}).items():
        print(f"  {key:<25} {value}")

    print("\n📊 ADMINISTRATIVE CODES:")
    for key, value in data.get("administrative_codes", {}).items():
        print(f"  {key:<25} {value}")

    # Validate critical fields
    print("\n" + "="*70)
    print("VALIDATION - CRITICAL FIELDS")
    print("="*70)

    validations = {
        "B/L Number": (data["header"].get("gbl_number"), "LKNQ0540823"),
        "SCAC": (data["header"].get("scac_code"), "SDDA"),
        "Service Code": (data["header"].get("service_code"), "D"),
        "Packing Date": (data["shipment"].get("requested_packing_date"), "20251216"),
        "Pickup Date": (data["shipment"].get("requested_pickup_date"), "20251216"),
        "Delivery Date": (data["shipment"].get("required_delivery_date"), "20260113"),
        "Origin Zip": (data["shipment"].get("origin_zip"), "92507"),
        "Destination Zip": (data["shipment"].get("destination_zip"), "98438"),
        "Tariff LH": (data["shipment"].get("tariff_lh_rate"), "67%"),
        "Tariff SIT": (data["shipment"].get("tariff_sit_rate"), "63%"),
    }

    all_pass = True
    for field_name, (actual, expected) in validations.items():
        status = "✓" if actual == expected else "✗"
        if actual != expected:
            all_pass = False
        print(f"{status} {field_name:<20} {actual:<15} (expected: {expected})")

    print("="*70)
    if all_pass:
        print("✅ ALL CRITICAL FIELDS VALIDATED - PARSER WORKING PERFECTLY!")
    else:
        print("⚠️  Some fields need attention")
    print("="*70)

    # Save to JSON
    output_file = "data/output/integrated_test_output.json"
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"\n💾 Full output saved to: {output_file}")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*70 + "\n")
