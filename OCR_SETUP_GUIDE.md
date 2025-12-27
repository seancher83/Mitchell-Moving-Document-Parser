# OCR Setup Guide for Scanned GBL Documents

## Overview

The Mitchell Moving Document Parser now automatically detects whether a GBL PDF is **text-based** or a **scanned image**, and uses the appropriate extraction method:

- **Text-based PDFs** (80% of samples): Use fast, accurate text extraction
- **Scanned PDFs** (20% of samples): Use OCR (Optical Character Recognition) with coordinate-based field extraction

## Detection Results

From your 10 sample GBLs:
- ✅ **8 samples** are text-based (fast extraction)
- 🖼️  **2 samples** (Sample 8, Sample 10) are scanned images (require OCR)

## How Detection Works

The parser automatically:
1. **Detects PDF type** by checking text content length
   - Text-based: >500 characters per page
   - Scanned: <100 characters per page
2. **Chooses extraction method** based on detection
   - Text-based → Standard text extraction (current method)
   - Scanned → OCR + coordinate-based extraction

## Installing OCR Support

### Step 1: Install Python Packages

```bash
pip install pytesseract pdf2image Pillow
```

### Step 2: Install Tesseract OCR Engine

#### macOS:
```bash
brew install tesseract
```

#### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install poppler-utils  # Required for pdf2image
```

#### Windows:
1. Download Tesseract installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer (choose "Add to PATH" option)
3. Download poppler for Windows: http://blog.alivate.com.au/poppler-windows/
4. Extract and add to PATH

#### Verify Installation:
```bash
tesseract --version
```

Should output something like:
```
tesseract 5.x.x
```

## OCR Extraction Features

### 1. Automatic Detection
```python
from parsers.gbl_parser import GBLParser

parser = GBLParser("data/input/GBL Sample 8.pdf")
result = parser.parse()

# Automatically detects scanned image and uses OCR
# Output shows:
# "PDF Type: SCANNED (confidence: high)"
# "→ Using OCR extraction method..."
```

### 2. Coordinate-Based Extraction

For scanned GBLs, the parser uses **template-based extraction** since GBL forms (DD Form 1840) have standardized layouts:

```python
# Approximate field positions (as fraction of page)
FIELD_COORDINATES = {
    'bl_number': (0.75, 0.05, 0.95, 0.10),      # Top right
    'scac': (0.15, 0.12, 0.25, 0.16),           # Header left
    'service_code': (0.35, 0.12, 0.45, 0.16),   # Header center
    'date_bl_printed': (0.55, 0.12, 0.70, 0.16),# Header right
    'packing_date': (0.05, 0.16, 0.20, 0.20),   # Date fields
    # ... more fields
}
```

### 3. Image Enhancement

Before OCR, images are enhanced for better accuracy:
- Convert to grayscale
- Increase contrast (2x)
- Increase sharpness (2x)
- Denoise (median filter)
- High DPI (300) for quality

### 4. Dual Extraction Strategy

OCR extraction uses **two methods** and merges results:

**A. Coordinate-based**: Extracts from known positions on form
**B. Pattern matching**: Uses regex patterns on OCR text (fallback)

## Testing OCR

### Test Detection Only:
```bash
python3 test_ocr_detection.py
```

This shows which samples are scanned vs text-based.

### Test Full Parsing:
```bash
python3 parse_gbl.py --input "data/input/GBL Sample 8.pdf" --output data/output --format json
```

With OCR installed, this will:
1. Detect Sample 8 as scanned
2. Use OCR extraction
3. Apply coordinate-based field extraction
4. Output JSON with extracted data

## Expected Results

### Without OCR (current state):
- Samples 1-7, 9: **100% extraction** (text-based)
- Samples 8, 10: **0% extraction** (scanned, no OCR)
- **Average: 80%**

### With OCR installed:
- Samples 1-7, 9: **100% extraction** (text-based)
- Samples 8, 10: **60-80% extraction** (OCR with template)
- **Average: 90-95%**

## OCR Accuracy Notes

### Factors Affecting OCR Accuracy:

1. **Image Quality** (Most Important)
   - High DPI scans (300+): 90-95% accuracy
   - Low DPI scans (<150): 50-70% accuracy
   - Clear, high-contrast: Better results

2. **Form Condition**
   - Clean, printed forms: 90%+ accuracy
   - Handwritten fields: 30-50% accuracy
   - Faded or damaged: 40-70% accuracy

3. **Field Types**
   - Printed text: 95% accuracy
   - Numbers (B/L, dates, zips): 90% accuracy
   - Checkboxes/marks: 80% accuracy
   - Handwriting: 30-50% accuracy

### Improving OCR Accuracy:

1. **Scan at higher DPI** (300-600 recommended)
2. **Clean, high-contrast scans**
3. **Straight/aligned documents** (not skewed)
4. **Original documents** (not photocopies)

## Troubleshooting

### "OCR libraries not available"
```
⚠️ OCR libraries not available!
Missing packages: pdf2image, pytesseract
```
**Solution**: Run `pip install pytesseract pdf2image Pillow`

### "tesseract is not installed or it's not in your PATH"
```
TesseractNotFoundError: tesseract is not installed
```
**Solution**: Install Tesseract OCR (see Step 2 above)

### "poppler not found"
```
PDFInfoNotInstalledError: Unable to get page count. Is poppler installed?
```
**Solution**:
- Linux: `sudo apt-get install poppler-utils`
- Mac: `brew install poppler`
- Windows: Download from http://blog.alivate.com.au/poppler-windows/

### Poor OCR Results

If OCR extraction is < 50% accurate:
1. Check image quality (should be 300 DPI minimum)
2. Ensure form is straight/aligned
3. Verify Tesseract is properly installed: `tesseract --version`
4. Try increasing DPI in code: `extractor.extract_with_ocr(dpi=600)`

## Alternative: Cloud OCR Services

For production use with high volumes, consider cloud OCR:

### AWS Textract
```python
import boto3

textract = boto3.client('textract')
response = textract.analyze_document(
    Document={'S3Object': {'Bucket': 'my-bucket', 'Name': 'gbl.pdf'}},
    FeatureTypes=['FORMS', 'TABLES']
)
```
- **Pros**: Very high accuracy (95%+), handles handwriting
- **Cons**: Costs money ($1.50 per 1000 pages)

### Google Cloud Vision
```python
from google.cloud import vision

client = vision.ImageAnnotatorClient()
response = client.document_text_detection(image=image)
```
- **Pros**: Excellent accuracy, supports many languages
- **Cons**: Costs money ($1.50 per 1000 pages)

### Azure Form Recognizer
```python
from azure.ai.formrecognizer import DocumentAnalysisClient

client = DocumentAnalysisClient(endpoint, credential)
poller = client.begin_analyze_document("prebuilt-document", document)
```
- **Pros**: Purpose-built for forms, very accurate
- **Cons**: Costs money ($10 per 1000 pages)

## Performance Comparison

| Method | Speed | Accuracy | Cost |
|--------|-------|----------|------|
| **Text Extraction** | 0.1s/page | 100% | Free |
| **Tesseract OCR** | 2-5s/page | 70-90% | Free |
| **AWS Textract** | 1-2s/page | 95-99% | $1.50/1000 |
| **Google Vision** | 1-2s/page | 95-99% | $1.50/1000 |
| **Azure Form Rec** | 2-3s/page | 95-99% | $10/1000 |

## Recommendation

For your use case (80% text-based, 20% scanned):

**Start with Tesseract OCR**:
- Free and open source
- Good enough for clear scans (70-90% accuracy)
- Works offline
- Easy to install and integrate

**Upgrade to cloud OCR if**:
- Processing thousands of documents
- Need >95% accuracy
- Have handwritten fields
- Budget allows ($50-100/month for moderate use)

## Summary

✅ **Detection is implemented and working**
✅ **OCR extraction code is ready**
⏳ **Just need to install OCR dependencies**

To activate OCR for Samples 8 & 10:
```bash
pip install pytesseract pdf2image Pillow
brew install tesseract  # or apt-get/download for your OS
```

Then run: `python3 parse_gbl.py --input "data/input/GBL Sample 8.pdf"`
