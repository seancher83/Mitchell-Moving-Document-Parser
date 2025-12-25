"""Text processing utilities for GBL parsing."""

import re
from typing import Optional, List, Tuple


def extract_field_value(text: str, field_label: str, multiline: bool = False) -> Optional[str]:
    """
    Extract value following a field label.

    Args:
        text: Text to search in
        field_label: Label to find (e.g., "B/L NO.")
        multiline: Whether to search across multiple lines

    Returns:
        Extracted value or None if not found
    """
    # Escape special regex characters in label
    escaped_label = re.escape(field_label)

    if multiline:
        # Match across multiple lines, capture until next field or newline
        pattern = rf'{escaped_label}\s*[:.]?\s*([^\n]+)'
    else:
        # Single line match
        pattern = rf'{escaped_label}\s*[:.]?\s*([^\n]+)'

    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def extract_bl_number(text: str) -> Optional[str]:
    """
    Extract Bill of Lading number.

    B/L numbers typically follow the format: 4 letters + 7 digits (e.g., LKNQ0540823)
    """
    # Pattern 1: Standard B/L format - 4 letters followed by 7 digits
    # This is the most reliable pattern for GBL documents
    pattern_standard = r'\b([A-Z]{4}\d{7})\b'
    match = re.search(pattern_standard, text)
    if match:
        return match.group(1).strip()

    # Pattern 2: Look near "B/L NO." label (fallback)
    pattern_label = r'B/L\s*NO\.?\s*[:.]?\s*([A-Z0-9]{4,})'
    match = re.search(pattern_label, text, re.IGNORECASE)
    if match:
        bl_num = match.group(1).strip()
        # Verify it's not just a single digit or short code
        if len(bl_num) >= 4:
            return bl_num

    # Pattern 3: Near "BILL OF LADING" text (fallback)
    pattern_bol = r'BILL OF LADING.*?B/L\s*NO\.?\s*[:.]?\s*([A-Z0-9]{4,})'
    match = re.search(pattern_bol, text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()

    return None


def extract_date(text: str, field_label: str) -> Optional[str]:
    """
    Extract date following a field label.

    Args:
        text: Text to search in
        field_label: Label before the date

    Returns:
        Date string in YYYYMMDD format or None
    """
    escaped_label = re.escape(field_label)
    # Match 8-digit date format (YYYYMMDD)
    pattern = rf'{escaped_label}\s*[:.]?\s*(\d{{8}})'

    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def extract_all_dates(text: str) -> List[str]:
    """
    Extract all dates in YYYYMMDD format from the text.

    Returns:
        List of date strings found
    """
    pattern = r'\b(20\d{6})\b'
    matches = re.findall(pattern, text)
    return matches


def extract_gbl_dates(text: str) -> dict:
    """
    Extract specific GBL dates based on document structure and context.

    In GBL documents, dates appear in specific positions:
    - Requested Packing/Pickup dates: appear early, near "LOT" and before B/L number
    - Required Delivery Date: appears near customer info
    - Date of Order: appears near service branch
    - Date B/L Printed: appears near "ORIGINAL"

    Returns:
        Dictionary with extracted dates
    """
    dates = {
        "requested_packing_date": None,
        "requested_pickup_date": None,
        "required_delivery_date": None,
        "date_of_order": None,
        "date_bl_printed": None,
        "date_of_receipt": None,
    }

    all_dates = extract_all_dates(text)
    if not all_dates:
        return dates

    # Date B/L Printed - appears near "ORIGINAL" marker (before or after)
    match = re.search(r'(\d{8})[^\d]{0,20}ORIGINAL', text, re.IGNORECASE)
    if match:
        dates["date_bl_printed"] = match.group(1)
    else:
        # Try after ORIGINAL as fallback
        match = re.search(r'ORIGINAL[^\d]*(\d{8})', text, re.IGNORECASE)
        if match:
            dates["date_bl_printed"] = match.group(1)

    # Date of Order - appears near service branch or "BUPERS"  / military command
    match = re.search(r'(?:United States (?:Air Force|Army|Navy|Marine Corps|Coast Guard)|BUPERS|ARPC)[^\d]{0,50}(\d{8})', text, re.IGNORECASE)
    if match:
        dates["date_of_order"] = match.group(1)

    # Requested Packing/Pickup Date - appears near "LOT" and package count
    # This is typically the first date after "LOT"
    match = re.search(r'LOT[^\d]*(\d+)[^\d]*(\d{8})', text)
    if match:
        packing_date = match.group(2)
        dates["requested_packing_date"] = packing_date
        dates["requested_pickup_date"] = packing_date  # Often the same

    # Required Delivery Date - Look for 8-digit date near customer name or between customer and GBLOC
    # This is often a different date than packing/pickup
    # Try to find a date that appears after customer info but before "GBLOC" or "BILL OF LADING"
    match = re.search(r'(?:WOD|WD)[^\d]*(\d{8})', text)
    if match:
        delivery_date = match.group(1)
        # Make sure it's different from packing date
        if delivery_date != dates["requested_packing_date"]:
            dates["required_delivery_date"] = delivery_date

    # Date of Receipt - near "DATE OF RECEIPT" text or receipt shipment
    match = re.search(r'(?:DATE OF RECEIPT|RECEIPT OF SHIPMENT)[^\d]*(\d{8})', text, re.IGNORECASE)
    if match:
        dates["date_of_receipt"] = match.group(1)

    return dates


def extract_scac_code(text: str) -> Optional[str]:
    """Extract SCAC (Standard Carrier Alpha Code)."""
    # SCAC is typically 2-4 letter code
    pattern = r'SCAC\s*[:.]?\s*([A-Z]{2,4})'
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()
    return None


def extract_rank_and_grade(text: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract military rank and pay grade.

    Returns:
        Tuple of (rank, pay_grade) or (None, None)
    """
    # Pattern: NAME, RANK/GRADE (e.g., "TSG/E-6")
    pattern = r'([A-Z]{2,4})/([E|O|W]-?\d{1,2})'
    match = re.search(pattern, text)
    if match:
        return match.group(1), match.group(2)
    return None, None


def extract_address(text: str, context_line: str) -> Optional[str]:
    """
    Extract address near a context line.

    Args:
        text: Full text to search
        context_line: Line that appears before the address

    Returns:
        Extracted address or None
    """
    # Find the context line and grab the next few lines
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if context_line.lower() in line.lower():
            # Get next 2-3 lines as potential address
            address_parts = []
            for j in range(i + 1, min(i + 4, len(lines))):
                addr_line = lines[j].strip()
                if addr_line and not addr_line.startswith('---'):
                    address_parts.append(addr_line)
                else:
                    break
            if address_parts:
                return ', '.join(address_parts)
    return None


def extract_weight(text: str, weight_type: str = "GROSS") -> Optional[str]:
    """
    Extract weight value (gross, tare, or net).

    Args:
        text: Text to search
        weight_type: Type of weight (GROSS, TARE, NET)

    Returns:
        Weight value or None
    """
    pattern = rf'{weight_type}\s*[:.]?\s*(\d+(?:,\d+)?(?:\.\d+)?)\s*(?:lbs?|pounds?)?'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).replace(',', '')
    return None


def extract_gbloc(text: str) -> List[str]:
    """
    Extract GBLOC codes from the document.

    Returns:
        List of GBLOC codes found
    """
    gblocs = []
    pattern = r'GBLOC:\s*([A-Z]{4})'
    matches = re.finditer(pattern, text)
    for match in matches:
        gblocs.append(match.group(1))
    return list(set(gblocs))  # Remove duplicates


def extract_shipment_number(text: str) -> Optional[str]:
    """Extract shipment number."""
    pattern = r'SHIPMENT NO\.\s*[:.]?\s*(\d+)'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def extract_service_code(text: str) -> Optional[str]:
    """Extract service code."""
    pattern = r'SERVICE CODE\s*[:.]?\s*([A-Z0-9]+)'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def clean_text(text: str) -> str:
    """
    Clean extracted text by removing extra whitespace and special characters.

    Args:
        text: Text to clean

    Returns:
        Cleaned text
    """
    if not text:
        return ""

    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    # Remove common artifacts
    text = text.replace('---', '').replace('Page 1', '')

    return text


def extract_code_field(text: str, code_name: str) -> Optional[str]:
    """
    Extract various code fields (SDN, AIN, DI, TAC, SAC, MDC).

    Args:
        text: Text to search
        code_name: Name of the code (e.g., "SDN", "AIN", "TAC")

    Returns:
        Code value or None
    """
    pattern = rf'{code_name}:\s*([A-Z0-9\s]+?)(?:\n|[A-Z]{{3}}:)'
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()
    return None
