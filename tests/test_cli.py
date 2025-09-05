import os
import sys
import tempfile
from pathlib import Path

# Add the python_implementation directory to the path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "python_implementation")
)

import pytest
from process_dmd import main


def test_cli_help():
    """Test that CLI help works"""
    # Test that help doesn't crash
    try:
        main(["--help"])
    except SystemExit:
        # argparse exits with SystemExit when --help is used, which is expected
        pass


def test_cli_version():
    """Test that CLI version works"""
    # Test that version doesn't crash
    try:
        main(["--version"])
    except SystemExit:
        # argparse exits with SystemExit when --version is used, which is expected
        pass


def test_cli_with_file():
    """Test CLI with a simple file"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Create a simple test DMD file
        test_content = """# Test

This is a test file.
"""

        dmd_file = tmp_path / "test.dmd"
        dmd_file.write_text(test_content, encoding="utf-8")

        # Test that processing doesn't crash
        try:
            main([str(dmd_file)])
            html_file = dmd_file.with_suffix(".html")
            assert html_file.exists()
        except SystemExit:
            # Main might exit, which is fine for this test
            pass


if __name__ == "__main__":
    pytest.main([__file__])
