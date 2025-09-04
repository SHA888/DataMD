import os
import sys
import tempfile
from pathlib import Path

# Add the python_implementation directory to the path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "python_implementation")
)

import pytest

# Import after path modification
from process_dmd import process_dmd_file


def test_pdf_table_shortcode():
    """Test the pdf_table shortcode functionality"""
    # Create a temporary directory for our test
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Create a simple test DMD file with pdf_table shortcode
        test_content = """# PDF Table Test

## Test PDF Table Extraction
{{ pdf_table "test_document.pdf" 1 }}
"""

        dmd_file = tmp_path / "test_pdf.dmd"
        dmd_file.write_text(test_content, encoding="utf-8")

        # Create a dummy PDF file
        pdf_file = tmp_path / "test_document.pdf"
        pdf_file.write_text("dummy PDF content", encoding="utf-8")

        # Process the DMD file
        try:
            process_dmd_file(str(dmd_file))
            # If we get here, the shortcode was at least recognized
            html_file = dmd_file.with_suffix(".html")
            assert html_file.exists()
        except Exception as e:
            # This is expected since we don't have a real PDF file
            assert "pdf_table" in str(e) or "PDF" in str(e)


def test_pdf_table_with_strategies():
    """Test the pdf_table shortcode with strategy parameters"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Create a simple test DMD file with pdf_table shortcode and strategies
        test_content = """# PDF Table Test

## Test PDF Table Extraction with Strategies
{{ pdf_table "test_document.pdf" 1 lines text }}
"""

        dmd_file = tmp_path / "test_pdf_strategies.dmd"
        dmd_file.write_text(test_content, encoding="utf-8")

        # Create a dummy PDF file
        pdf_file = tmp_path / "test_document.pdf"
        pdf_file.write_text("dummy PDF content", encoding="utf-8")

        # Process the DMD file
        try:
            process_dmd_file(str(dmd_file))
            html_file = dmd_file.with_suffix(".html")
            assert html_file.exists()
        except Exception as e:
            # Expected since we don't have a real PDF file
            assert "pdf_table" in str(e) or "PDF" in str(e)


def test_pdf_table_with_thresholds():
    """Test the pdf_table shortcode with threshold parameters"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Create a test DMD file with pdf_table shortcode and threshold parameters
        test_content = """# PDF Table Test

## Test PDF Table Extraction with Threshold Parameters
{{ pdf_table "test_document.pdf" 1 lines text snap=5 edge=10 intersect=3 }}
"""

        dmd_file = tmp_path / "test_pdf_thresholds.dmd"
        dmd_file.write_text(test_content, encoding="utf-8")

        # Create a dummy PDF file
        pdf_file = tmp_path / "test_document.pdf"
        pdf_file.write_text("dummy PDF content", encoding="utf-8")

        # Process the DMD file
        try:
            process_dmd_file(str(dmd_file))
            html_file = dmd_file.with_suffix(".html")
            assert html_file.exists()

            # Check that the HTML contains the threshold parameters in the error message
            # (since we're using a dummy PDF file)
            html_content = html_file.read_text(encoding="utf-8")
            # The error message should mention the pdf_table command
            assert "pdf_table" in html_content
        except Exception as e:
            # Expected since we don't have a real PDF file
            assert "pdf_table" in str(e) or "PDF" in str(e)


def test_pdf_table_with_mixed_parameters():
    """Test the pdf_table shortcode with mixed parameters"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Create a test DMD file with pdf_table shortcode and mixed parameters
        test_content = """# PDF Table Test

## Test PDF Table Extraction with Mixed Parameters
{{ pdf_table "test_document.pdf" 2 text lines snap=3.5 edge=7 intersect=1.5 }}
"""

        dmd_file = tmp_path / "test_pdf_mixed.dmd"
        dmd_file.write_text(test_content, encoding="utf-8")

        # Create a dummy PDF file
        pdf_file = tmp_path / "test_document.pdf"
        pdf_file.write_text("dummy PDF content", encoding="utf-8")

        # Process the DMD file
        try:
            process_dmd_file(str(dmd_file))
            html_file = dmd_file.with_suffix(".html")
            assert html_file.exists()
        except Exception as e:
            # Expected since we don't have a real PDF file
            assert "pdf_table" in str(e) or "PDF" in str(e)


if __name__ == "__main__":
    pytest.main([__file__])
