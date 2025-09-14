"""
Performance benchmarks for DataMD features.

This script contains benchmarks for measuring performance of key operations
in the DataMD engine, including video thumbnail generation, PDF table extraction,
chart generation, and large file processing.
"""

import os
import sys
import tempfile
import time
from pathlib import Path

# Add the python_implementation directory to the path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "python_implementation")
)

import pytest

# Try to import psutil for memory profiling
try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    psutil = None

from datamd_ext import (
    DataMDPreprocessor,
    process_csv_streaming,
    process_large_csv,
    read_csv_chunked,
    sanitize_boolean_input,
    sanitize_chart_options,
    sanitize_numeric_input,
    sanitize_strategy,
)


def get_memory_usage():
    """Get current memory usage in MB."""
    if not PSUTIL_AVAILABLE:
        return 0
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024


def benchmark_function(func, *args, **kwargs):
    """
    Benchmark a function and return timing and memory usage information.

    Args:
        func: Function to benchmark
        *args: Positional arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function

    Returns:
        dict: Dictionary with timing and memory usage information
    """
    start_memory = get_memory_usage()
    start_time = time.perf_counter()

    try:
        result = func(*args, **kwargs)
        exception = None
    except Exception as e:
        result = None
        exception = e

    end_time = time.perf_counter()
    end_memory = get_memory_usage()

    return {
        "time_taken": end_time - start_time,
        "memory_usage": end_memory - start_memory,
        "result": result,
        "exception": exception,
    }


def create_test_csv(file_path, num_rows):
    """Create a test CSV file with specified number of rows."""
    with open(file_path, "w") as f:
        f.write("id,name,value,category,timestamp,description\n")
        for i in range(num_rows):
            f.write(
                f"{i},name{i},value{i},category{i % 5},"
                f"2023-01-{(i % 30) + 1:02d},"
                f"description for item {i}\n"
            )


@pytest.mark.benchmark
def test_sanitize_functions_performance():
    """Benchmark sanitize functions performance."""
    # Test sanitize_numeric_input
    result = benchmark_function(
        sanitize_numeric_input, "123.45", min_val=0, max_val=1000
    )
    assert result["time_taken"] < 0.01  # Should be very fast

    # Test sanitize_boolean_input
    result = benchmark_function(sanitize_boolean_input, "true", default=False)
    assert result["time_taken"] < 0.01  # Should be very fast

    # Test sanitize_strategy
    result = benchmark_function(sanitize_strategy, "lines")
    assert result["time_taken"] < 0.01  # Should be very fast

    # Test sanitize_chart_options
    options_str = "title=Test,width=10,height=5,color=red,grid=true"
    result = benchmark_function(sanitize_chart_options, options_str)
    assert result["time_taken"] < 0.01  # Should be very fast


@pytest.mark.benchmark
def test_csv_processing_performance():
    """Benchmark CSV processing performance."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        csv_file = tmp_path / "test.csv"

        # Create a medium-sized test CSV (10,000 rows)
        create_test_csv(csv_file, 10000)

        # Benchmark standard chunked reading
        result = benchmark_function(
            list, read_csv_chunked(str(csv_file), chunk_size=1000)
        )
        assert result["time_taken"] < 5.0  # Should complete in reasonable time
        assert len(result["result"]) == 10  # 10,000 rows / 1,000 chunk size

        # Benchmark streaming processing
        result = benchmark_function(
            list, process_csv_streaming(str(csv_file), chunk_size=1000)
        )
        assert result["time_taken"] < 5.0  # Should complete in reasonable time

        # Benchmark large file processing
        result = benchmark_function(
            process_large_csv, str(csv_file), sep=",", max_memory_mb=10
        )
        assert result["time_taken"] < 5.0  # Should complete in reasonable time


@pytest.mark.benchmark
def test_shortcode_processing_performance():
    """Benchmark shortcode processing performance."""
    # Test DataMDPreprocessor with various shortcodes
    preprocessor = DataMDPreprocessor(None)

    # Test simple shortcode processing
    test_lines = [
        '{{ csv "test.csv" }}',
        '{{ json "test.json" }}',
        '{{ xlsx "test.xlsx" }}',
        '{{ pdf "test.pdf" }}',
        '{{ image_ocr "test.jpg" }}',
        '{{ video "test.mp4" }}',
        '{{ video_thumb "test.mp4" 5 }}',
        '{{ chart "test.csv" bar x y }}',
        '{{ pdf_table "test.pdf" 1 }}',
    ]

    for line in test_lines:
        result = benchmark_function(preprocessor.run, [line])
        assert result["time_taken"] < 0.1  # Each should be fast


@pytest.mark.benchmark
def test_chart_options_parsing_performance():
    """Benchmark chart options parsing performance."""
    # Test with complex options string
    complex_options = (
        "title=Complex Chart,width=12,height=8,color=blue,grid=true,"
        "alpha=0.7,linestyle=--,marker=o,size=20,bins=15"
    )

    # Run multiple iterations to get a good average
    times = []
    for _ in range(100):
        result = benchmark_function(sanitize_chart_options, complex_options)
        times.append(result["time_taken"])

    avg_time = sum(times) / len(times)
    assert avg_time < 0.01  # Average should be very fast


@pytest.mark.benchmark
def test_strategy_sanitization_performance():
    """Benchmark strategy sanitization performance."""
    # Test with various strategy inputs
    strategies = ["lines", "text", "explicit", "invalid", "LINES", "Text"]

    # Run multiple iterations
    times = []
    for strategy in strategies:
        for _ in range(50):
            result = benchmark_function(sanitize_strategy, strategy)
            times.append(result["time_taken"])

    avg_time = sum(times) / len(times)
    assert avg_time < 0.01  # Average should be very fast


if __name__ == "__main__":
    # Run benchmarks
    print("Running Performance Benchmarks")
    print("=" * 40)

    # Test sanitize functions
    print("\n1. Sanitize Functions Performance:")
    test_sanitize_functions_performance()
    print("   ✓ All sanitize functions perform well")

    # Test CSV processing
    print("\n2. CSV Processing Performance:")
    test_csv_processing_performance()
    print("   ✓ CSV processing performs well")

    # Test shortcode processing
    print("\n3. Shortcode Processing Performance:")
    test_shortcode_processing_performance()
    print("   ✓ Shortcode processing performs well")

    # Test chart options parsing
    print("\n4. Chart Options Parsing Performance:")
    test_chart_options_parsing_performance()
    print("   ✓ Chart options parsing performs well")

    # Test strategy sanitization
    print("\n5. Strategy Sanitization Performance:")
    test_strategy_sanitization_performance()
    print("   ✓ Strategy sanitization performs well")

    print("\nAll performance benchmarks completed successfully!")
