# Data Markdown (DataMD) Syntax Reference

## Shortcode Format

All Data Markdown (DataMD) shortcodes follow this pattern:
```
{{ command "filepath" [arg1] [arg2] [arg3] }}
```

## Supported Commands

### CSV Files
```markdown
{{ csv "data/file.csv" }}
{{ csv "data/file.csv" ";" }}  # Custom separator
```

### JSON Files
```markdown
{{ json "config/data.json" }}
{{ json "config/data.json" true }}  # Flatten to table
```

### Excel Files
```markdown
{{ xlsx "report.xlsx" }}
{{ xlsx "report.xlsx" "Sheet1" }}    # Specific sheet by name
{{ xlsx "report.xlsx" 0 }}           # Specific sheet by index
{{ xls "legacy.xls" }}               # Legacy Excel format
{{ xlsm "macro.xlsm" }}              # Macro-enabled Excel
{{ ods "calc.ods" }}                 # OpenDocument Spreadsheet
```

### PDF Files
```markdown
{{ pdf "document.pdf" }}             # All pages
{{ pdf "document.pdf" 1 }}           # Specific page
{{ pdf_table "report.pdf" 2 }}       # Extract tables from page 2
{{ pdf_table "report.pdf" 2 lines text }}  # Extract tables with specific strategies
{{ pdf_table "report.pdf" 2 lines text snap=3 edge=5 intersect=2 }}  # Extract tables with threshold parameters
```

### Images (OCR)
```markdown
{{ image_ocr "scan.jpg" }}           # English (default)
{{ image_ocr "scan.jpg" "spa" }}     # Spanish
{{ image_ocr "scan.jpg" "fra" }}     # French
```

### Videos
```markdown
{{ video "clip.mp4" }}                           # Default size
{{ video "clip.mp4" 800 600 }}                  # Custom dimensions
{{ video "clip.mp4" 800 600 true false }}       # With controls, no autoplay
{{ video_thumb "clip.mp4" 5 }}                  # Thumbnail at 5 seconds
{{ video_thumb "clip.mp4" 10 320 240 }}         # Thumbnail at 10s with custom dimensions
```

### Charts
```markdown
{{ chart "data/sales.csv" bar month sales title="Monthly Sales" }}
{{ chart "data/profit.xlsx" line month profit xlabel="Month" ylabel="Profit ($)" }}
{{ chart "data/market.json" pie category value title="Market Share" }}
```

## Language Codes for OCR

- `eng` - English
- `spa` - Spanish
- `fra` - French
- `deu` - German
- `chi_sim` - Chinese Simplified
- `jpn` - Japanese
- `rus` - Russian
- `ara` - Arabic

*Note: Language packs must be installed in Tesseract*

## PDF Table Extraction Strategies

- `lines` - Detect tables based on lines (default)
- `text` - Detect tables based on text alignment
- `explicit` - Use explicit table boundaries

## PDF Table Detection Thresholds

Table detection sensitivity can be controlled with the following optional parameters:

- `snap=N` - Controls how close lines must be to be considered part of the same table (default: 3)
- `edge=N` - Controls how close edges must be to be considered part of the same table (default: 5)
- `intersect=N` - Controls how close edges must be to be considered intersecting (default: 2)

Example:
```markdown
{{ pdf_table "report.pdf" 1 lines text snap=5 edge=10 intersect=3 }}
```

## Chart Parameters

The `chart` shortcode takes the following parameters:
- `chart_type` (required) - Type of chart to generate (bar, line, pie, scatter, histogram)
- `x_column` (optional) - Column to use for X-axis values
- `y_column` (optional) - Column to use for Y-axis values
- `options` (optional) - Additional options in key=value format separated by spaces

### Supported Chart Types

- `bar` - Bar chart (default)
- `line` - Line chart
- `pie` - Pie chart
- `scatter` - Scatter plot
- `histogram` - Histogram

### Chart Options

- `title="Chart Title"` - Chart title
- `xlabel="X Label"` - X-axis label
- `ylabel="Y Label"` - Y-axis label
- `transform="filter:age>25|sort:name"` - Data transformations to apply before charting

Example:
```markdown
{{ chart "data/sales.csv" bar month sales title="Monthly Sales" xlabel="Month" ylabel="Sales ($)" }}
```

## File Path Guidelines

- Paths are relative to the .dmd file location
- Use forward slashes (/) for cross-platform compatibility
- Enclose paths in double quotes
- Ensure files exist before rendering

## Video Thumbnail Parameters

The `video_thumb` shortcode takes the following parameters:
- `time` (required) - Time in seconds to extract the frame
- `width` (optional) - Width of the thumbnail in pixels
- `height` (optional) - Height of the thumbnail in pixels

If only one dimension is provided, the other will be calculated to maintain aspect ratio.
If no dimensions are provided, the original frame dimensions are used.

## CLI Options

The DataMD processor supports the following command-line options:

### Basic Options
- `input` - Input .dmd file or directory (required)
- `-o, --output` - Output HTML file (for single file processing)
- `--watch` - Watch for file changes (requires watchdog)
- `--config` - Path to configuration file

### Output Format Options
- `-f, --format` - Output format (currently only HTML is supported)
- `--style-body` - Custom CSS for body element
- `--style-table` - Custom CSS for table elements
- `--style-cell` - Custom CSS for table cell elements
- `--style-header` - Custom CSS for table header elements
- `--style-pre` - Custom CSS for pre elements
- `--style-video` - Custom CSS for video elements
- `--style-img` - Custom CSS for img elements

### Debugging Options
- `-v, --verbose` - Enable verbose output

Example:
```bash
python process_dmd.py report.dmd -v --style-body "font-family: Arial; max-width: 1000px;"
```
