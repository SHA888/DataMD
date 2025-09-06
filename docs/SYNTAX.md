# Data Markdown (DataMD) Syntax Reference

## Shortcode Format

All Data Markdown (DataMD) shortcodes follow this pattern:
```
{{ command "filepath" [arg1] [arg2] [arg3] }}
```

## Configuration

DataMD can be configured through a JSON configuration file, environment variables, or programmatically. The configuration system allows customization of application behavior, feature availability, and processing limits.

### Configuration File

To use a configuration file, pass the `--config` option to the CLI:

```bash
python process_dmd.py document.dmd --config config/app_config.json
```

The configuration file should be a JSON file with the following structure:

```json
{
  "application": {
    "name": "DataMD Processor",
    "version": "1.0.0",
    "environment": "production"
  },
  "features": {
    "ocr_enabled": true,
    "pdf_processing": true,
    "video_support": true,
    "excel_formats": ["xlsx", "xls", "xlsm", "ods"]
  },
  "limits": {
    "max_file_size_mb": 100,
    "max_pages_pdf": 50,
    "supported_languages": ["eng", "spa", "fra", "deu"]
  },
  "processing": {
    "default_csv_separator": ",",
    "default_pdf_strategy": "lines",
    "default_ocr_language": "eng",
    "video_thumb_width": 320,
    "video_thumb_height": 240
  },
  "security": {
    "allow_directory_traversal": false,
    "max_filename_length": 255,
    "allowed_file_extensions": [
      ".csv", ".json", ".xlsx", ".xls", ".xlsm", ".ods",
      ".pdf", ".jpg", ".jpeg", ".png", ".gif", ".bmp",
      ".mp4", ".avi", ".mov", ".wmv"
    ]
  }
}
```

### Environment Variables

Configuration values can also be set using environment variables. The following environment variables are supported:

- `DATAMD_APP_NAME` - Application name
- `DATAMD_APP_VERSION` - Application version
- `DATAMD_ENVIRONMENT` - Environment (production, development, etc.)
- `DATAMD_OCR_ENABLED` - Enable/disable OCR processing (true/false)
- `DATAMD_PDF_PROCESSING` - Enable/disable PDF processing (true/false)
- `DATAMD_VIDEO_SUPPORT` - Enable/disable video support (true/false)
- `DATAMD_MAX_FILE_SIZE_MB` - Maximum file size in MB
- `DATAMD_MAX_PAGES_PDF` - Maximum PDF pages to process
- `DATAMD_DEFAULT_CSV_SEPARATOR` - Default CSV separator
- `DATAMD_DEFAULT_PDF_STRATEGY` - Default PDF table extraction strategy
- `DATAMD_DEFAULT_OCR_LANGUAGE` - Default OCR language
- `DATAMD_ALLOW_DIRECTORY_TRAVERSAL` - Allow directory traversal (security setting)

Environment variables take precedence over configuration file values.

## Caching

DataMD automatically caches the results of expensive operations to improve performance when processing the same files multiple times. The cache system automatically invalidates cached data when source files are modified.

### Cache Directory

By default, DataMD stores cache files in:

- `~/.cache/datamd` on Unix-like systems
- `./cache` in the current directory as a fallback

You can configure the cache directory by setting the `DATAMD_CACHE_DIR` environment variable:

```bash
export DATAMD_CACHE_DIR=/path/to/custom/cache/directory
```

### Cache Invalidation

Cache entries are automatically invalidated when:

- The source file is modified (based on file modification timestamp)
- The processing parameters change

### Cache Management

To clear the cache manually, delete the cache directory:

```bash
rm -rf ~/.cache/datamd
# or if using custom directory
rm -rf /path/to/custom/cache/directory
```

## Supported Commands

### CSV Files
````
{{ csv "data/file.csv" }}
{{ csv "data/file.csv" ";" }}  # Custom separator
```

### JSON Files
```
{{ json "config/data.json" }}
{{ json "config/data.json" true }}  # Flatten to table
```

### Excel Files
```
{{ xlsx "report.xlsx" }}
{{ xlsx "report.xlsx" "Sheet1" }}    # Specific sheet by name
{{ xlsx "report.xlsx" 0 }}           # Specific sheet by index
{{ xls "legacy.xls" }}               # Legacy Excel format
{{ xlsm "macro.xlsm" }}              # Macro-enabled Excel
{{ ods "calc.ods" }}                 # OpenDocument Spreadsheet
```

### PDF Files
```
{{ pdf "document.pdf" }}             # All pages
{{ pdf "document.pdf" 1 }}           # Specific page
{{ pdf_table "report.pdf" 2 }}       # Extract tables from page 2
{{ pdf_table "report.pdf" 2 lines text }}  # Extract tables with specific strategies
{{ pdf_table "report.pdf" 2 lines text snap=3 edge=5 intersect=2 }}  # Extract tables with threshold parameters
```

### Images (OCR)
```
{{ image_ocr "scan.jpg" }}           # English (default)
{{ image_ocr "scan.jpg" "spa" }}     # Spanish
{{ image_ocr "scan.jpg" "fra" }}     # French
{{ image_ocr "scan.jpg" "ind" }}     # Indonesian (Bahasa Indonesia)
```

### Videos
```
{{ video "clip.mp4" }}                           # Default size
{{ video "clip.mp4" 800 600 }}                  # Custom dimensions
{{ video "clip.mp4" 800 600 true false }}       # With controls, no autoplay
{{ video_thumb "clip.mp4" 5 }}                  # Thumbnail at 5 seconds
{{ video_thumb "clip.mp4" 10 320 240 }}         # Thumbnail at 10s with custom dimensions
```

### Charts
```
{{ chart "data/sales.csv" bar month sales title="Monthly Sales" }}
{{ chart "data/profit.xlsx" line month profit xlabel="Month" ylabel="Profit ($)" }}
{{ chart "data/market.json" pie category value title="Market Share" }}
```

## Language Codes for OCR

- `eng` - English
- `spa` - Spanish
- `fra` - French
- `deu` - German
- `ind` - Indonesian (Bahasa Indonesia)
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
```
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
- `color="color"` - Color for the chart elements
- `width=N` - Width of the chart in inches
- `height=N` - Height of the chart in inches
- `alpha=N` - Transparency level (0.0 to 1.0)
- `grid=true` - Show grid lines
- `linestyle="-"` - Line style for line charts (-, --, -., :)
- `marker="o"` - Marker style for line charts (o, s, ^, v, *, etc.)
- `size=N` - Marker size for scatter plots
- `bins=N` - Number of bins for histograms

Example:
```
{{ chart "data/sales.csv" bar month sales title="Monthly Sales" xlabel="Month" ylabel="Sales ($)" color=blue width=10 height=6 }}
{{ chart "data/trend.xlsx" line date value title="Trend Analysis" xlabel="Date" ylabel="Value" color=red linestyle="--" marker="o" }}
{{ chart "data/distribution.json" histogram value title="Value Distribution" xlabel="Value" ylabel="Frequency" color=green bins=20 alpha=0.7 }}
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

## Data Transformation Syntax

DataMD supports transforming data from CSV, JSON, and Excel files using a simple query language. Transformations can be applied using the `transform` parameter in the shortcode.

### Transformation Operations

Transformations are specified as a pipe-separated list of operations:

```
filter:condition|sort:column|limit:n
```

### Filter Operation

Filter data based on column values:

- `filter:column==value` - Equal to
- `filter:column!=value` - Not equal to
- `filter:column<value` - Less than
- `filter:column>value` - Greater than
- `filter:column<=value` - Less than or equal to
- `filter:column>=value` - Greater than or equal to
- `filter:column contains text` - Contains text (case-insensitive)

Examples:
```
{{ csv "data/sales.csv" "," "filter:amount>1000" }}
{{ xlsx "data/employees.xlsx" 0 "filter:department contains engineering|sort:salary|limit:5" }}
```

### Sort Operation

Sort data by one or more columns:

- `sort:column` - Sort by column (ascending)
- `sort:-column` - Sort by column (descending)

Examples:
```
{{ csv "data/sales.csv" "," "sort:amount" }}
{{ csv "data/sales.csv" "," "sort:-date|sort:amount" }}
```

### Limit Operation

Limit the number of rows returned:

- `limit:n` - Return only the first n rows

Example:
```
{{ csv "data/large_file.csv" "," "limit:100" }}
```

### Combining Operations

Multiple operations can be combined using the pipe (|) character:

```
{{ csv "data/sales.csv" "," "filter:amount>1000|sort:-amount|limit:10" }}
```

This example filters for sales over $1000, sorts by amount in descending order, and limits to the top 10 results.

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

### Performance Options
- `--chunk-size N` - Set chunk size for streaming processing (default: 10000)
- `--max-memory N` - Set maximum memory usage in MB (default: 100)

### Examples

Process a single file:
```
python process_dmd.py document.dmd
```

Process a directory of files:
```
python process_dmd.py /path/to/documents/
```

Process with custom output location:
```
python process_dmd.py document.dmd -o output.html
```

Process with custom styling:
```
python process_dmd.py document.dmd --style-body "font-family: Arial; max-width: 1000px;"
```

Process with verbose output:
```
python process_dmd.py document.dmd -v
```

Watch for file changes:
```
python process_dmd.py document.dmd --watch
```

Use custom configuration:
```
python process_dmd.py document.dmd --config config/app_config.json
```

Process with custom streaming parameters:
```
python process_dmd.py large_document.dmd --chunk-size 5000 --max-memory 50
```

### Streaming Processing

DataMD automatically uses streaming processing for large files to reduce memory usage. Files larger than the streaming threshold (default: 10MB) will be processed in chunks rather than loaded entirely into memory.

The streaming threshold and chunk size can be configured in the configuration file or through CLI options:

```json
{
  "performance": {
    "chunk_size": 10000,
    "max_memory_mb": 100,
    "streaming_threshold_mb": 10
  }
}
```

When streaming processing is used, large files are processed in chunks and the output is separated by horizontal rules (---) to indicate chunk boundaries.

Example output for a large CSV file:
```
| id | name  | value |
|----|-------|-------|
| 1  | Item1 | 100   |
| 2  | Item2 | 200   |
...
---
| id | name  | value |
|----|-------|-------|
| 10001 | Item10001 | 1000100 |
| 10002 | Item10002 | 1000200 |
...
```

This approach significantly reduces memory usage while processing large files, allowing DataMD to handle files of virtually any size within disk constraints.
