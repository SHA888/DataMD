# Data Markdown (DataMD)

DataMD is an enhanced Markdown format that allows embedding and processing various data formats directly within Markdown documents using the `.dmd` file extension.

## Features

DataMD supports embedding and processing:

- **Tabular Data**: CSV, JSON, Excel (XLSX, XLS, XLSM, ODS)
- **Documents**: PDF text extraction and table extraction
- **Images**: OCR text extraction from images
- **Videos**: Video embedding and thumbnail generation
- **Structured Data**: Custom data transformations and filtering

## New Features Implemented

### Video Thumbnail Generation
Generate thumbnails from videos at specific timecodes with custom dimensions:
```
{{ video_thumb "clip.mp4" 5 }}                  # Thumbnail at 5 seconds
{{ video_thumb "clip.mp4" 10 320 240 }}         # Thumbnail at 10s with custom dimensions
{{ video_thumb "clip.mp4" 15 640 }}             # Width-only (height calculated)
```

### Enhanced PDF Table Extraction
Extract tables from PDFs with advanced strategy options:
```
{{ pdf_table "report.pdf" 2 }}                  # Basic table extraction
{{ pdf_table "report.pdf" 2 lines text }}       # With strategy parameters
```

## Installation

```bash
pip install -r requirements.txt
```

For live rebuilds:
```bash
pip install .[watch]
```

## Usage

### Process a single file:
```bash
python python_implementation/process_dmd.py simple_example.dmd
```

### Process all files in a directory:
```bash
python python_implementation/process_dmd.py .
```

### Live rebuilds:
```bash
python python_implementation/process_dmd.py . --watch
```

## Syntax

See [SYNTAX.md](SYNTAX.md) for detailed syntax reference.

## Examples

See the [examples/](examples/) directory for sample DataMD files.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
