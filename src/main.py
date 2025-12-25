#!/usr/bin/env python3
"""
Mitchell Moving Document Parser - Main Entry Point

This tool parses Government Bill of Lading (GBL) documents and extracts
structured data for further processing.
"""

import argparse
import sys
from pathlib import Path


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

    # TODO: Implement actual parsing logic
    print("\nParser implementation coming soon...")
    print("Please add your sample GBL document to data/input/")

    return 0


if __name__ == "__main__":
    sys.exit(main())
