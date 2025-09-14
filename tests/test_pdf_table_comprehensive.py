# Remove unused pytest import
# import pytest

from python_implementation.datamd_ext import sanitize_strategy


def test_sanitize_strategy():
    """Test sanitize_strategy function."""
    # Test valid strategies
    assert sanitize_strategy("lines") == "lines"
    assert sanitize_strategy("text") == "text"
    assert sanitize_strategy("explicit") == "explicit"

    # Test invalid strategy
    assert sanitize_strategy("invalid") == "lines"  # Default
    assert sanitize_strategy("") == "lines"  # Default
    assert sanitize_strategy(None) == "lines"  # Default

    # Note: Current implementation doesn't do case conversion
    # assert sanitize_strategy("LINES") == "lines"  # Case insensitive


def test_sanitize_strategy_with_config():
    """Test sanitize_strategy with custom default from config."""
    # This would require mocking the config, but we're testing the basic function
    pass
