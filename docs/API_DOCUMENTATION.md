# Data Markdown (DataMD) API Documentation

This document provides comprehensive API documentation for all Python modules and public functions in the DataMD project.

## Table of Contents
1. [Main Modules](#main-modules)
   - [datamd_ext.py](#datamd_extpy)
   - [process_dmd.py](#process_dmdpy)
   - [config.py](#configpy)
   - [cache.py](#cachepy)
   - [data_transform.py](#data_transformpy)
2. [Public Functions and Classes](#public-functions-and-classes)
3. [Configuration Options](#configuration-options)
4. [Usage Examples](#usage-examples)

## Main Modules

### datamd_ext.py

This is the core extension module that implements all DataMD shortcode handlers and processing logic.

#### Classes

##### DataMDPreprocessor
Extends `markdown.preprocessors.Preprocessor`

Main preprocessor class that handles DataMD shortcodes in Markdown documents.

**Methods:**
- `run(lines)`: Process lines of Markdown text and replace DataMD shortcodes with processed content

##### DataMDExtension
Extends `markdown.extensions.Extension`

Markdown extension class that registers the DataMD preprocessor.

**Methods:**
- `extendMarkdown(md)`: Register the DataMD preprocessor with the Markdown processor

##### Utility Functions

###### resolve_secure_path(file_path, base_dir=None)
Resolve a file path securely, preventing directory traversal attacks.

**Parameters:**
- `file_path` (str): The file path to resolve
- `base_dir` (str, optional): The base directory to resolve relative paths against

**Returns:**
- `Path`: The resolved secure path

**Raises:**
- `ValueError`: If the path is invalid or attempts directory traversal
- `FileNotFoundError`: If the file doesn't exist

###### sanitize_numeric_input(value, min_val=None, max_val=None, default=None)
Sanitize numeric input with optional min/max constraints.

**Parameters:**
- `value` (str): The input value to sanitize
- `min_val` (float, optional): Minimum allowed value
- `max_val` (float, optional): Maximum allowed value
- `default`: Default value if input is invalid

**Returns:**
- `float or int`: Sanitized numeric value, or default if invalid

###### sanitize_boolean_input(value, default=False)
Sanitize boolean input.

**Parameters:**
- `value` (str): The input value to sanitize
- `default` (bool): Default value if input is invalid

**Returns:**
- `bool`: Sanitized boolean value

###### sanitize_string_input(value, max_length=1000, allowed_chars=None)
Sanitize string input with length and character constraints.

**Parameters:**
- `value` (str): The input value to sanitize
- `max_length` (int): Maximum allowed length
- `allowed_chars` (str, optional): String of allowed characters

**Returns:**
- `str`: Sanitized string value

###### sanitize_language_code(lang_code)
Sanitize language code for OCR.

**Parameters:**
- `lang_code` (str): The language code to sanitize

**Returns:**
- `str`: Sanitized language code (default: 'eng')

###### sanitize_sheet_name(sheet)
Sanitize sheet name/index for Excel files.

**Parameters:**
- `sheet` (str): The sheet name or index

**Returns:**
- `str or int`: Sanitized sheet name or index

###### sanitize_strategy(strategy)
Sanitize PDF table extraction strategy.

**Parameters:**
- `strategy` (str): The strategy to sanitize

**Returns:**
- `str`: Sanitized strategy (default: 'lines')

###### sanitize_chart_type(chart_type)
Sanitize chart type for chart generation.

**Parameters:**
- `chart_type` (str): The chart type to sanitize

**Returns:**
- `str`: Sanitized chart type (default: 'bar')

###### sanitize_chart_options(options_str)
Sanitize chart options string.

**Parameters:**
- `options_str` (str): Chart options string in format "key1=value1,key2=value2"

**Returns:**
- `dict`: Dictionary of chart options

###### read_csv_chunked(file_path, chunk_size=10000, **kwargs)
Read CSV file in chunks to reduce memory usage for large files.

**Parameters:**
- `file_path` (str): Path to CSV file
- `chunk_size` (int): Number of rows per chunk
- `**kwargs`: Additional arguments for pd.read_csv

**Yields:**
- `pd.DataFrame`: Chunks of the CSV file

###### read_excel_chunked(file_path, sheet_name=0, chunk_size=10000, engine="openpyxl")
Read Excel file in chunks (simplified implementation).

**Parameters:**
- `file_path` (str): Path to Excel file
- `sheet_name` (str or int): Sheet name or index
- `chunk_size` (int): Number of rows per chunk
- `engine` (str): Excel engine to use

**Yields:**
- `pd.DataFrame`: Chunks of the Excel file

###### process_csv_streaming(file_path, sep=",", transform="", chunk_size=10000)
Process CSV files in streaming fashion with chunked reading.

**Parameters:**
- `file_path` (str): Path to CSV file
- `sep` (str): CSV separator
- `transform` (str): Transformation string
- `chunk_size` (int): Number of rows per chunk

**Yields:**
- `str`: Processed chunk as markdown

###### process_excel_streaming(file_path, sheet_name=0, transform="", chunk_size=10000, engine="openpyxl")
Process Excel files in streaming fashion.

**Parameters:**
- `file_path` (str): Path to Excel file
- `sheet_name` (str or int): Sheet name or index
- `transform` (str): Transformation string
- `chunk_size` (int): Number of rows per chunk
- `engine` (str): Excel engine to use

**Yields:**
- `str`: Processed chunk as markdown

###### process_large_csv(file_path, sep=",", transform="", max_memory_mb=100)
Process large CSV files with memory optimization.

**Parameters:**
- `file_path` (str): Path to CSV file
- `sep` (str): CSV separator
- `transform` (str): Transformation string
- `max_memory_mb` (int): Maximum memory usage in MB

**Returns:**
- `str`: Markdown representation of processed data

###### process_large_excel(file_path, sheet_name=0, transform="", engine="openpyxl", max_memory_mb=100)
Process large Excel files with memory optimization.

**Parameters:**
- `file_path` (str): Path to Excel file
- `sheet_name` (str or int): Sheet name or index
- `transform` (str): Transformation string
- `engine` (str): Excel engine to use
- `max_memory_mb` (int): Maximum memory usage in MB

**Returns:**
- `str`: Markdown representation of processed data

### process_dmd.py

Command-line interface for processing DataMD files.

#### Functions

###### process_dmd_file(input_file, output_file=None, output_format="html", style_options=None, verbose=False, chunk_size=None, max_memory_mb=None)
Process a single .dmd file and convert to specified format.

**Parameters:**
- `input_file` (str): Path to input .dmd file
- `output_file` (str, optional): Path to output file
- `output_format` (str): Output format (currently only HTML is supported)
- `style_options` (dict, optional): Custom CSS styling options
- `verbose` (bool): Enable verbose output
- `chunk_size` (int, optional): Chunk size for streaming processing
- `max_memory_mb` (int, optional): Maximum memory usage in MB

**Returns:**
- `bool`: True if processing was successful

###### process_directory(directory, output_format="html", style_options=None, verbose=False, chunk_size=None, max_memory_mb=None)
Process all .dmd files in a directory.

**Parameters:**
- `directory` (str or Path): Directory containing .dmd files
- `output_format` (str): Output format (currently only HTML is supported)
- `style_options` (dict, optional): Custom CSS styling options
- `verbose` (bool): Enable verbose output
- `chunk_size` (int, optional): Chunk size for streaming processing
- `max_memory_mb` (int, optional): Maximum memory usage in MB

###### watch_path(target_path, output_format="html", style_options=None, verbose=False, chunk_size=None, max_memory_mb=None)
Watch a file or directory for changes and reprocess .dmd files.

**Parameters:**
- `target_path` (str): Path to file or directory to watch
- `output_format` (str): Output format (currently only HTML is supported)
- `style_options` (dict, optional): Custom CSS styling options
- `verbose` (bool): Enable verbose output
- `chunk_size` (int, optional): Chunk size for streaming processing
- `max_memory_mb` (int, optional): Maximum memory usage in MB

###### main(args=None)
Main entry point for the DataMD processor.

**Parameters:**
- `args` (list, optional): Command-line arguments

### config.py

Configuration management for DataMD application.

#### Classes

##### Configuration
Configuration class for DataMD application.

Manages application settings from JSON config file, environment variables, and provides default values.

**Methods:**
- `__init__(config_file=None)`: Initialize configuration
- `get(key_path, default=None)`: Get configuration value using dot notation
- `set(key_path, value)`: Set configuration value using dot notation
- `get_application_name()`: Get application name
- `get_application_version()`: Get application version
- `is_feature_enabled(feature)`: Check if a feature is enabled
- `get_supported_excel_formats()`: Get list of supported Excel formats
- `get_max_file_size_mb()`: Get maximum allowed file size in MB
- `get_max_pdf_pages()`: Get maximum allowed PDF pages
- `get_supported_languages()`: Get list of supported OCR languages
- `get_default_csv_separator()`: Get default CSV separator
- `get_default_pdf_strategy()`: Get default PDF table extraction strategy
- `get_default_ocr_language()`: Get default OCR language
- `get_video_thumb_dimensions()`: Get default video thumbnail dimensions
- `get_chunk_size()`: Get default chunk size for streaming processing
- `get_max_memory_mb()`: Get maximum memory usage for processing in MB
- `get_streaming_threshold_mb()`: Get file size threshold for switching to streaming mode in MB
- `is_directory_traversal_allowed()`: Check if directory traversal is allowed (security setting)
- `get_allowed_file_extensions()`: Get list of allowed file extensions
- `get_max_filename_length()`: Get maximum allowed filename length
- `to_dict()`: Get complete configuration as dictionary
- `save_to_file(filepath)`: Save current configuration to JSON file

#### Functions

###### get_config(config_file=None)
Get singleton configuration instance.

**Parameters:**
- `config_file` (str, optional): Path to JSON configuration file

**Returns:**
- `Configuration`: Configuration instance

###### reset_config()
Reset configuration singleton instance.

### cache.py

Caching mechanism for DataMD application.

#### Classes

##### CacheManager
Cache manager for DataMD application.

Provides file-based caching with automatic invalidation based on file modification times.

**Methods:**
- `__init__(cache_dir=None)`: Initialize cache manager
- `get(file_path, **kwargs)`: Get cached data for a file
- `set(file_path, data, **kwargs)`: Cache data for a file
- `clear()`: Clear all cached data
- `get_cache_info()`: Get information about the cache

#### Functions

###### get_cache_manager(cache_dir=None)
Get singleton cache manager instance.

**Parameters:**
- `cache_dir` (str, optional): Directory to store cache files

**Returns:**
- `CacheManager`: Cache manager instance

###### reset_cache()
Reset cache manager singleton instance.

### data_transform.py

Data transformation capabilities for DataMD.

#### Classes

##### DataTransformer
Data transformation class for DataMD.

Supports filtering, sorting, and aggregation operations on pandas DataFrames.

**Methods:**
- `__init__(df)`: Initialize DataTransformer with a DataFrame
- `filter(condition)`: Filter DataFrame based on a condition
- `sort(columns, ascending=True)`: Sort DataFrame by one or more columns
- `aggregate(group_by=None, aggregations=None)`: Aggregate data by grouping and applying aggregation functions
- `limit(n)`: Limit the number of rows in the DataFrame
- `get_dataframe()`: Get the transformed DataFrame
- `to_markdown(index=False)`: Convert DataFrame to markdown table

#### Functions

###### parse_transform_string(transform_str)
Parse a transformation string into a list of transformation operations.

**Parameters:**
- `transform_str` (str): Transformation string with operations separated by |

**Returns:**
- `list`: List of transformation operations as dictionaries

###### apply_transformations(df, transform_str)
Apply transformations to a DataFrame based on a transformation string.

**Parameters:**
- `df` (pd.DataFrame): DataFrame to transform
- `transform_str` (str): Transformation string

**Returns:**
- `pd.DataFrame`: Transformed DataFrame

## Public Functions and Classes

### Main Entry Points

- `DataMDExtension` - The main Markdown extension class
- `process_dmd.main()` - The main CLI entry point
- `get_config()` - Get the global configuration instance
- `get_cache_manager()` - Get the global cache manager instance

### Utility Functions

- `resolve_secure_path()` - Secure file path resolution
- `sanitize_*()` functions - Input sanitization utilities
- `read_csv_chunked()` - Chunked CSV reading
- `read_excel_chunked()` - Chunked Excel reading
- `process_*_streaming()` - Streaming processing functions
- `process_large_*()` - Large file processing functions

## Configuration Options

### Application Settings
- `application.name` - Application name (default: "DataMD Processor")
- `application.version` - Application version (default: "1.0.0")
- `application.environment` - Environment (default: "production")

### Feature Settings
- `features.ocr_enabled` - Enable/disable OCR processing (default: true)
- `features.pdf_processing` - Enable/disable PDF processing (default: true)
- `features.video_support` - Enable/disable video support (default: true)
- `features.excel_formats` - List of supported Excel formats (default: ["xlsx", "xls", "xlsm", "ods"])

### Limit Settings
- `limits.max_file_size_mb` - Maximum file size in MB (default: 100)
- `limits.max_pages_pdf` - Maximum PDF pages to process (default: 50)
- `limits.supported_languages` - Supported OCR languages (default: ["eng", "spa", "fra", "deu", "ind"])

### Processing Settings
- `processing.default_csv_separator` - Default CSV separator (default: ",")
- `processing.default_pdf_strategy` - Default PDF table extraction strategy (default: "lines")
- `processing.default_ocr_language` - Default OCR language (default: "eng")
- `processing.video_thumb_width` - Default video thumbnail width (default: 320)
- `processing.video_thumb_height` - Default video thumbnail height (default: 240)

### Performance Settings
- `performance.chunk_size` - Chunk size for streaming processing (default: 10000)
- `performance.max_memory_mb` - Maximum memory usage in MB (default: 100)
- `performance.streaming_threshold_mb` - File size threshold for streaming mode (default: 10)

### Security Settings
- `security.allow_directory_traversal` - Allow directory traversal (security setting, default: false)
- `security.max_filename_length` - Maximum filename length (default: 255)
- `security.allowed_file_extensions` - Allowed file extensions (default: [".csv", ".json", ".xlsx", ".xls", ".xlsm", ".ods", ".pdf", ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".mp4", ".avi", ".mov", ".wmv"])

## Usage Examples

### Programmatic Usage

```python
from python_implementation.datamd_ext import DataMDExtension
from python_implementation.config import get_config
from python_implementation.cache import get_cache_manager
from python_implementation.data_transform import apply_transformations

# Get configuration
config = get_config("config.json")

# Get cache manager
cache = get_cache_manager()

# Process a DataFrame with transformations
import pandas as pd
df = pd.read_csv("data.csv")
transformed_df = apply_transformations(df, "filter:amount>1000|sort:-amount|limit:10")

# Use the extension in a Markdown processor
import markdown
md = markdown.Markdown(extensions=[DataMDExtension()])
html = md.convert("# My Document\n{{ csv \"data.csv\" }}")
```

### Extending Functionality

```python
# Custom shortcode handler (example)
class CustomDataMDPreprocessor(DataMDPreprocessor):
    def run(self, lines):
        # Call parent implementation
        new_lines = super().run(lines)

        # Add custom processing
        for i, line in enumerate(new_lines):
            # Custom shortcode processing
            if "{{ custom_shortcode" in line:
                # Process custom shortcode
                new_lines[i] = self.process_custom_shortcode(line)

        return new_lines
```

This API documentation provides a comprehensive reference for all public functions and classes in the DataMD project, enabling developers to understand and extend the functionality as needed.
