import os
import sys
import tempfile
from pathlib import Path

# Add the python_implementation directory to the path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "python_implementation")
)

import pytest
from datamd_ext import process_large_csv, read_csv_chunked


def test_read_csv_chunked():
    """Test reading CSV files in chunks"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        csv_file = tmp_path / "test.csv"

        # Create a test CSV file with multiple rows
        csv_content = "name,age,city\n"
        for i in range(100):
            csv_content += f"Person{i},{20+i},City{i}\n"

        csv_file.write_text(csv_content)

        # Test reading in chunks
        chunks = list(read_csv_chunked(str(csv_file), chunk_size=25))

        # Should have 4 chunks of 25 rows each
        assert len(chunks) == 4
        for chunk in chunks:
            assert len(chunk) == 25
            assert list(chunk.columns) == ["name", "age", "city"]


def test_process_large_csv():
    """Test processing large CSV files"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        csv_file = tmp_path / "large_test.csv"

        # Create a test CSV file
        csv_content = "name,age,city\n"
        for i in range(150):
            csv_content += f"Person{i},{20+i},City{i}\n"

        csv_file.write_text(csv_content)

        # Process as large file
        result = process_large_csv(str(csv_file), sep=",", max_memory_mb=1)

        # Should contain preview data and note about large file
        assert "Person0" in result
        assert "Person1" in result
        assert "Large file detected" in result
        assert "Showing first 100 rows" in result


def test_read_excel_chunked():
    """Test reading Excel files in chunks"""
    # This test would require creating an Excel file, which is more complex
    # For now, we'll skip this test as it requires additional dependencies
    pass


if __name__ == "__main__":
    pytest.main([__file__])
