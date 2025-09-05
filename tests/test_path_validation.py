import os
import sys
import tempfile
from pathlib import Path

# Add the python_implementation directory to the path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "python_implementation")
)

import pytest
from datamd_ext import resolve_secure_path


def test_resolve_secure_path_valid_relative():
    """Test resolving a valid relative path"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")

        # Test with the temp directory as base
        result = resolve_secure_path("test.txt", str(tmp_path))
        assert result == test_file.resolve()


def test_resolve_secure_path_valid_subdirectory():
    """Test resolving a valid path in a subdirectory"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        sub_dir = tmp_path / "subdir"
        sub_dir.mkdir()
        test_file = sub_dir / "test.txt"
        test_file.write_text("test content")

        # Test with the temp directory as base
        result = resolve_secure_path("subdir/test.txt", str(tmp_path))
        assert result == test_file.resolve()


def test_resolve_secure_path_directory_traversal():
    """Test that directory traversal attempts are blocked"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")

        # Try to access file with directory traversal
        with pytest.raises(ValueError, match="Path traversal attempt detected"):
            resolve_secure_path("../test.txt", str(tmp_path))


def test_resolve_secure_path_absolute_path_within_base():
    """Test resolving an absolute path that is within the base directory"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")

        # Test with absolute path
        result = resolve_secure_path(str(test_file), str(tmp_path))
        assert result == test_file.resolve()


def test_resolve_secure_path_absolute_path_outside_base():
    """Test that absolute paths outside the base directory are blocked"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")

        # Try to access a path outside the base directory
        with pytest.raises(
            ValueError,
            match="Access to path outside of working directory is not allowed",
        ):
            resolve_secure_path("/etc/passwd", str(tmp_path))


def test_resolve_secure_path_nonexistent_file():
    """Test that nonexistent files raise FileNotFoundError"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Try to access a nonexistent file
        with pytest.raises(FileNotFoundError, match="File not found"):
            resolve_secure_path("nonexistent.txt", str(tmp_path))


def test_resolve_secure_path_default_base_dir():
    """Test resolving a path with the default base directory (current working
    directory)"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        original_cwd = os.getcwd()
        try:
            # Change to temp directory
            os.chdir(tmp_dir)
            tmp_path = Path(tmp_dir)
            test_file = tmp_path / "test.txt"
            test_file.write_text("test content")

            # Test with default base directory
            result = resolve_secure_path("test.txt")
            assert result == test_file.resolve()
        finally:
            # Restore original working directory
            os.chdir(original_cwd)


if __name__ == "__main__":
    pytest.main([__file__])
