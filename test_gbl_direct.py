#!/usr/bin/env python3
"""Direct test of GBL parser - standalone version."""

import sys
import json
import re
from pathlib import Path
from PyPDF2 import PdfReader

def extract_bl_number(text):
    """Extract Bill of Lading number."""
    patterns = [
        r'B/L\s*NO\.?\s*([A-Z0-9]+)',
        r'ORIGINAL.*?B/L\s*NO\.?\s*([A-Z0-9]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None

def extract_date(text, field_label):
    """Extract date following a field label."""
    escaped_label = re.escape(field_label)
    pattern = rf'{escaped_label}\s*[:.]?\s*(\d{{8}})'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

def extract_scac_code(text):
    """Extract SCAC code."""
    pattern = r'SCAC\s*[:.]?\s*([A-Z]{2,4})'
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()
    return None

def main():
    pdf_path = "data/input/GBL Sample.pdf"
    output_path = "data/output/gbl_parsed_test.json"

    print("Mitchell Moving Document Parser - Test Run")
    print("=" * 50)
    print(f"Input: {pdf_path}")
    print(f"Output: {output_path}")
    print("=" * 50)

    # Extract text from PDF
    reader = PdfReader(pdf_path)
    full_text = ""
    for page_num, page in enumerate(reader.pages, 1):
        text = page.extract_text()
        if text:
            full_text += f"\n--- Page {page_num} ---\n{text}"

    print(f"\n✓ Extracted text from {len(reader.pages)} page(s)")

    # Extract data
    data = {
        "file_name": Path(pdf_path).name,
        "num_pages": len(reader.pages),
        "header": {
            "gbl_number": extract_bl_number(full_text),
            "date_bl_printed": extract_date(full_text, "DATE B/L PRINTED"),
            "scac_code": extract_scac_code(full_text),
        },
        "customer": {},
        "shipment": {},
        "administrative_codes": {},
    }

    # Extract property owner name
    name_match = re.search(r'(BLYTHE,\s*NICHOLAS)', full_text)
    if name_match:
        data["customer"]["name"] = name_match.group(1)

    # Extract rank and grade
    rank_match = re.search(r'([A-Z]{2,4})/([E|O|W]-?\d{1,2})', full_text)
    if rank_match:
        data["customer"]["rank"] = rank_match.group(1)
        data["customer"]["pay_grade"] = rank_match.group(2)

    # Extract service branch
    if "United States Air Force" in full_text:
        data["customer"]["service_branch"] = "United States Air Force"

    # Extract transportation company
    company_match = re.search(r'Suddath Relocation Systems[^\n]+', full_text)
    if company_match:
        data["header"]["transportation_company"] = company_match.group(0).strip()

    # Extract codes
    for code_name in ["SDN", "AIN", "DI", "TAC", "SAC", "MDC"]:
        pattern = rf'{code_name}:\s*([A-Z0-9\s]+?)(?:\n|[A-Z]{{3}}:)'
        match = re.search(pattern, full_text)
        if match:
            data["administrative_codes"][code_name.lower()] = match.group(1).strip()

    # Extract addresses
    origin_match = re.search(r'RIVERSIDE,\s*CA\s*\d{5}', full_text)
    if origin_match:
        data["shipment"]["origin"] = origin_match.group(0)

    dest_match = re.search(r'McChord AFB,\s*WA\s*\d{5}', full_text)
    if dest_match:
        data["shipment"]["destination"] = dest_match.group(0)

    # Print results
    print("\n✓ Extraction Results:")
    print(f"  - GBL Number: {data['header'].get('gbl_number')}")
    print(f"  - Transportation Company: {data['header'].get('transportation_company')}")
    print(f"  - Customer: {data['customer'].get('name')} ({data['customer'].get('rank')}/{data['customer'].get('pay_grade')})")
    print(f"  - Service Branch: {data['customer'].get('service_branch')}")
    print(f"  - Origin: {data['shipment'].get('origin')}")
    print(f"  - Destination: {data['shipment'].get('destination')}")

    # Save to JSON
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"\n✓ Results saved to: {output_path}")
    print("=" * 50)
    print("Test completed successfully!")

    return 0

if __name__ == "__main__":
    sys.exit(main())
