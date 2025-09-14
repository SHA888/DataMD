# Remove unused pytest import
# import pytest

from python_implementation.datamd_ext import sanitize_chart_options, sanitize_chart_type


def test_sanitize_chart_type():
    """Test sanitize_chart_type function."""
    # Test valid chart types
    assert sanitize_chart_type("bar") == "bar"
    assert sanitize_chart_type("BAR") == "bar"  # Case insensitive
    assert sanitize_chart_type("line") == "line"
    assert sanitize_chart_type("pie") == "pie"
    assert sanitize_chart_type("scatter") == "scatter"
    assert sanitize_chart_type("histogram") == "histogram"

    # Test invalid chart type
    assert sanitize_chart_type("invalid") == "bar"  # Default
    assert sanitize_chart_type("") == "bar"  # Default
    assert sanitize_chart_type(None) == "bar"  # Default


def test_sanitize_chart_options():
    """Test sanitize_chart_options function."""
    # Test empty options
    assert sanitize_chart_options("") == {}
    assert sanitize_chart_options(None) == {}

    # Test simple options
    result = sanitize_chart_options("title=Sales Chart")
    assert result == {"title": "Sales Chart"}

    # Test multiple options
    result = sanitize_chart_options("title=Sales Chart,color=blue,width=10")
    expected = {"title": "Sales Chart", "color": "blue", "width": 10}
    assert result == expected

    # Test numeric values
    result = sanitize_chart_options("width=10,height=5.5")
    expected = {"width": 10, "height": 5.5}
    assert result == expected

    # Test boolean values
    result = sanitize_chart_options("grid=true,alpha=0.5")
    expected = {"grid": True, "alpha": 0.5}
    assert result == expected

    # Test complex title with spaces
    result = sanitize_chart_options("title=Monthly Sales Report,xlabel=Month")
    expected = {"title": "Monthly Sales Report", "xlabel": "Month"}
    assert result == expected


def test_sanitize_chart_options_edge_cases():
    """Test edge cases for sanitize_chart_options function."""
    # Test options with extra spaces
    result = sanitize_chart_options(" title = Sales Chart , color = blue ")
    # Note: Current implementation doesn't strip spaces, so they're preserved
    expected = {" title ": " Sales Chart ", " color ": " blue "}
    assert result == expected

    # Test malformed options
    result = sanitize_chart_options("title=,color=blue")
    expected = {"title": "", "color": "blue"}
    assert result == expected

    # Test option without value
    result = sanitize_chart_options("title,color=blue")
    expected = {"color": "blue"}
    assert result == expected


def test_sanitize_chart_type_case_insensitive():
    """Test that chart type sanitization is case insensitive."""
    # Test various case combinations
    assert sanitize_chart_type("BAR") == "bar"
    assert sanitize_chart_type("Bar") == "bar"
    assert sanitize_chart_type("Line") == "line"
    assert sanitize_chart_type("PIE") == "pie"
    assert sanitize_chart_type("Scatter") == "scatter"
    assert sanitize_chart_type("HISTOGRAM") == "histogram"


def test_sanitize_chart_options_complex_values():
    """Test chart options with complex values."""
    # Test options with quoted values (if supported)
    result = sanitize_chart_options('title="Sales Report",color=red')
    expected = {"title": '"Sales Report"', "color": "red"}
    assert result == expected

    # Test options with special characters
    result = sanitize_chart_options("title=Sales & Profit,color=#FF0000")
    expected = {"title": "Sales & Profit", "color": "#FF0000"}
    assert result == expected
