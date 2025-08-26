# DataMD - Enhanced Markdown with Data Format Support

DataMD is a powerful Markdown flavor that supports embedding and processing various data formats directly in your documents using the `.dmd` extension.

## Supported Formats

- **CSV** - Tabular data rendered as Markdown tables
- **JSON** - Structured data displayed as tables or formatted JSON
- **XLSX** (and variants: .xls, .xlsm, .ods) - Excel spreadsheets as tables
- **PDF** - Text extraction and display
- **Images** - OCR text extraction from images (PNG, JPG, etc.)
- **MP4 Videos** - Embedded video players

## Installation

### Prerequisites

1. **Quarto** (recommended approach):
   ```bash
   # Download from https://quarto.org/docs/get-started/
   ```

2. **Python Dependencies**:
   ```bash
   pip install pandas openpyxl pdfplumber pytesseract pillow moviepy
   ```

3. **Tesseract OCR** (for image text extraction):
   ```bash
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr
   
   # macOS
   brew install tesseract
   
   # Windows
   # Download from https://github.com/UB-Mannheim/tesseract/wiki
   ```

## Usage

Create files with the `.dmd` extension and use shortcode syntax to embed data:

### CSV Files
```markdown
{{ csv "data/sales.csv" }}
```

### JSON Data
```markdown
{{ json "config/settings.json" }}
```

### Excel Files
```markdown
{{ xlsx "reports/quarterly.xlsx" }}
{{ xlsx "reports/data.xlsm" sheet="Summary" }}
```

### PDF Documents
```markdown
{{ pdf "documents/report.pdf" }}
```

### Image OCR
```markdown
{{ image_ocr "scans/receipt.jpg" }}
```

### Videos
```markdown
{{ video "media/presentation.mp4" }}
```

## Rendering

```bash
# Render a single file
quarto render report.dmd

# Render all .dmd files in project
quarto render
```

## Project Structure

```
your-project/
├── _quarto.yml          # Quarto configuration
├── datamd.lua           # Custom filter for shortcodes
├── requirements.txt     # Python dependencies
├── data/               # Data files
├── documents/          # PDF files
├── media/              # Video files
├── scans/              # Images for OCR
└── *.dmd               # Your DataMD files
```

## Alternative: Python-Only Implementation

For environments without Quarto, use the Python-Markdown extension approach (see `python_implementation/` directory).
