import os
import sys
import tempfile
from pathlib import Path

# Add the python_implementation directory to the path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "python_implementation")
)

import pytest
from datamd_ext import process_csv_streaming, read_csv_chunked


def test_process_csv_streaming():
    """Test streaming processing of CSV files"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        csv_file = tmp_path / "test.csv"

        # Create a test CSV file with multiple rows
        csv_content = "name,age,city\n"
        for i in range(100):
            csv_content += f"Person{i},{20+i},City{i}\n"

        csv_file.write_text(csv_content)

        # Test streaming processing
        results = list(process_csv_streaming(str(csv_file), chunk_size=25))

        # Should have 4 chunks
        assert len(results) == 4

        # Check that each chunk is a markdown table
        for result in results:
            assert "| name" in result
            assert "| Person" in result


def test_process_csv_streaming_with_transform():
    """Test streaming processing of CSV files with transformations"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        csv_file = tmp_path / "test.csv"

        # Create a test CSV file
        csv_content = "name,age,city\n"
        for i in range(50):
            csv_content += f"Person{i},{20+i},City{i}\n"

        csv_file.write_text(csv_content)

        # Test streaming processing with filter transformation
        results = list(
            process_csv_streaming(
                str(csv_file), chunk_size=25, transform="filter:age>30"
            )
        )

        # Should have 2 chunks
        assert len(results) == 2

        # Check that results contain filtered data
        combined_result = "\n".join(results)
        assert "Person11" in combined_result  # Age 31
        assert "Person0" not in combined_result  # Age 20 (should be filtered out)


def test_read_csv_chunked_large_file():
    """Test reading large CSV files in chunks"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        csv_file = tmp_path / "large_test.csv"

        # Create a larger test CSV file
        csv_content = "id,value,category\n"
        for i in range(1000):
            csv_content += f"{i},value{i},category{i % 5}\n"

        csv_file.write_text(csv_content)

        # Test reading in chunks
        chunks = list(read_csv_chunked(str(csv_file), chunk_size=100))

        # Should have 10 chunks of 100 rows each
        assert len(chunks) == 10
        for i, chunk in enumerate(chunks):
            assert len(chunk) == 100
            assert list(chunk.columns) == ["id", "value", "category"]
            # Check that the data is correct
            assert chunk.iloc[0]["id"] == i * 100


if __name__ == "__main__":
    pytest.main([__file__])
