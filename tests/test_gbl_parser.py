"""Tests for GBL Parser"""

import pytest
from pathlib import Path
from src.parsers.gbl_parser import GBLParser


class TestGBLParser:
    """Test cases for GBL parser functionality."""

    def test_parser_initialization_with_valid_file(self, tmp_path):
        """Test that parser initializes with a valid PDF file."""
        # Create a temporary PDF file
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_text("dummy content")

        # This will fail with actual parsing, but tests initialization
        parser = GBLParser(str(pdf_file))
        assert parser.file_path.exists()
        assert parser.file_path.suffix == ".pdf"

    def test_parser_initialization_with_missing_file(self):
        """Test that parser raises error for missing file."""
        with pytest.raises(FileNotFoundError):
            GBLParser("nonexistent_file.pdf")

    def test_parser_initialization_with_non_pdf_file(self, tmp_path):
        """Test that parser raises error for non-PDF files."""
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("not a pdf")

        with pytest.raises(ValueError, match="Only PDF files are supported"):
            GBLParser(str(txt_file))

    def test_parser_repr(self, tmp_path):
        """Test string representation of parser."""
        pdf_file = tmp_path / "sample.pdf"
        pdf_file.write_text("dummy")

        parser = GBLParser(str(pdf_file))
        assert "sample.pdf" in repr(parser)
        assert "GBLParser" in repr(parser)

    # TODO: Add tests for actual parsing once we have sample GBL documents
    # def test_parse_gbl_header(self):
    #     """Test parsing of GBL header information."""
    #     pass
    #
    # def test_parse_shipment_details(self):
    #     """Test parsing of shipment details."""
    #     pass
    #
    # def test_parse_customer_info(self):
    #     """Test parsing of customer information."""
    #     pass
