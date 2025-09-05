import os
import sys

# Add the python_implementation directory to the path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "python_implementation")
)

import pytest
from datamd_ext import (
    sanitize_boolean_input,
    sanitize_language_code,
    sanitize_numeric_input,
    sanitize_sheet_name,
    sanitize_strategy,
    sanitize_string_input,
)


def test_sanitize_numeric_input():
    """Test numeric input sanitization"""
    # Valid inputs
    assert sanitize_numeric_input("5") == 5
    assert sanitize_numeric_input("3.14") == 3.14
    assert sanitize_numeric_input("-2") == -2

    # With constraints
    assert sanitize_numeric_input("150", min_val=0, max_val=100) == 100
    assert sanitize_numeric_input("-5", min_val=0, max_val=100) == 0
    assert sanitize_numeric_input("50", min_val=0, max_val=100) == 50

    # Invalid inputs with defaults
    assert sanitize_numeric_input("abc", default=10) == 10
    assert sanitize_numeric_input("", default=5) == 5
    assert sanitize_numeric_input(None, default=3.14) == 3.14


def test_sanitize_boolean_input():
    """Test boolean input sanitization"""
    # Valid true values
    assert sanitize_boolean_input("true") is True
    assert sanitize_boolean_input("True") is True
    assert sanitize_boolean_input("1") is True
    assert sanitize_boolean_input("yes") is True
    assert sanitize_boolean_input("on") is True
    assert sanitize_boolean_input("enabled") is True

    # Valid false values
    assert sanitize_boolean_input("false") is False
    assert sanitize_boolean_input("False") is False
    assert sanitize_boolean_input("0") is False
    assert sanitize_boolean_input("no") is False

    # Invalid inputs with defaults
    assert sanitize_boolean_input("maybe", default=True) is True
    assert sanitize_boolean_input("", default=False) is False
    assert sanitize_boolean_input(None, default=True) is True


def test_sanitize_string_input():
    """Test string input sanitization"""
    # Valid inputs
    assert sanitize_string_input("hello") == "hello"
    assert sanitize_string_input("test string") == "test string"

    # Length constraints
    long_string = "a" * 1500
    sanitized = sanitize_string_input(long_string, max_length=1000)
    assert len(sanitized) == 1000

    # Character constraints
    result = sanitize_string_input("hello123", allowed_chars="helo")
    assert result == "hello"

    # Empty input
    assert sanitize_string_input("") == ""
    assert sanitize_string_input(None) == ""


def test_sanitize_language_code():
    """Test language code sanitization"""
    # Valid language codes
    assert sanitize_language_code("eng") == "eng"
    assert sanitize_language_code("spa") == "spa"
    assert sanitize_language_code("fra") == "fra"

    # Invalid language codes default to 'eng'
    assert sanitize_language_code("invalid") == "eng"
    assert sanitize_language_code("") == "eng"
    assert sanitize_language_code(None) == "eng"


def test_sanitize_sheet_name():
    """Test sheet name sanitization"""
    # Numeric sheet index
    assert sanitize_sheet_name("0") == 0
    assert sanitize_sheet_name("1") == 1
    assert sanitize_sheet_name("5") == 5

    # Sheet name strings
    assert sanitize_sheet_name("Sheet1") == "Sheet1"
    assert sanitize_sheet_name("") == 0

    # Long sheet names should be truncated
    long_name = "a" * 50
    sanitized = sanitize_sheet_name(long_name)
    assert len(sanitized) <= 31  # Excel sheet name limit


def test_sanitize_strategy():
    """Test PDF strategy sanitization"""
    # Valid strategies
    assert sanitize_strategy("lines") == "lines"
    assert sanitize_strategy("text") == "text"
    assert sanitize_strategy("explicit") == "explicit"

    # Invalid strategies default to 'lines'
    assert sanitize_strategy("invalid") == "lines"
    assert sanitize_strategy("") == "lines"
    assert sanitize_strategy(None) == "lines"


if __name__ == "__main__":
    pytest.main([__file__])
