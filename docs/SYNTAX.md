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
