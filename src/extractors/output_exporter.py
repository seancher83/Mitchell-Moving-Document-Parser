"""Output exporter for GBL parsed data."""

import json
import csv
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


class OutputExporter:
    """Export parsed GBL data to various formats."""

    def __init__(self, output_dir: Path):
        """
        Initialize the exporter.

        Args:
            output_dir: Directory to save output files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export(self, results: List[Dict[str, Any]], format_type: str = "json") -> str:
        """
        Export results to specified format.

        Args:
            results: List of parsed GBL data
            format_type: Output format (json, csv, excel)

        Returns:
            Path to the exported file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if format_type == "json":
            return self._export_json(results, timestamp)
        elif format_type == "csv":
            return self._export_csv(results, timestamp)
        elif format_type == "excel":
            return self._export_excel(results, timestamp)
        else:
            raise ValueError(f"Unsupported format: {format_type}")

    def _export_json(self, results: List[Dict[str, Any]], timestamp: str) -> str:
        """Export to JSON format."""
        output_file = self.output_dir / f"gbl_parsed_{timestamp}.json"

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        return str(output_file)

    def _export_csv(self, results: List[Dict[str, Any]], timestamp: str) -> str:
        """Export to CSV format."""
        output_file = self.output_dir / f"gbl_parsed_{timestamp}.csv"

        if not results:
            return str(output_file)

        # Flatten the nested structure for CSV
        rows = []
        for result in results:
            file_name = result.get("file_name", "")
            data = result.get("data", {})

            row = {
                "file_name": file_name,
                "num_pages": data.get("num_pages", ""),
            }

            # Add header info
            header = data.get("header", {})
            row.update({
                "gbl_number": header.get("gbl_number", ""),
                "date_bl_printed": header.get("date_bl_printed", ""),
                "shipment_number": header.get("shipment_number", ""),
                "scac_code": header.get("scac_code", ""),
                "service_code": header.get("service_code", ""),
                "transportation_company": header.get("transportation_company", ""),
                "gbloc_codes": ", ".join(header.get("gbloc_codes", [])),
            })

            # Add customer info
            customer = data.get("customer", {})
            row.update({
                "customer_name": customer.get("name", ""),
                "rank": customer.get("rank", ""),
                "pay_grade": customer.get("pay_grade", ""),
                "service_branch": customer.get("service_branch", ""),
                "issuing_officer": customer.get("issuing_officer", ""),
                "department_agency": customer.get("department_agency", ""),
            })

            # Add shipment details
            shipment = data.get("shipment", {})
            row.update({
                "origin": shipment.get("origin", ""),
                "destination": shipment.get("destination", ""),
                "requested_packing_date": shipment.get("requested_packing_date", ""),
                "requested_pickup_date": shipment.get("requested_pickup_date", ""),
                "required_delivery_date": shipment.get("required_delivery_date", ""),
                "date_of_receipt": shipment.get("date_of_receipt", ""),
                "authority": shipment.get("authority", ""),
                "date_of_order": shipment.get("date_of_order", ""),
            })

            # Add inventory
            inventory = data.get("inventory", {})
            row.update({
                "package_count": inventory.get("package_count", ""),
                "package_type": inventory.get("package_type", ""),
                "containers": inventory.get("containers", ""),
                "protection_type": inventory.get("protection_type", ""),
                "shipment_description": inventory.get("description", ""),
            })

            # Add charges
            charges = data.get("charges", {})
            row.update({
                "bill_to_name": charges.get("bill_to_name", ""),
                "bill_to_address": charges.get("bill_to_address", ""),
            })

            # Add administrative codes
            admin = data.get("administrative_codes", {})
            row.update({
                "sdn": admin.get("sdn", ""),
                "ain": admin.get("ain", ""),
                "di": admin.get("di", ""),
                "tac": admin.get("tac", ""),
                "sac": admin.get("sac", ""),
                "mdc": admin.get("mdc", ""),
            })

            rows.append(row)

        # Write CSV
        if rows:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)

        return str(output_file)

    def _export_excel(self, results: List[Dict[str, Any]], timestamp: str) -> str:
        """Export to Excel format."""
        try:
            import pandas as pd
        except ImportError:
            raise ImportError(
                "pandas and openpyxl are required for Excel export. "
                "Install with: pip install pandas openpyxl"
            )

        output_file = self.output_dir / f"gbl_parsed_{timestamp}.xlsx"

        # Create a DataFrame for each section
        all_data = []
        for result in results:
            file_name = result.get("file_name", "")
            data = result.get("data", {})

            # Flatten data similar to CSV
            flattened = {"file_name": file_name}

            # Add all sections
            for section in ["header", "customer", "shipment", "inventory", "charges", "administrative_codes"]:
                section_data = data.get(section, {})
                for key, value in section_data.items():
                    if isinstance(value, list):
                        flattened[f"{section}_{key}"] = ", ".join(str(v) for v in value)
                    else:
                        flattened[f"{section}_{key}"] = value

            all_data.append(flattened)

        df = pd.DataFrame(all_data)
        df.to_excel(output_file, index=False, engine='openpyxl')

        return str(output_file)
