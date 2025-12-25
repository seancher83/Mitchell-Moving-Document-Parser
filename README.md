# Mitchell Moving Document Parser

A Python-based parser for Government Bill of Lading (GBL) documents used in military and government relocations.

## Overview

This tool extracts structured data from GBL PDF documents, converting unstructured forms into machine-readable formats (JSON, CSV, Excel) for further processing and analysis.

## Features

- Parse Government Bill of Lading (GBL) PDF documents
- Extract key information:
  - GBL number and dates
  - Shipment origin and destination
  - Customer/member information
  - Inventory items and weights
  - Charges and pricing
- Export to multiple formats (JSON, CSV, Excel)
- Batch processing support
- OCR support for scanned documents

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Mitchell-Moving-Document-Parser
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. For OCR support, install Tesseract:
- **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
- **macOS**: `brew install tesseract`
- **Windows**: Download from [Tesseract GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

## Usage

### Parse a Single GBL Document

```bash
python src/main.py --input data/input/sample_gbl.pdf --output data/output
```

### Parse Multiple Documents (Batch Mode)

```bash
python src/main.py --input data/input/ --output data/output --batch
```

### Specify Output Format

```bash
# Output as JSON (default)
python src/main.py -i data/input/gbl.pdf -o data/output -f json

# Output as CSV
python src/main.py -i data/input/gbl.pdf -o data/output -f csv

# Output as Excel
python src/main.py -i data/input/gbl.pdf -o data/output -f excel
```

### Enable Verbose Logging

```bash
python src/main.py -i data/input/gbl.pdf -o data/output --verbose
```

## Project Structure

```
Mitchell-Moving-Document-Parser/
├── src/
│   ├── __init__.py
│   ├── main.py              # Main entry point
│   ├── parsers/
│   │   ├── __init__.py
│   │   └── gbl_parser.py    # GBL document parser
│   ├── extractors/          # Data extraction utilities
│   │   └── __init__.py
│   └── utils/               # Helper functions
│       └── __init__.py
├── tests/                   # Unit tests
│   ├── __init__.py
│   └── test_gbl_parser.py
├── data/
│   ├── input/              # Place your GBL PDFs here
│   └── output/             # Parsed output files
├── config/                 # Configuration files
├── requirements.txt        # Python dependencies
├── pytest.ini             # Test configuration
├── CLAUDE.MD              # AI assistant documentation
└── README.md              # This file
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src tests/

# Run specific test file
pytest tests/test_gbl_parser.py
```

### Adding Sample Documents

Place your GBL PDF documents in the `data/input/` directory:

```bash
cp /path/to/your/gbl_document.pdf data/input/
```

### Code Style

This project follows PEP 8 style guidelines. Use tools like `black` and `flake8` for formatting:

```bash
pip install black flake8
black src/ tests/
flake8 src/ tests/
```

## GBL Data Structure

The parser extracts the following information from GBL documents:

### Header Information
- GBL number
- Issue date
- Effective date

### Shipment Details
- Origin location
- Destination location
- Pickup date
- Delivery date
- Service type

### Customer Information
- Name
- Rank/Grade
- Service branch
- Contact phone
- Contact email

### Inventory
- Total items count
- Total weight
- Individual items list

### Charges
- Base transportation rate
- Additional charges
- Total amount

## Troubleshooting

### PDF Parsing Issues

If you encounter issues parsing a PDF:
1. Ensure the PDF is not password-protected
2. Try using OCR for scanned documents (requires Tesseract)
3. Check if the PDF has extractable text: `pdftotext your_file.pdf -`

### Missing Dependencies

If you get import errors:
```bash
pip install -r requirements.txt --upgrade
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Add tests for new functionality
4. Ensure all tests pass: `pytest`
5. Submit a pull request

## License

[Add your license here]

## Contact

[Add contact information]

## Next Steps

1. Add your sample GBL document to `data/input/`
2. Review the parsed output structure
3. Customize extraction rules based on your specific GBL format
4. Add validation rules for extracted data

For detailed AI assistant documentation, see [CLAUDE.MD](CLAUDE.MD).
