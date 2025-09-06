"""
Memory profiling script for DataMD large file handling.

This script profiles memory usage for different file processing approaches
to analyze current memory usage patterns and validate the effectiveness
of streaming/chunked processing implementations.
"""

import os
import tempfile
from pathlib import Path

import pandas as pd
import psutil


def get_memory_usage():
    """Get current memory usage in MB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024


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


def profile_standard_csv_reading(file_path):
    """Profile standard CSV reading (loads entire file into memory)."""
    start_memory = get_memory_usage()
    start_time = pd.Timestamp.now()

    df = pd.read_csv(file_path)

    end_time = pd.Timestamp.now()
    end_memory = get_memory_usage()

    return {
        "time_taken": (end_time - start_time).total_seconds(),
        "memory_usage": end_memory - start_memory,
        "shape": df.shape,
    }


def profile_chunked_csv_reading(file_path, chunk_size=10000):
    """Profile chunked CSV reading (processes file in chunks)."""
    start_memory = get_memory_usage()
    start_time = pd.Timestamp.now()

    total_rows = 0
    total_cols = 0

    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        total_rows += len(chunk)
        total_cols = len(chunk.columns)

    end_time = pd.Timestamp.now()
    end_memory = get_memory_usage()

    return {
        "time_taken": (end_time - start_time).total_seconds(),
        "memory_usage": end_memory - start_memory,
        "shape": (total_rows, total_cols),
    }


def profile_large_file_processing(file_path):
    """Profile large file processing function."""
    start_memory = get_memory_usage()
    start_time = pd.Timestamp.now()

    # Import here to avoid circular imports
    import sys

    sys.path.insert(
        0, os.path.join(os.path.dirname(__file__), "..", "python_implementation")
    )

    from datamd_ext import process_large_csv

    result = process_large_csv(file_path, sep=",", max_memory_mb=10)

    end_time = pd.Timestamp.now()
    end_memory = get_memory_usage()

    return {
        "time_taken": (end_time - start_time).total_seconds(),
        "memory_usage": end_memory - start_memory,
        "result_length": len(result) if isinstance(result, str) else 0,
    }


def main():
    """Run memory profiling tests."""
    print("Memory Profiling for DataMD Large File Handling")
    print("=" * 50)

    # Test with different file sizes
    test_sizes = [1000, 10000, 50000]

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        for size in test_sizes:
            print(f"\nTesting with {size} rows:")
            print("-" * 20)

            # Create test CSV
            csv_file = tmp_path / "large_test.csv"
            print(f"Creating test CSV with {size} rows...")
            create_test_csv(csv_file, size)

            file_size_mb = csv_file.stat().st_size / (1024 * 1024)
            print(f"Created {csv_file} with {file_size_mb:.2f} MB")

            # Profile standard reading
            print("Profiling standard CSV reading...")
            standard_result = profile_standard_csv_reading(csv_file)
            print(f"  Time taken: {standard_result['time_taken']:.2f} seconds")
            print(f"  Memory usage: {standard_result['memory_usage']:.2f} MB")
            print(f"  DataFrame shape: {standard_result['shape']}")

            # Profile chunked reading
            print("Profiling chunked CSV reading...")
            chunked_result = profile_chunked_csv_reading(csv_file)
            print(f"  Time taken: {chunked_result['time_taken']:.2f} seconds")
            print(f"  Memory usage: {chunked_result['memory_usage']:.2f} MB")
            print(f"  DataFrame shape: {chunked_result['shape']}")

            # Profile large file processing
            print("Profiling large file processing...")
            large_file_result = profile_large_file_processing(str(csv_file))
            print(f"  Time taken: {large_file_result['time_taken']:.2f} seconds")
            print(f"  Memory usage: {large_file_result['memory_usage']:.2f} MB")
            print(f"  Result length: {large_file_result['result_length']} characters")

            # Calculate memory savings
            if standard_result["memory_usage"] > 0:
                savings = (
                    (standard_result["memory_usage"] - chunked_result["memory_usage"])
                    / standard_result["memory_usage"]
                    * 100
                )
                print(
                    f"Chunked reading reduces memory usage by {savings:.0f}% "
                    f"compared to standard reading"
                )


if __name__ == "__main__":
    main()
