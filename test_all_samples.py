#!/usr/bin/env python3
"""Test GBL parser with all available sample documents."""

import sys
sys.path.insert(0, 'src')

from pathlib import Path
from PyPDF2 import PdfReader
from utils.text_utils import (
    extract_bl_number,
    extract_date,
    extract_scac_code,
    extract_rank_and_grade,
    extract_code_field,
)
import json

def test_gbl_sample(pdf_path):
    """Test extraction on a single GBL sample."""
    print(f"\n{'='*60}")
    print(f"Testing: {pdf_path}")
    print('='*60)

    if not Path(pdf_path).exists():
        print(f"✗ File not found: {pdf_path}")
        return None

    # Extract text
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\n"

    # Extract key fields
    results = {
        "file": Path(pdf_path).name,
        "bl_number": extract_bl_number(full_text),
        "scac_code": extract_scac_code(full_text),
        "date_bl_printed": extract_date(full_text, "DATE B/L PRINTED"),
        "date_of_order": extract_date(full_text, "DATE OF ORDER"),
    }

    # Extract rank and grade
    rank, pay_grade = extract_rank_and_grade(full_text)
    results["rank"] = rank
    results["pay_grade"] = pay_grade

    # Extract customer name
    import re
    name_match = re.search(r'([A-Z]+,\s*[A-Z]+)\s+[A-Z]{2,4}/[EWO]-?\d', full_text)
    if name_match:
        results["customer_name"] = name_match.group(1)

    # Extract service branch
    if "United States Air Force" in full_text:
        results["service_branch"] = "USAF"
    elif "United States Army" in full_text:
        results["service_branch"] = "USA"
    elif "United States Navy" in full_text:
        results["service_branch"] = "USN"
    elif "United States Marine Corps" in full_text:
        results["service_branch"] = "USMC"

    # Extract transportation company
    company_match = re.search(r'([\w\s]+(?:Relocation|Moving|Van Lines)[^\n]{0,50})', full_text)
    if company_match:
        results["transportation_company"] = company_match.group(1).strip()

    # Extract codes
    for code in ["SDN", "AIN", "TAC"]:
        results[code.lower()] = extract_code_field(full_text, code)

    # Display results
    print(f"\n{'Key Extractions:':<25}")
    print(f"  B/L Number:          {results.get('bl_number', 'NOT FOUND')}")
    print(f"  SCAC Code:           {results.get('scac_code', 'NOT FOUND')}")
    print(f"  Customer:            {results.get('customer_name', 'NOT FOUND')}")
    print(f"  Rank/Grade:          {results.get('rank', '')}/{results.get('pay_grade', '')}")
    print(f"  Service Branch:      {results.get('service_branch', 'NOT FOUND')}")
    print(f"  Transport Company:   {results.get('transportation_company', 'NOT FOUND')[:50]}")
    print(f"  Date B/L Printed:    {results.get('date_bl_printed', 'NOT FOUND')}")
    print(f"  Date of Order:       {results.get('date_of_order', 'NOT FOUND')}")
    print(f"  SDN:                 {results.get('sdn', 'NOT FOUND')}")
    print(f"  AIN:                 {results.get('ain', 'NOT FOUND')}")
    print(f"  TAC:                 {results.get('tac', 'NOT FOUND')}")

    return results

def main():
    """Test all available GBL samples."""
    print("\n" + "="*60)
    print("GBL PARSER - COMPREHENSIVE SAMPLE TESTING")
    print("="*60)

    # List of sample files to test
    samples = [
        "data/input/GBL Sample.pdf",
        "data/input/GBL Sample 2.pdf",
        "data/input/GBL Sample 3.pdf",
    ]

    all_results = []
    for sample in samples:
        result = test_gbl_sample(sample)
        if result:
            all_results.append(result)

    # Save combined results
    if all_results:
        output_file = "data/output/all_samples_test.json"
        with open(output_file, 'w') as f:
            json.dump(all_results, f, indent=2)

        print(f"\n{'='*60}")
        print(f"✓ Tested {len(all_results)} file(s)")
        print(f"✓ Results saved to: {output_file}")
        print("="*60)

        # Summary
        print("\nSUMMARY:")
        for r in all_results:
            bl_status = "✓" if r.get('bl_number') and len(r.get('bl_number', '')) > 4 else "✗"
            print(f"  {bl_status} {r['file']:<25} B/L: {r.get('bl_number', 'MISSING')}")

if __name__ == "__main__":
    main()
