"""
Government Bill of Lading (GBL) Parser

This module handles parsing of GBL documents and extraction of structured data.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import re

# Try to import PDF libraries
try:
    import pdfplumber
    PDF_LIBRARY = "pdfplumber"
except ImportError:
    pdfplumber = None
    try:
        from PyPDF2 import PdfReader
        PDF_LIBRARY = "pypdf2"
    except ImportError:
        raise ImportError("Either pdfplumber or PyPDF2 is required. Install with: pip install PyPDF2")
try:
    from ..utils.text_utils import (
        extract_bl_number,
        extract_date,
        extract_scac_code,
        extract_service_code_gbl,
        extract_rank_and_grade,
        extract_gbloc,
        extract_shipment_number,
        extract_service_code,
        extract_field_value,
        extract_code_field,
        extract_gbl_dates,
        extract_zip_codes,
        extract_tariff_rates,
        clean_text,
    )
except ImportError:
    from utils.text_utils import (
        extract_bl_number,
        extract_date,
        extract_scac_code,
        extract_service_code_gbl,
        extract_rank_and_grade,
        extract_gbloc,
        extract_shipment_number,
        extract_service_code,
        extract_field_value,
        extract_code_field,
        extract_gbl_dates,
        extract_zip_codes,
        extract_tariff_rates,
        clean_text,
    )


class GBLParser:
    """Parser for Government Bill of Lading documents."""

    def __init__(self, file_path: str):
        """
        Initialize the GBL parser.

        Args:
            file_path: Path to the GBL document (PDF format)
        """
        self.file_path = Path(file_path)
        self.data: Dict[str, Any] = {}

        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if self.file_path.suffix.lower() != ".pdf":
            raise ValueError(f"Only PDF files are supported. Got: {self.file_path.suffix}")

    def parse(self) -> Dict[str, Any]:
        """
        Parse the GBL document and extract all relevant data.

        Returns:
            Dictionary containing extracted GBL data
        """
        print(f"Parsing GBL document: {self.file_path.name}")

        full_text = ""
        num_pages = 0

        if PDF_LIBRARY == "pdfplumber" and pdfplumber is not None:
            # Use pdfplumber if available
            with pdfplumber.open(self.file_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text:
                        full_text += f"\n--- Page {page_num} ---\n{text}"
                num_pages = len(pdf.pages)
        else:
            # Fallback to PyPDF2
            from PyPDF2 import PdfReader
            reader = PdfReader(str(self.file_path))
            for page_num, page in enumerate(reader.pages, 1):
                text = page.extract_text()
                if text:
                    full_text += f"\n--- Page {page_num} ---\n{text}"
            num_pages = len(reader.pages)

        # Store raw text for debugging
        self.data["raw_text"] = full_text
        self.data["num_pages"] = num_pages

        # Extract structured data
        self._extract_header_info(full_text)
        self._extract_shipment_details(full_text)
        self._extract_customer_info(full_text)
        self._extract_inventory(full_text)
        self._extract_charges(full_text)
        self._extract_administrative_codes(full_text)

        return self.data

    def _extract_header_info(self, text: str) -> None:
        """Extract header information (GBL number, dates, etc.)."""
        # Extract dates using the comprehensive date extraction
        dates = extract_gbl_dates(text)

        self.data["header"] = {
            "gbl_number": extract_bl_number(text),
            "date_bl_printed": dates.get("date_bl_printed"),
            "shipment_number": extract_shipment_number(text),
            "scac_code": extract_scac_code(text),
            "service_code": extract_service_code_gbl(text),
            "transportation_company": self._extract_transportation_company(text),
            "gbloc_codes": extract_gbloc(text),
        }

    def _extract_transportation_company(self, text: str) -> Optional[str]:
        """Extract transportation company name."""
        # Look for company name after "TRANSPORTATION COMPANY" or at beginning
        pattern = r'TRANSPORTATION\s+COMPANY[^\n]*\n\s*([^\n]+)'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            company = match.group(1).strip()
            # Clean up the company name
            company = re.sub(r'TENDERED TO.*$', '', company, flags=re.IGNORECASE).strip()
            return clean_text(company)
        return None

    def _extract_shipment_details(self, text: str) -> None:
        """Extract shipment details (origin, destination, dates)."""
        # Extract all dates
        dates = extract_gbl_dates(text)

        # Extract zip codes
        zips = extract_zip_codes(text)

        # Extract tariff rates
        rates = extract_tariff_rates(text)

        self.data["shipment"] = {
            "origin": self._extract_origin_address(text),
            "destination": self._extract_destination_address(text),
            "origin_zip": zips.get("origin_zip"),
            "destination_zip": zips.get("destination_zip"),
            "requested_packing_date": dates.get("requested_packing_date"),
            "requested_pickup_date": dates.get("requested_pickup_date"),
            "required_delivery_date": dates.get("required_delivery_date"),
            "date_of_receipt": dates.get("date_of_receipt"),
            "authority": extract_field_value(text, "AUTHORITY FOR SHIPMENT"),
            "date_of_order": dates.get("date_of_order"),
            "tariff_lh_rate": rates.get("lh_rate"),
            "tariff_sit_rate": rates.get("sit_rate"),
        }

    def _extract_origin_address(self, text: str) -> Optional[str]:
        """Extract origin/pickup address."""
        # Look for address after "FROM (Complete address of point of pickup)"
        pattern = r'FROM\s*\(Complete address[^\)]*\)[^\n]*\n\s*([^\n]+(?:\n[^\n]+)?)'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return clean_text(match.group(1))
        return None

    def _extract_destination_address(self, text: str) -> Optional[str]:
        """Extract destination/delivery address."""
        # Look for consignee address
        pattern = r'CONSIGNEE[^\n]*\n\s*([^\n]+(?:\n[^\n]+)?)'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return clean_text(match.group(1))
        return None

    def _extract_customer_info(self, text: str) -> None:
        """Extract customer/member information."""
        rank, pay_grade = extract_rank_and_grade(text)

        self.data["customer"] = {
            "name": self._extract_property_owner_name(text),
            "rank": rank,
            "pay_grade": pay_grade,
            "service_branch": self._extract_service_branch(text),
            "ssn_last_four": self._extract_ssn_redacted(text),
            "issuing_officer": extract_field_value(text, "ISSUING OFFICER"),
            "department_agency": extract_field_value(text, "DEPARTMENT/AGENCY"),
        }

    def _extract_property_owner_name(self, text: str) -> Optional[str]:
        """Extract property owner's name."""
        # Look for name in "PROPERTY OWNER'S NAME" field
        pattern = r"PROPERTY OWNER'?S NAME[^\n]*\n\s*([A-Z]+,\s*[A-Z]+)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None

    def _extract_service_branch(self, text: str) -> Optional[str]:
        """Extract military service branch."""
        branches = [
            "United States Air Force",
            "United States Army",
            "United States Navy",
            "United States Marine Corps",
            "United States Coast Guard",
            "United States Space Force",
        ]
        for branch in branches:
            if branch in text:
                return branch
        return None

    def _extract_ssn_redacted(self, text: str) -> Optional[str]:
        """Extract redacted SSN (usually shown as XXX-XX-XXXX)."""
        pattern = r'XXX-XX-(\d{4})'
        match = re.search(pattern, text)
        if match:
            return f"XXX-XX-{match.group(1)}"
        return None

    def _extract_inventory(self, text: str) -> None:
        """Extract inventory/items list."""
        description = self._extract_shipment_description(text)

        self.data["inventory"] = {
            "description": description,
            "package_count": self._extract_package_count(text),
            "package_type": self._extract_package_type(text),
            "containers": self._extract_container_count(text),
            "protection_type": self._extract_protection_type(text),
        }

    def _extract_shipment_description(self, text: str) -> Optional[str]:
        """Extract description of shipment."""
        pattern = r'DESCRIPTION OF SHIPMENT[^\n]*\n\s*([^\n]+(?:\n(?!\d+\.|GROSS|TARE|NET)[^\n]+)*)'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return clean_text(match.group(1))
        return None

    def _extract_package_count(self, text: str) -> Optional[str]:
        """Extract number of packages."""
        # Look in PACKAGES section
        pattern = r'PACKAGES.*?NO\.\s*KIND.*?\n\s*(\d+)'
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1)
        return None

    def _extract_package_type(self, text: str) -> Optional[str]:
        """Extract type of package (LOT, CRATE, etc.)."""
        pattern = r'PACKAGES.*?NO\.\s*KIND.*?\n\s*\d+\s+([A-Z]+)'
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1)
        return None

    def _extract_container_count(self, text: str) -> Optional[str]:
        """Extract number of containers."""
        pattern = r'Containers:\s*(\d+)'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
        return None

    def _extract_protection_type(self, text: str) -> Optional[str]:
        """Extract protection/valuation type."""
        pattern = r'released at\s+([^\.]+protection[^\.]*)'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return clean_text(match.group(1))
        return None

    def _extract_charges(self, text: str) -> None:
        """Extract financial information and charges."""
        self.data["charges"] = {
            "bill_to_name": self._extract_bill_to(text),
            "bill_to_address": self._extract_bill_to_address(text),
        }

    def _extract_bill_to(self, text: str) -> Optional[str]:
        """Extract billing party name."""
        pattern = r'BILL CHARGES TO[^\n]*\n\s*([^\n]+)'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return clean_text(match.group(1))
        return None

    def _extract_bill_to_address(self, text: str) -> Optional[str]:
        """Extract billing address."""
        pattern = r'BILL CHARGES TO[^\n]*\n[^\n]+\n\s*([^\n]+(?:\n[^\n]+)?)'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            addr = match.group(1)
            # Clean up and get multi-line address
            lines = [line.strip() for line in addr.split('\n') if line.strip()]
            return ', '.join(lines)
        return None

    def _extract_administrative_codes(self, text: str) -> None:
        """Extract administrative codes (SDN, AIN, TAC, etc.)."""
        self.data["administrative_codes"] = {
            "sdn": extract_code_field(text, "SDN"),
            "ain": extract_code_field(text, "AIN"),
            "di": extract_code_field(text, "DI"),
            "tac": extract_code_field(text, "TAC"),
            "sac": extract_code_field(text, "SAC"),
            "mdc": extract_code_field(text, "MDC"),
            "transportation_control_no": extract_field_value(text, "TRANSPORTATION CONTROL NO"),
        }

    def to_dict(self) -> Dict[str, Any]:
        """Return the parsed data as a dictionary."""
        return self.data

    def __repr__(self) -> str:
        """String representation of the parser."""
        return f"GBLParser(file='{self.file_path.name}', parsed={bool(self.data)})"
