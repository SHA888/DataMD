import os
import sys

# Add the python_implementation directory to the path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "python_implementation")
)

import pytest
from datamd_ext import sanitize_chart_options, sanitize_chart_type


def test_sanitize_chart_type():
    """Test chart type sanitization"""
    # Valid chart types
    assert sanitize_chart_type("bar") == "bar"
    assert sanitize_chart_type("line") == "line"
    assert sanitize_chart_type("pie") == "pie"
    assert sanitize_chart_type("scatter") == "scatter"
    assert sanitize_chart_type("histogram") == "histogram"

    # Case insensitive
    assert sanitize_chart_type("BAR") == "bar"
    assert sanitize_chart_type("Line") == "line"

    # Invalid chart types default to bar
    assert sanitize_chart_type("invalid") == "bar"
    assert sanitize_chart_type("") == "bar"
    assert sanitize_chart_type(None) == "bar"


def test_sanitize_chart_options():
    """Test chart options sanitization"""
    # Valid options
    options = sanitize_chart_options("title=Sales Chart,xlabel=Month,ylabel=Sales")
    assert options["title"] == "Sales Chart"
    assert options["xlabel"] == "Month"
    assert options["ylabel"] == "Sales"

    # Numeric values
    options = sanitize_chart_options("width=10,height=5.5")
    assert options["width"] == 10
    assert options["height"] == 5.5

    # Boolean values
    options = sanitize_chart_options("show_grid=true,legend=false")
    assert options["show_grid"] is True
    assert options["legend"] is False

    # Empty options
    options = sanitize_chart_options("")
    assert options == {}

    options = sanitize_chart_options(None)
    assert options == {}


def test_chart_shortcode_parsing():
    """Test chart shortcode parsing in DataMDPreprocessor"""
    # This would require more complex testing with actual preprocessing
    # For now, we'll test the helper functions
    pass


if __name__ == "__main__":
    pytest.main([__file__])
