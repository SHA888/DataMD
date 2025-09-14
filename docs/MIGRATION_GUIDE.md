# Data Markdown (DataMD) Migration Guide

This guide provides instructions for migrating from previous versions of DataMD to the current version, highlighting breaking changes, new features, and best practices for upgrading.

## Table of Contents
1. [Version Compatibility](#version-compatibility)
2. [Breaking Changes](#breaking-changes)
3. [New Features](#new-features)
4. [Configuration Changes](#configuration-changes)
5. [Syntax Changes](#syntax-changes)
6. [API Changes](#api-changes)
7. [Performance Improvements](#performance-improvements)
8. [Migration Steps](#migration-steps)
9. [Testing Your Migration](#testing-your-migration)
10. [Troubleshooting](#troubleshooting)

## Version Compatibility

This migration guide covers upgrading to DataMD v1.0.0 from previous versions.

### Supported Upgrade Paths
- v0.1.x → v1.0.0
- v0.2.x → v1.0.0
- v0.3.x → v1.0.0

### Unsupported Upgrade Paths
- Versions older than v0.1.0 are not supported for direct upgrade. Please upgrade to v0.1.0 first.

## Breaking Changes

### 1. Configuration System
The configuration system has been completely rewritten to support JSON configuration files and environment variables.

**Old approach:**
```python
# Direct parameter passing
process_dmd_file("document.dmd", chunk_size=5000)
```

**New approach:**
```python
# Configuration through config system
from python_implementation.config import get_config
config = get_config("config.json")
config.set("performance.chunk_size", 5000)
```

### 2. CLI Parameter Changes
Several CLI parameters have been renamed or restructured for consistency.

**Removed parameters:**
- `--chunksize` (replaced with `--chunk-size`)
- `--maxmemory` (replaced with `--max-memory`)

**Added parameters:**
- `--config` for configuration file support
- `--style-*` parameters for custom CSS styling

### 3. Cache Directory Structure
The cache directory structure has changed to support better organization and invalidation.

**Old cache location:** `.datamd_cache/`
**New cache location:** `~/.cache/datamd/` or `./cache/`

### 4. Error Handling
Error messages have been improved for better clarity, but the format has changed.

**Old error format:**
```
Error: File not found
```

**New error format:**
```
Error: File not found: path/to/file.csv
```

## New Features

### 1. Video Thumbnail Generation
Added support for generating thumbnails from video files:
```markdown
{{ video_thumb "clip.mp4" 5 }}                  # Thumbnail at 5 seconds
{{ video_thumb "clip.mp4" 10 320 240 }}         # Thumbnail at 10s with custom dimensions
```

### 2. Enhanced PDF Table Extraction
Added advanced PDF table extraction with strategy and threshold parameters:
```markdown
{{ pdf_table "report.pdf" 2 lines text snap=3 edge=5 intersect=2 }}
```

### 3. Chart Generation
Added support for generating charts from data files:
```markdown
{{ chart "data/sales.csv" bar month sales title="Monthly Sales" }}
```

### 4. Data Transformations
Added powerful data transformation capabilities:
```markdown
{{ csv "data/customers.csv" "," "filter:age>25|sort:name|limit:10" }}
```

### 5. Configuration System
Added comprehensive configuration system with JSON files and environment variables.

### 6. Improved Caching
Enhanced caching mechanism with better invalidation and performance.

### 7. Large File Handling
Added optimized processing for large files with streaming and memory management.

## Configuration Changes

### New Configuration Structure
The configuration system now uses a hierarchical JSON structure:

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
    "video_support": true
  },
  "limits": {
    "max_file_size_mb": 100,
    "max_pages_pdf": 50
  },
  "processing": {
    "default_csv_separator": ",",
    "default_pdf_strategy": "lines"
  },
  "performance": {
    "chunk_size": 10000,
    "max_memory_mb": 100,
    "streaming_threshold_mb": 10
  },
  "security": {
    "allow_directory_traversal": false,
    "max_filename_length": 255
  }
}
```

### Environment Variables
All configuration options can now be set using environment variables:

```bash
export DATAMD_APP_NAME="My DataMD Processor"
export DATAMD_OCR_ENABLED=false
export DATAMD_MAX_FILE_SIZE_MB=200
```

## Syntax Changes

### 1. PDF Table Parameters
Enhanced PDF table extraction now supports threshold parameters:

**Old syntax:**
```markdown
{{ pdf_table "report.pdf" 2 lines text }}
```

**New syntax (backward compatible):**
```markdown
{{ pdf_table "report.pdf" 2 lines text }}  # Same as before
{{ pdf_table "report.pdf" 2 lines text snap=3 edge=5 intersect=2 }}  # New threshold parameters
```

### 2. Chart Parameters
Added chart generation shortcode:

```markdown
{{ chart "data/sales.csv" bar month sales title="Monthly Sales" xlabel="Month" ylabel="Sales ($)" }}
```

### 3. Data Transformation Parameters
Added data transformation syntax:

```markdown
{{ csv "data/customers.csv" "," "filter:age>25|sort:name|limit:10" }}
```

## API Changes

### 1. Configuration API
The configuration API has been completely redesigned:

**Old API:**
```python
# Direct parameter passing
process_dmd_file("document.dmd", chunk_size=5000)
```

**New API:**
```python
# Configuration through singleton
from python_implementation.config import get_config
config = get_config()
config.set("performance.chunk_size", 5000)

# Or through configuration file
config = get_config("config.json")
```

### 2. Cache API
The cache API has been enhanced:

**Old API:**
```python
# Limited caching functionality
```

**New API:**
```python
from python_implementation.cache import get_cache_manager
cache = get_cache_manager()
cache.set("key", data)
data = cache.get("key")
```

### 3. Data Transformation API
Added new data transformation APIs:

```python
from python_implementation.data_transform import apply_transformations
transformed_df = apply_transformations(df, "filter:age>25|sort:name|limit:10")
```

## Performance Improvements

### 1. Streaming Processing
Large files are now processed in chunks to reduce memory usage:

```python
# Automatically used for files > streaming_threshold_mb
{{ csv "large_file.csv" }}
```

### 2. Enhanced Caching
Improved cache invalidation based on file modification times:

```python
# Cache automatically invalidated when source file changes
```

### 3. Memory Optimization
Better memory management for large file processing:

```bash
# CLI options for memory management
python process_dmd.py document.dmd --chunk-size 5000 --max-memory 50
```

## Migration Steps

### Step 1: Backup Your Current Installation
```bash
# Backup your current DataMD installation
cp -r /path/to/datamd /path/to/datamd.backup
```

### Step 2: Update Dependencies
```bash
# Install new dependencies
pip install -r requirements.txt
```

### Step 3: Update Configuration
Convert your old configuration approach to the new JSON format:

1. Create a new configuration file:
```json
{
  "application": {
    "name": "DataMD Processor",
    "version": "1.0.0"
  },
  "performance": {
    "chunk_size": 10000,
    "max_memory_mb": 100
  }
}
```

2. Update your code to use the new configuration system:
```python
from python_implementation.config import get_config
config = get_config("config.json")
```

### Step 4: Update CLI Usage
Update any scripts or workflows that use the CLI:

**Old command:**
```bash
python process_dmd.py document.dmd --chunksize 5000
```

**New command:**
```bash
python process_dmd.py document.dmd --chunk-size 5000
```

### Step 5: Clear Cache
Clear the old cache directory and let DataMD create the new cache structure:

```bash
# Remove old cache
rm -rf .datamd_cache/

# Process files to create new cache
python process_dmd.py document.dmd
```

### Step 6: Update Documentation References
Update any documentation that references DataMD features or syntax.

## Testing Your Migration

### 1. Test Basic Functionality
```bash
# Test processing a simple document
python process_dmd.py examples/simple_example.dmd
```

### 2. Test New Features
```bash
# Test video thumbnail generation
python process_dmd.py examples/video_example.dmd

# Test PDF table extraction
python process_dmd.py examples/comprehensive_example.dmd

# Test chart generation
python process_dmd.py examples/chart_example.dmd
```

### 3. Test Configuration
```bash
# Test with configuration file
python process_dmd.py document.dmd --config config.json

# Test with environment variables
export DATAMD_MAX_FILE_SIZE_MB=200
python process_dmd.py document.dmd
```

### 4. Test Large File Handling
```bash
# Test streaming processing
python process_dmd.py large_document.dmd --chunk-size 5000 --max-memory 50
```

## Troubleshooting

### Issue: Configuration Not Loading
**Solution:** Ensure your configuration file is valid JSON and located in the correct path.

### Issue: Cache Directory Permissions
**Solution:** Check that the cache directory is writable. DataMD will use `./cache/` if `~/.cache/datamd/` is not accessible.

### Issue: Missing Dependencies
**Solution:** Install all required dependencies:
```bash
pip install -r requirements.txt
```

### Issue: CLI Parameter Errors
**Solution:** Check that you're using the new parameter names:
- `--chunk-size` instead of `--chunksize`
- `--max-memory` instead of `--maxmemory`

### Issue: Video Processing Not Working
**Solution:** Ensure moviepy is installed:
```bash
pip install moviepy
```

### Issue: Chart Generation Not Working
**Solution:** Ensure matplotlib is installed:
```bash
pip install matplotlib
```

## Conclusion

This migration guide covers the essential steps to upgrade from previous versions of DataMD to v1.0.0. The new version includes significant improvements in functionality, performance, and usability while maintaining backward compatibility for most existing features.

If you encounter any issues during the migration process, please consult the documentation or reach out to the community for support.
