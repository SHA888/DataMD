# Large File Handling Design for DataMD

## Overview
This document outlines the design for implementing streaming/chunked processing capabilities in DataMD to handle large files efficiently while minimizing memory usage.

## Current State Analysis
Based on memory profiling, we've identified that:
1. Standard CSV reading uses significantly more memory than chunked reading
2. For a 1.91MB file with 50,000 rows:
   - Standard reading: 9.38 MB memory usage
   - Chunked reading: 2.59 MB memory usage
   - Large file processing: 0.02 MB memory usage (with preview)
3. Chunked reading reduces memory usage by ~72% compared to standard reading

## Design Approach

### 1. Streaming Architecture
We'll implement a streaming architecture that processes data in chunks rather than loading entire files into memory.

#### Key Components:
- **Chunked Data Readers**: Specialized functions for reading data formats in chunks
- **Streaming Processors**: Components that process data chunks incrementally
- **Memory-Efficient Transformers**: Data transformation functions that work with chunks
- **Progressive Output Generators**: Functions that generate output incrementally

### 2. Chunked Processing Pipeline

#### CSV Files:
```python
def process_csv_streaming(file_path, chunk_size=10000, transform=None):
    """
    Process CSV files in streaming fashion with chunked reading.

    Args:
        file_path (str): Path to CSV file
        chunk_size (int): Number of rows per chunk
        transform (str): Transformation string

    Yields:
        str: Processed chunk as markdown
    """
    for chunk in read_csv_chunked(file_path, chunk_size=chunk_size):
        if transform:
            chunk = apply_transformations(chunk, transform)
        yield chunk.to_markdown(index=False)
```

#### Excel Files:
```python
def process_excel_streaming(file_path, sheet_name=0, chunk_size=10000, transform=None):
    """
    Process Excel files in streaming fashion.

    Args:
        file_path (str): Path to Excel file
        sheet_name (str or int): Sheet name or index
        chunk_size (int): Number of rows per chunk
        transform (str): Transformation string

    Yields:
        str: Processed chunk as markdown
    """
    for chunk in read_excel_chunked(file_path, sheet_name=sheet_name, chunk_size=chunk_size):
        if transform:
            chunk = apply_transformations(chunk, transform)
        yield chunk.to_markdown(index=False)
```

### 3. Memory Optimization Techniques

#### a. Lazy Loading
Only load data chunks as needed rather than pre-loading entire datasets.

#### b. Generator-Based Processing
Use Python generators to process data incrementally without storing all results in memory.

#### c. Configurable Chunk Sizes
Allow users to configure chunk sizes based on their memory constraints:
```python
# In config.py
DEFAULTS = {
    "performance": {
        "chunk_size": 10000,
        "max_memory_mb": 100,
        "streaming_threshold_mb": 10
    }
}
```

#### d. Memory Monitoring
Implement memory monitoring to dynamically adjust chunk sizes based on available memory.

### 4. Integration with Existing Features

#### a. Configuration System
Add new configuration options for large file handling:
- `chunk_size`: Number of rows per chunk
- `streaming_threshold_mb`: File size threshold for switching to streaming mode
- `max_memory_mb`: Maximum memory usage for processing

#### b. Data Transformation
Modify data transformation functions to work with streaming data:
- Filter operations can be applied to each chunk independently
- Sorting operations require collecting all data (memory intensive)
- Aggregation operations can be done incrementally with map-reduce approach

#### c. Caching
Update caching mechanism to handle chunked data:
- Cache individual chunks rather than entire processed files
- Implement LRU eviction for chunk cache

### 5. User Experience Considerations

#### a. Progressive Output
For very large files, provide progressive output with status updates:
```
Processing large file (150MB): 25% complete...
```

#### b. Preview Mode
For large files, show a preview of the first N rows with a note about the full file size:
```
| name | age | city |
|------|-----|------|
| John | 25  | NYC  |
| Jane | 30  | LA   |

*Note: Large file detected (150MB). Showing first 100 rows. Use --full flag to process entire file.*
```

#### c. CLI Options
Add new CLI options for large file handling:
- `--chunk-size N`: Set chunk size for processing
- `--max-memory N`: Set maximum memory usage in MB
- `--preview`: Only process first chunk for preview
- `--full`: Process entire file (default behavior for smaller files)

## Implementation Plan

### Phase 1: Core Streaming Infrastructure
1. Implement chunked readers for all supported formats
2. Create streaming processors for basic operations
3. Add configuration options for streaming parameters

### Phase 2: Advanced Features
1. Implement streaming data transformations
2. Add memory monitoring and dynamic chunk sizing
3. Enhance caching for chunked data

### Phase 3: User Experience
1. Add progressive output and status reporting
2. Implement preview mode for large files
3. Add CLI options for streaming parameters

## Testing Strategy

### Performance Benchmarks
1. Test memory usage with files of various sizes (1MB, 10MB, 100MB)
2. Measure processing time compared to current implementation
3. Test with different chunk sizes to find optimal defaults

### Edge Cases
1. Test with empty files
2. Test with files that don't divide evenly into chunks
3. Test error handling in streaming mode
4. Test with corrupted files

### Integration Testing
1. Verify compatibility with all existing shortcode handlers
2. Test with data transformation operations
3. Test with caching enabled/disabled

## Expected Benefits

1. **Reduced Memory Usage**: 50-80% reduction in memory usage for large files
2. **Improved Stability**: Eliminate out-of-memory errors with large files
3. **Better User Experience**: Progressive feedback for long-running operations
4. **Scalability**: Ability to process files of any size within disk constraints

## Risks and Mitigations

### 1. Performance Overhead
**Risk**: Chunked processing may be slower than loading entire files
**Mitigation**: Optimize chunk sizes and use efficient processing algorithms

### 2. Complexity Increase
**Risk**: Streaming implementation adds complexity to codebase
**Mitigation**: Maintain backward compatibility and clear separation of concerns

### 3. Feature Limitations
**Risk**: Some features may not work with streaming (e.g., global sorting)
**Mitigation**: Provide fallback to standard processing when needed and clear documentation

## Next Steps

1. Implement chunked readers for all data formats
2. Create streaming processors for basic operations
3. Add configuration options for streaming parameters
4. Begin performance testing with large files
