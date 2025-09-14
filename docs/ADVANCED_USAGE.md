# Data Markdown (DataMD) Advanced Usage Guide

This guide covers advanced features and complex use cases for Data Markdown (DataMD), demonstrating how to leverage the full power of the platform for sophisticated data processing and visualization tasks.

## Table of Contents
1. [Configuration System](#configuration-system)
2. [Advanced PDF Processing](#advanced-pdf-processing)
3. [Video Processing](#video-processing)
4. [Chart Generation](#chart-generation)
5. [Data Transformations](#data-transformations)
6. [Caching Mechanism](#caching-mechanism)
7. [Large File Handling](#large-file-handling)
8. [Security Features](#security-features)
9. [CLI Advanced Options](#cli-advanced-options)
10. [Performance Optimization](#performance-optimization)

## Configuration System

DataMD provides a flexible configuration system that allows customization of application behavior through JSON configuration files, environment variables, or programmatic settings.

### Configuration File

Create a JSON configuration file to customize DataMD behavior:

```json
{
  "application": {
    "name": "My DataMD Processor",
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
    "supported_languages": ["eng", "spa", "fra", "deu", "ind"]
  },
  "processing": {
    "default_csv_separator": ",",
    "default_pdf_strategy": "lines",
    "default_ocr_language": "eng",
    "video_thumb_width": 320,
    "video_thumb_height": 240
  },
  "performance": {
    "chunk_size": 10000,
    "max_memory_mb": 100,
    "streaming_threshold_mb": 10
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

Use the configuration file with the CLI:

```bash
python process_dmd.py document.dmd --config config/app_config.json
```

### Environment Variables

Configuration values can also be set using environment variables:

```bash
export DATAMD_APP_NAME="Custom DataMD Processor"
export DATAMD_OCR_ENABLED=false
export DATAMD_MAX_FILE_SIZE_MB=200
export DATAMD_DEFAULT_PDF_STRATEGY=text
```

Environment variables take precedence over configuration file values.

## Advanced PDF Processing

DataMD provides sophisticated PDF processing capabilities with advanced table extraction features.

### PDF Table Extraction Strategies

DataMD supports three table extraction strategies:
- `lines` - Detect tables based on lines (default)
- `text` - Detect tables based on text alignment
- `explicit` - Use explicit table boundaries

Example:
```markdown
{{ pdf_table "report.pdf" 1 lines text }}
```

### PDF Table Detection Thresholds

Fine-tune table detection sensitivity with threshold parameters:

- `snap=N` - Controls how close lines must be to be considered part of the same table (default: 3)
- `edge=N` - Controls how close edges must be to be considered part of the same table (default: 5)
- `intersect=N` - Controls how close edges must be to be considered intersecting (default: 2)

Example:
```markdown
{{ pdf_table "report.pdf" 1 lines text snap=5 edge=10 intersect=3 }}
```

### Combining Multiple Strategies

For complex PDFs, combine different strategies to improve extraction accuracy:

```markdown
{{ pdf_table "complex_report.pdf" 3 lines explicit snap=2 edge=4 }}
```

## Video Processing

DataMD supports video embedding and thumbnail generation with customizable parameters.

### Video Embedding

Embed videos with custom dimensions and playback controls:

```markdown
{{ video "clip.mp4" 800 600 true false }}
```

Parameters:
1. Width (pixels)
2. Height (pixels)
3. Controls (true/false)
4. Autoplay (true/false)

### Video Thumbnail Generation

Generate thumbnails from videos at specific timecodes with custom dimensions:

```markdown
{{ video_thumb "clip.mp4" 15 640 480 }}
```

Parameters:
1. Time in seconds
2. Width (optional, pixels)
3. Height (optional, pixels)

If only one dimension is provided, the other is calculated to maintain aspect ratio:

```markdown
{{ video_thumb "clip.mp4" 10 320 }}  # Width-only (height calculated)
{{ video_thumb "clip.mp4" 20 0 480 }}  # Height-only (width calculated)
```

## Chart Generation

DataMD supports multiple chart types with extensive customization options.

### Supported Chart Types

- `bar` - Bar chart (default)
- `line` - Line chart
- `pie` - Pie chart
- `scatter` - Scatter plot
- `histogram` - Histogram

### Chart Customization Options

Customize charts with various options:

```markdown
{{ chart "data/sales.csv" bar month sales title="Monthly Sales" xlabel="Month" ylabel="Sales ($)" color=blue width=10 height=6 }}
```

Available options:
- `title="Chart Title"` - Chart title
- `xlabel="X Label"` - X-axis label
- `ylabel="Y Label"` - Y-axis label
- `color="color"` - Color for chart elements
- `width=N` - Width in inches
- `height=N` - Height in inches
- `alpha=N` - Transparency (0.0 to 1.0)
- `grid=true` - Show grid lines
- `linestyle="-"` - Line style for line charts (-, --, -., :)
- `marker="o"` - Marker style for line charts (o, s, ^, v, *, etc.)
- `size=N` - Marker size for scatter plots
- `bins=N` - Number of bins for histograms

### Advanced Chart Examples

Line chart with custom styling:
```markdown
{{ chart "data/trend.xlsx" line date value title="Trend Analysis" xlabel="Date" ylabel="Value" color=red linestyle="--" marker="o" }}
```

Histogram with custom bins:
```markdown
{{ chart "data/distribution.json" histogram value title="Value Distribution" xlabel="Value" ylabel="Frequency" color=green bins=20 alpha=0.7 }}
```

## Data Transformations

DataMD supports powerful data transformations including filtering, sorting, and aggregation.

### Transformation Syntax

Transformations are specified as a pipe-separated list of operations:

```markdown
{{ csv "data/sales.csv" "," "filter:amount>1000|sort:-amount|limit:10" }}
```

### Filter Operations

Filter data based on column values:

- `filter:column==value` - Equal to
- `filter:column!=value` - Not equal to
- `filter:column<value` - Less than
- `filter:column>value` - Greater than
- `filter:column<=value` - Less than or equal to
- `filter:column>=value` - Greater than or equal to
- `filter:column contains text` - Contains text (case-insensitive)

Examples:
```markdown
{{ csv "data/sales.csv" "," "filter:amount>1000" }}
{{ xlsx "data/employees.xlsx" 0 "filter:department contains engineering|sort:salary|limit:5" }}
```

### Sort Operations

Sort data by one or more columns:

- `sort:column` - Sort by column (ascending)
- `sort:-column` - Sort by column (descending)

Examples:
```markdown
{{ csv "data/sales.csv" "," "sort:amount" }}
{{ csv "data/sales.csv" "," "sort:-date|sort:amount" }}
```

### Limit Operations

Limit the number of rows returned:

- `limit:n` - Return only the first n rows

Example:
```markdown
{{ csv "data/large_file.csv" "," "limit:100" }}
```

### Combining Operations

Multiple operations can be combined using the pipe (|) character:

```markdown
{{ csv "data/sales.csv" "," "filter:amount>1000|sort:-amount|limit:10" }}
```

This example filters for sales over $1000, sorts by amount in descending order, and limits to the top 10 results.

## Caching Mechanism

DataMD automatically caches the results of expensive operations to improve performance when processing the same files multiple times.

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

## Large File Handling

DataMD automatically uses streaming processing for large files to reduce memory usage.

### Streaming Processing

Files larger than the streaming threshold (default: 10MB) will be processed in chunks rather than loaded entirely into memory.

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
```markdown
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

### CLI Options for Large Files

Process with custom streaming parameters:
```bash
python process_dmd.py large_document.dmd --chunk-size 5000 --max-memory 50
```

## Security Features

DataMD includes several security features to protect against common vulnerabilities.

### Path Validation

DataMD prevents directory traversal attacks by default. File paths are resolved securely relative to the .dmd file location.

To disable this security feature (not recommended):
```bash
export DATAMD_ALLOW_DIRECTORY_TRAVERSAL=true
```

### Input Sanitization

All input parameters are sanitized to prevent injection attacks and other security vulnerabilities.

### File Format Validation

Files are validated to ensure they match expected formats based on extension and content.

## CLI Advanced Options

The DataMD processor supports several advanced command-line options.

### Output Customization

Customize output styling:
```bash
python process_dmd.py document.dmd --style-body "font-family: Arial; max-width: 1000px;" --style-table "border: 2px solid #333;"
```

### Performance Options

Adjust performance parameters:
```bash
python process_dmd.py large_document.dmd --chunk-size 5000 --max-memory 50
```

### Debugging Options

Enable verbose output for debugging:
```bash
python process_dmd.py document.dmd -v
```

### Watch Mode

Watch for file changes and automatically reprocess:
```bash
python process_dmd.py document.dmd --watch
```

## Performance Optimization

DataMD includes several features to optimize performance for large-scale processing.

### Memory Management

Large files are processed in chunks to reduce memory usage. The chunk size and memory limits can be adjusted based on system resources.

### Caching

Results of expensive operations are cached to avoid reprocessing the same data.

### Parallel Processing

When processing multiple files, DataMD can take advantage of multiple CPU cores for improved performance.

### Best Practices

1. Use appropriate chunk sizes for your data and system resources
2. Enable caching for frequently processed files
3. Use streaming processing for large files
4. Limit the number of concurrent operations to avoid resource exhaustion
5. Monitor memory usage and adjust limits as needed

## Conclusion

DataMD provides a powerful platform for creating dynamic, data-driven documents with advanced features for complex use cases. By leveraging the configuration system, advanced PDF processing, video handling, chart generation, data transformations, caching, and large file handling capabilities, you can create sophisticated reports and documentation that automatically update with your data.
