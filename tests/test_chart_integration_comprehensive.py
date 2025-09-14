import json
import os
import tempfile
from pathlib import Path

import pandas as pd

from python_implementation.datamd_ext import DataMDPreprocessor


def process_chart_shortcode(file_path, chart_type, x_col, y_col, options=""):
    """Process a chart shortcode and return the result."""
    # Create a mock preprocessor
    preprocessor = DataMDPreprocessor(None)

    # Create test lines with the shortcode
    if x_col and y_col and options:
        line = f'{{{{ chart "{file_path}" {chart_type} {x_col} {y_col} {options} }}}}'
    elif x_col and y_col:
        line = f'{{{{ chart "{file_path}" {chart_type} {x_col} {y_col} }}}}'
    else:
        line = f'{{{{ chart "{file_path}" {chart_type} }}}}'

    # Process the line
    result_lines = preprocessor.run([line])
    return result_lines[0] if result_lines else ""


def test_chart_shortcode_basic():
    """Test basic chart shortcode functionality."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Create test CSV
        csv_file = tmp_path / "test_data.csv"
        df = pd.DataFrame(
            {
                "month": ["Jan", "Feb", "Mar", "Apr"],
                "sales": [100, 150, 120, 200],
                "profit": [20, 30, 25, 40],
            }
        )
        df.to_csv(csv_file, index=False)

        # Test basic bar chart
        result = process_chart_shortcode(str(csv_file), "bar", "month", "sales")

        # Verify the result contains the chart markdown
        assert "![Bar chart](" in result or "![](chart_" in result
        assert ".png" in result


def test_chart_shortcode_with_title():
    """Test chart shortcode with custom title."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Create test CSV
        csv_file = tmp_path / "test_data.csv"
        df = pd.DataFrame(
            {"month": ["Jan", "Feb", "Mar", "Apr"], "sales": [100, 150, 120, 200]}
        )
        df.to_csv(csv_file, index=False)

        # Test chart with title
        # Break long line into multiple lines
        options = "title=Monthly Sales Report"
        result = process_chart_shortcode(
            str(csv_file), "bar", "month", "sales", options
        )

        # Verify the result contains the chart markdown with title
        assert "![Monthly Sales Report](" in result or "![](chart_" in result
        assert ".png" in result


def test_chart_shortcode_with_complex_data():
    """Test chart shortcode with complex data and multiple options."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Create test CSV with complex data
        csv_file = tmp_path / "complex_data.csv"
        csv_content = """category,month,value,percentage
A,Jan,100,10.5
A,Feb,150,15.2
B,Jan,200,20.1
B,Feb,180,18.3
C,Jan,120,12.4
C,Feb,160,16.7"""

        with open(csv_file, "w") as f:
            f.write(csv_content)

        # Test complex chart with many options
        # Break long line into multiple lines
        options = (
            "title=Complex Data Analysis,xlabel=Month,"
            "ylabel=Value,color=blue,width=12,height=8,grid=true,"
            "alpha=0.7"
        )
        result = process_chart_shortcode(
            str(csv_file), "bar", "month", "value", options
        )

        assert "![Complex Data Analysis](" in result or "![](chart_" in result
        assert ".png" in result


def test_chart_shortcode_line_chart():
    """Test line chart shortcode."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Create test CSV
        csv_file = tmp_path / "test_data.csv"
        df = pd.DataFrame(
            {
                "date": ["2023-01", "2023-02", "2023-03", "2023-04"],
                "value": [100, 150, 120, 200],
            }
        )
        df.to_csv(csv_file, index=False)

        # Test line chart
        # Break long line into multiple lines
        options = "title=Trend Analysis,xlabel=Date,ylabel=Value"
        result = process_chart_shortcode(
            str(csv_file), "line", "date", "value", options
        )

        assert ".png" in result


def test_chart_shortcode_pie_chart():
    """Test pie chart shortcode."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Create test CSV
        csv_file = tmp_path / "test_data.csv"
        df = pd.DataFrame({"category": ["A", "B", "C", "D"], "value": [30, 25, 20, 25]})
        df.to_csv(csv_file, index=False)

        # Test pie chart
        # Break long line into multiple lines
        options = "title=Category Distribution"
        result = process_chart_shortcode(
            str(csv_file), "pie", "category", "value", options
        )

        assert ".png" in result


def test_chart_shortcode_scatter_plot():
    """Test scatter plot shortcode."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Create test CSV
        csv_file = tmp_path / "test_data.csv"
        df = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": [2, 4, 6, 8, 10]})
        df.to_csv(csv_file, index=False)

        # Test scatter plot
        # Break long line into multiple lines
        options = "title=Scatter Plot,xlabel=X Values,ylabel=Y Values"
        result = process_chart_shortcode(str(csv_file), "scatter", "x", "y", options)

        assert ".png" in result


def test_chart_shortcode_histogram():
    """Test histogram shortcode."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Create test CSV
        csv_file = tmp_path / "test_data.csv"
        df = pd.DataFrame({"values": [1, 2, 2, 3, 3, 3, 4, 4, 5]})
        df.to_csv(csv_file, index=False)

        # Test histogram
        # Break long line into multiple lines
        options = "title=Value Distribution,xlabel=Values,ylabel=Frequency"
        result = process_chart_shortcode(
            str(csv_file), "histogram", "", "values", options
        )

        assert ".png" in result


def test_chart_shortcode_error_handling():
    """Test chart shortcode error handling."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Test with non-existent file
        non_existent_file = tmp_path / "non_existent.csv"
        result = process_chart_shortcode(str(non_existent_file), "bar", "x", "y")

        # Should contain error message
        assert "Error" in result or "error" in result

        # Test with invalid chart type
        csv_file = tmp_path / "test_data.csv"
        df = pd.DataFrame({"x": [1, 2], "y": [3, 4]})
        df.to_csv(csv_file, index=False)

        result = process_chart_shortcode(str(csv_file), "invalid", "x", "y")
        # Should fallback to bar chart
        assert ".png" in result
