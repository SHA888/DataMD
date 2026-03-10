# Data Markdown (DataMD)

DataMD is an enhanced Markdown format that allows embedding and processing various data formats directly within Markdown documents using the `.dmd` file extension. A Rust implementation is planned to deliver higher performance and a single-binary distribution while preserving full `.dmd` compatibility and offering optional Python bindings.

## Features (Current Python Engine)

DataMD supports embedding and processing:

- **Tabular Data**: CSV, JSON, Excel (XLSX, XLS, XLSM, ODS)
- **Documents**: PDF text extraction and table extraction
- **Images**: OCR text extraction from images
- **Videos**: Video embedding and thumbnail generation
- **Charts**: Data visualization with customizable charts
- **Structured Data**: Custom data transformations and filtering
- **Security**: Path validation and input sanitization
- **Performance**: Caching and large file optimization

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
{{ pdf_table "report.pdf" 2 lines text snap=3 edge=5 intersect=2 }}  # With threshold parameters
```

### Chart Generation
Create visualizations from data files:
```
{{ chart "data/sales.csv" bar month sales title="Monthly Sales" }}
{{ chart "data/profit.xlsx" line month profit xlabel="Month" ylabel="Profit ($)" }}
{{ chart "data/market.json" pie category value title="Market Share" }}
```

### Data Transformations
Apply filtering, sorting, and aggregation to data:
```
{{ csv "data/customers.csv" "," "filter:age>25|sort:name|limit:10" }}
{{ json "data/sales.json" true "groupby:region|sum:sales" }}
```

### Configuration System
Customize behavior with JSON configuration files and environment variables.

### Caching
Automatic caching of processed data with intelligent invalidation.

### CLI Enhancements
Customizable output styling and verbose mode:
```bash
python python_implementation/process_dmd.py report.dmd -v --style-body "font-family: Arial;"
```

### Large File Handling
Optimized processing for large data files with memory management.

## Migration to Rust (Planned)

- Target: 10x performance on large files, safer concurrency, single binary
- Backward compatibility: `.dmd` syntax and outputs remain the same
- Python interoperability: PyO3 bindings planned for programmatic use
- Timeline and phases: see `docs/MIGRATION_FROM_PYTHON.md` and `docs/RUST_ARCHITECTURE.md`

## Installation (Python engine)

```bash
pip install -r requirements.txt
```

For live rebuilds:
```bash
pip install .[watch]
```

## Usage (Python engine)

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

### Verbose mode with custom styling:
```bash
python python_implementation/process_dmd.py report.dmd -v --style-body "font-family: Arial; max-width: 1000px;"
```

## Advanced Usage

- Advanced features: [docs/ADVANCED_USAGE.md](docs/ADVANCED_USAGE.md)
- Syntax reference: [docs/SYNTAX.md](docs/SYNTAX.md)
- API docs (Python): [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)
- Extending shortcodes: [docs/EXTENDING_SHORTCODES.md](docs/EXTENDING_SHORTCODES.md)
- Migration guide: [docs/MIGRATION_FROM_PYTHON.md](docs/MIGRATION_FROM_PYTHON.md)
- Rust architecture outline: [docs/RUST_ARCHITECTURE.md](docs/RUST_ARCHITECTURE.md)

## Examples

See the [examples/](examples/) directory for sample DataMD files:
- [Basic example](examples/example.dmd)
- [Comprehensive example](examples/comprehensive_example.dmd)
- [Video example](examples/video_example.dmd)
- [Chart example](examples/chart_example.dmd)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
