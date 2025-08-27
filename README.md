# Data Markdown (DataMD) - Enhanced Markdown with Data Format Support

Data Markdown (DataMD) is a powerful Markdown flavor that supports embedding and processing various data formats directly in your documents using the `.dmd` extension.

There are two ways to render Data Markdown, with the Python-only engine being the primary path:

- Python-only engine (CLI `datamd`) that processes `.dmd` directly without Quarto.
- Optional Quarto integration (uses `datamd.lua` to inject executable Python chunks). Note: Quarto does not execute `.dmd` directly; use a `.qmd` copy.

## Supported Formats

- **CSV** - Tabular data rendered as Markdown tables
- **JSON** - Structured data displayed as tables or formatted JSON
- **XLSX** (and variants: .xls, .xlsm, .ods) - Excel spreadsheets as tables
- **PDF** - Text extraction and display
- **Images** - OCR text extraction from images (PNG, JPG, etc.)
- **MP4 Videos** - Embedded video players

## Installation

### Prerequisites

1. **Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Optional: enable live rebuilds support
   ```bash
   # install optional extras for file watching
   pip install .[watch]
   ```

2. Optional — **Quarto** (for Quarto-based rendering):
   - Download: https://quarto.org/docs/get-started/
   - Linux .deb quick install:
     ```bash
     curl -LO https://quarto.org/download/latest/quarto-linux-amd64.deb
     sudo dpkg -i quarto-linux-amd64.deb || sudo apt-get -f install -y
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

4. Optional — **FFmpeg** (for video/thumbnail helpers):
   ```bash
   sudo apt-get install ffmpeg
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

You can render using the primary Python engine (`datamd`) or, optionally, via Quarto (using a `.qmd` copy).

> Live rebuilds: run with `--watch` (requires `watchdog`).

### Option A: Python-only engine (primary)

Use the custom processor in `python_implementation/` (exposed via the `datamd` CLI) to execute shortcodes and emit HTML directly from `.dmd`:

```bash
# Single file
python python_implementation/process_dmd.py simple_example.dmd
# Output: simple_example.html
```

Project-level rendering can process all `.dmd` files in a directory as well:

```bash
# Process all .dmd files in a directory
python python_implementation/process_dmd.py .

### Option B: Optional Quarto integration

Quarto only executes `.qmd` and `.ipynb`. For a `.dmd` file, copy it to `.qmd` and render:

```bash
# Single file
cp simple_example.dmd simple_example.qmd
quarto render simple_example.qmd --to html
# Output: simple_example.html
```

Notes:
- The project config `_quarto.yml` includes the `datamd.lua` filter.
- The document should include front matter with an engine, e.g.:
  ```yaml
  ---
  title: "My DataMD Report"
  engine: jupyter
  format: html
  ---
  ```
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
└── *.dmd               # Your Data Markdown (DataMD) files
```

## Alternative: Python-Only Implementation

For environments without Quarto, use the Python-only engine described above (see `python_implementation/` directory).
