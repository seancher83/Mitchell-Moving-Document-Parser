"""OCR-based extraction for scanned GBL documents."""

from typing import Optional, Dict, Any
import re
from pathlib import Path

# OCR dependencies (optional)
try:
    from pdf2image import convert_from_path
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


class GBLFormExtractor:
    """
    Extract data from scanned GBL forms using OCR and coordinate-based extraction.

    GBL forms follow a standardized layout (DD Form 1840), so we can use
    approximate coordinates to extract specific fields.
    """

    # Approximate field coordinates (normalized 0-1 scale)
    # Format: (x_start, y_start, x_end, y_end) as fraction of page width/height
    FIELD_COORDINATES = {
        'bl_number': (0.75, 0.05, 0.95, 0.10),
        'scac': (0.15, 0.12, 0.25, 0.16),
        'service_code': (0.35, 0.12, 0.45, 0.16),
        'date_bl_printed': (0.55, 0.12, 0.70, 0.16),
        'shipment_number': (0.45, 0.12, 0.55, 0.16),
        'packing_date': (0.05, 0.16, 0.20, 0.20),
        'pickup_date': (0.20, 0.16, 0.35, 0.20),
        'delivery_date': (0.35, 0.16, 0.50, 0.20),
        'customer_name': (0.50, 0.16, 0.95, 0.22),
        'origin_address': (0.05, 0.40, 0.50, 0.50),
        'destination_address': (0.50, 0.40, 0.95, 0.50),
    }

    def __init__(self, pdf_path: str):
        """
        Initialize the extractor.

        Args:
            pdf_path: Path to the scanned PDF
        """
        self.pdf_path = pdf_path
        self.full_text = None
        self.images = None

    def extract_with_ocr(self, dpi: int = 300, enhance: bool = True) -> Dict[str, Any]:
        """
        Extract data from scanned GBL using OCR.

        Args:
            dpi: Resolution for PDF to image conversion (higher = better quality, slower)
            enhance: Whether to enhance image before OCR

        Returns:
            Dictionary with extracted data
        """
        if not OCR_AVAILABLE:
            return {
                'error': 'OCR libraries not available. Install with: pip install pytesseract pdf2image Pillow',
                'method': 'ocr',
                'success': False
            }

        try:
            # Convert PDF to images
            print(f"Converting PDF to images at {dpi} DPI...")
            self.images = convert_from_path(self.pdf_path, dpi=dpi)

            if not self.images:
                return {'error': 'No images extracted from PDF', 'success': False}

            # Process first page (GBL is typically single page)
            image = self.images[0]

            if enhance:
                image = self._enhance_image(image)

            # Extract full text
            print("Running OCR on document...")
            self.full_text = pytesseract.image_to_string(image, config='--psm 6')

            # Extract fields using coordinate-based method
            print("Extracting fields using coordinate-based method...")
            coordinate_data = self._extract_by_coordinates(image)

            # Extract fields using text pattern matching on OCR text
            print("Extracting fields using pattern matching...")
            pattern_data = self._extract_by_patterns(self.full_text)

            # Merge results with smart precedence
            # Pattern matching is more reliable for: SCAC, B/L number, dates, zips
            # Coordinate extraction is better for: small fields, specific positions
            merged_data = {**coordinate_data, **pattern_data}

            # For fields where both methods found a value, prefer pattern matching
            # for text-based fields and coordinate extraction for position-specific fields
            reliable_pattern_fields = ['scac', 'bl_number', 'origin_zip', 'destination_zip']
            for field in reliable_pattern_fields:
                if field in pattern_data and pattern_data[field]:
                    merged_data[field] = pattern_data[field]

            merged_data['method'] = 'ocr'
            merged_data['success'] = True
            merged_data['ocr_text_length'] = len(self.full_text)

            return merged_data

        except Exception as e:
            return {
                'error': f'OCR extraction failed: {str(e)}',
                'method': 'ocr',
                'success': False
            }

    def _enhance_image(self, image: 'Image') -> 'Image':
        """
        Enhance image for better OCR results.

        Args:
            image: PIL Image object

        Returns:
            Enhanced PIL Image
        """
        from PIL import ImageEnhance, ImageFilter

        # Convert to grayscale
        image = image.convert('L')

        # Increase contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)

        # Increase sharpness
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(2.0)

        # Denoise
        image = image.filter(ImageFilter.MedianFilter(size=3))

        return image

    def _extract_by_coordinates(self, image: 'Image') -> Dict[str, Any]:
        """
        Extract fields from specific coordinates on the form.

        Args:
            image: PIL Image of the document

        Returns:
            Dictionary with extracted field values
        """
        data = {}
        width, height = image.size

        for field_name, coords in self.FIELD_COORDINATES.items():
            try:
                # Convert normalized coordinates to pixel coordinates
                x1 = int(coords[0] * width)
                y1 = int(coords[1] * height)
                x2 = int(coords[2] * width)
                y2 = int(coords[3] * height)

                # Crop region
                region = image.crop((x1, y1, x2, y2))

                # OCR the region
                text = pytesseract.image_to_string(region, config='--psm 7').strip()

                # Clean and validate
                text = self._clean_field_value(field_name, text)

                if text:
                    data[field_name] = text

            except Exception as e:
                # Continue if a single field fails
                continue

        return data

    def _extract_by_patterns(self, text: str) -> Dict[str, Any]:
        """
        Extract fields using regex patterns on OCR text.

        Args:
            text: OCR extracted text

        Returns:
            Dictionary with extracted values
        """
        # Import extraction functions from text_utils
        # Note: Using relative import might need adjustment based on execution context
        try:
            import sys
            from pathlib import Path
            sys.path.insert(0, str(Path(__file__).parent))
            from text_utils import (
                extract_bl_number,
                extract_scac_code,
                extract_service_code_gbl,
                extract_gbl_dates,
                extract_zip_codes,
                extract_tariff_rates
            )
        except ImportError:
            # Fallback to basic patterns if imports fail
            return self._extract_basic_patterns(text)

        # Use existing extraction functions
        data = {}

        bl_number = extract_bl_number(text)
        if bl_number:
            data['bl_number'] = bl_number

        scac = extract_scac_code(text)
        if scac:
            data['scac'] = scac

        service_code = extract_service_code_gbl(text)
        if service_code:
            data['service_code'] = service_code

        dates = extract_gbl_dates(text)
        data.update(dates)

        zips = extract_zip_codes(text)
        data.update(zips)

        rates = extract_tariff_rates(text)
        data.update(rates)

        return data

    def _extract_basic_patterns(self, text: str) -> Dict[str, Any]:
        """
        Fallback extraction using basic patterns.

        Args:
            text: OCR text

        Returns:
            Dictionary with extracted values
        """
        data = {}

        # B/L Number: 4 letters + 7 digits
        match = re.search(r'\b([A-Z]{4}\d{7})\b', text)
        if match:
            data['bl_number'] = match.group(1)

        # Dates: 8 digits
        dates = re.findall(r'\b(\d{8})\b', text)
        if dates:
            data['dates_found'] = dates

        # Zip codes: 5 digits
        zips = re.findall(r'\b(\d{5})\b', text)
        if zips:
            data['zips_found'] = zips

        return data

    def _clean_field_value(self, field_name: str, value: str) -> Optional[str]:
        """
        Clean and validate field value based on field type.

        Args:
            field_name: Name of the field
            value: Raw OCR value

        Returns:
            Cleaned value or None
        """
        if not value:
            return None

        # Remove extra whitespace
        value = ' '.join(value.split())

        # Field-specific cleaning
        if field_name == 'bl_number':
            # Should be 4 letters + 7 digits
            match = re.search(r'([A-Z]{4}\d{7})', value.upper())
            return match.group(1) if match else None

        elif field_name in ['scac']:
            # Should be 2-4 uppercase letters
            match = re.search(r'([A-Z]{2,4})', value.upper())
            return match.group(1) if match else None

        elif field_name == 'service_code':
            # Single letter
            match = re.search(r'([A-Z])', value.upper())
            return match.group(1) if match else None

        elif 'date' in field_name:
            # Should be 8 digits
            match = re.search(r'(\d{8})', value)
            return match.group(1) if match else None

        elif 'zip' in field_name:
            # Should be 5 digits
            match = re.search(r'(\d{5})', value)
            return match.group(1) if match else None

        return value if len(value) > 0 else None


def check_ocr_availability() -> Dict[str, bool]:
    """
    Check if OCR dependencies are available.

    Returns:
        Dictionary with availability status
    """
    status = {
        'ocr_available': OCR_AVAILABLE,
        'missing_packages': []
    }

    if not OCR_AVAILABLE:
        try:
            import pdf2image
        except ImportError:
            status['missing_packages'].append('pdf2image')

        try:
            import pytesseract
        except ImportError:
            status['missing_packages'].append('pytesseract')

        try:
            from PIL import Image
        except ImportError:
            status['missing_packages'].append('Pillow')

    return status
