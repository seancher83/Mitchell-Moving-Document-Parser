# Mitchell Moving Document Parser

## Project Overview

This project is designed to parse and process documents related to Mitchell Moving services. The parser extracts structured data from various moving-related documents such as quotes, invoices, inventory lists, and customer information.

## Project Purpose

- Parse moving-related documents (PDFs, images, text files)
- Extract key information (customer details, inventory, pricing, dates)
- Convert unstructured document data into structured formats
- Automate data entry and document processing workflows

## Technology Stack

(To be determined based on implementation)
- Potential technologies: Python, OCR libraries, PDF processing, data extraction frameworks

## Project Structure

```
Mitchell-Moving-Document-Parser/
├── src/                    # Source code
│   ├── parsers/           # Document parser modules
│   ├── extractors/        # Data extraction logic
│   ├── utils/             # Utility functions
│   └── main.py            # Main entry point
├── tests/                 # Test files
├── data/                  # Sample documents and test data
│   ├── input/            # Input documents
│   └── output/           # Processed output
├── config/               # Configuration files
├── requirements.txt      # Python dependencies
└── README.md            # User-facing documentation
```

## Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose

### Testing
- Write unit tests for all parser functions
- Include integration tests for end-to-end workflows
- Test with various document formats and edge cases
- Maintain test coverage above 80%

### Document Processing Pipeline
1. **Input**: Load document (PDF, image, or text)
2. **Preprocessing**: Clean and normalize document
3. **Extraction**: Extract text and data using OCR/parsing
4. **Parsing**: Apply business logic to extract structured data
5. **Validation**: Verify extracted data quality
6. **Output**: Export to desired format (JSON, CSV, database)

## Common Tasks

### Setup Development Environment
```bash
# Clone the repository
git clone <repository-url>
cd Mitchell-Moving-Document-Parser

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Parser
```bash
# Parse a single document
python src/main.py --input data/input/document.pdf --output data/output/

# Batch process documents
python src/main.py --batch data/input/ --output data/output/
```

### Testing
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_parsers.py
```

## Key Features to Implement

- [ ] PDF document parser
- [ ] OCR for scanned documents
- [ ] Invoice data extraction
- [ ] Quote/estimate parsing
- [ ] Customer information extraction
- [ ] Inventory list processing
- [ ] Date and location parsing
- [ ] Price and payment term extraction
- [ ] Export to multiple formats (JSON, CSV, Excel)
- [ ] Error handling and logging
- [ ] API endpoint for document processing
- [ ] Web interface for document upload

## Data to Extract

### Customer Information
- Name, contact details
- GBL Number
- Start Date
- RDD Date
- Pickup and delivery addresses

### Moving Details
- Move date(s)
- Origin and destination
- Distance
- Special requirements

### Inventory
- Item descriptions
- Quantities
- Dimensions/weights
- Special handling notes

### Financial
- Quote/estimate amounts
- Actual charges
- Payment terms
- Itemized costs

## Working with Claude Code

### Context for AI Assistance
When working with Claude on this project:
- This is a document parsing system for moving company documents
- Focus on accuracy and data quality in extraction
- Consider various document formats (typed, handwritten, scanned)
- Handle edge cases and malformed documents gracefully
- Prioritize maintainable and testable code

### Useful Prompts
- "Add OCR support for scanned invoices"
- "Create a parser for Mitchell Moving quote PDFs"
- "Extract customer addresses from documents"
- "Add validation for extracted phone numbers and emails"
- "Write tests for the invoice parser"
- "Handle edge cases where dates are in different formats"

## Dependencies

Key libraries to consider:
- `PyPDF2` or `pdfplumber` - PDF parsing
- `pytesseract` - OCR for scanned documents
- `pandas` - Data manipulation
- `python-dateutil` - Date parsing
- `regex` - Pattern matching
- `pytest` - Testing framework

## Configuration

Configuration files should include:
- Document type patterns
- Field extraction rules
- Validation criteria
- Output format specifications
- Logging levels

## Error Handling

- Log all parsing errors with document context
- Continue processing batch jobs even if individual documents fail
- Provide detailed error messages for debugging
- Create error reports for manual review

## Future Enhancements

- Machine learning for improved extraction accuracy
- Support for additional document types
- Real-time document processing API
- Integration with moving company CRM/ERP systems
- Automated quality checks and data validation
- Multi-language support
- Cloud deployment options

## Notes

- Keep sensitive customer data secure
- Ensure GDPR/privacy compliance when handling personal information
- Document any business rules specific to Mitchell Moving
- Maintain backward compatibility when updating parsers

---

**Last Updated**: 2025-12-24
**Project Status**: Initial Setup
