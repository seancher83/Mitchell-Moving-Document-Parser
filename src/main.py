#!/usr/bin/env python3
"""
Mitchell Moving Document Parser - Main Entry Point

This tool parses Government Bill of Lading (GBL) documents and extracts
structured data for further processing.
"""

import argparse
import sys
import json
from pathlib import Path

# Handle imports for both direct execution and module execution
try:
    from .parsers.gbl_parser import GBLParser
    from .extractors.output_exporter import OutputExporter
except ImportError:
    from parsers.gbl_parser import GBLParser
    from extractors.output_exporter import OutputExporter


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Parse Government Bill of Lading (GBL) documents"
    )

    parser.add_argument(
        "--input",
        "-i",
        type=str,
        required=True,
        help="Input file path or directory containing GBL documents"
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="data/output",
        help="Output directory for parsed data (default: data/output)"
    )

    parser.add_argument(
        "--format",
        "-f",
        type=str,
        choices=["json", "csv", "excel"],
        default="json",
        help="Output format (default: json)"
    )

    parser.add_argument(
        "--batch",
        action="store_true",
        help="Process all files in the input directory"
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    return parser.parse_args()


def main():
    """Main entry point for the GBL parser."""
    args = parse_arguments()

    print("Mitchell Moving Document Parser")
    print("=" * 50)
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    print(f"Format: {args.format}")
    print(f"Batch mode: {args.batch}")
    print("=" * 50)

    # Validate input path
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input path '{args.input}' does not exist", file=sys.stderr)
        sys.exit(1)

    # Create output directory if it doesn't exist
    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)

    # Collect files to process
    files_to_process = []
    if args.batch and input_path.is_dir():
        files_to_process = list(input_path.glob("*.pdf"))
    elif input_path.is_file():
        files_to_process = [input_path]
    else:
        print(f"Error: Invalid input path '{args.input}'", file=sys.stderr)
        sys.exit(1)

    if not files_to_process:
        print("No PDF files found to process.", file=sys.stderr)
        sys.exit(1)

    print(f"\nProcessing {len(files_to_process)} file(s)...\n")

    # Process each file
    results = []
    for pdf_file in files_to_process:
        try:
            if args.verbose:
                print(f"Processing: {pdf_file.name}")

            # Parse the GBL document
            parser = GBLParser(str(pdf_file))
            data = parser.parse()

            # Remove raw_text from output unless verbose
            if not args.verbose and "raw_text" in data:
                del data["raw_text"]

            results.append({
                "file_name": pdf_file.name,
                "data": data
            })

            print(f"✓ Successfully parsed: {pdf_file.name}")

        except Exception as e:
            print(f"✗ Error parsing {pdf_file.name}: {str(e)}", file=sys.stderr)
            if args.verbose:
                import traceback
                traceback.print_exc()

    # Export results
    if results:
        exporter = OutputExporter(output_path)
        output_file = exporter.export(results, args.format)
        print(f"\n✓ Results exported to: {output_file}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
