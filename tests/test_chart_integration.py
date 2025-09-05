import os
import sys
from pathlib import Path

# Add the python_implementation directory to the path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "python_implementation")
)

import pytest
from process_dmd import process_dmd_file


def test_chart_shortcode_integration():
    """Test the chart shortcode integration with actual data"""
    # Create a temporary directory for our test
    test_dir = Path(__file__).parent / "test_data"
    test_dir.mkdir(exist_ok=True)

    # Create a simple CSV file for testing
    csv_content = """month,sales,profit
January,1000,200
February,1200,250
March,800,150
April,1500,300
May,2000,400
"""

    csv_file = test_dir / "sales.csv"
    csv_file.write_text(csv_content, encoding="utf-8")

    # Create a test DMD file with chart shortcode
    test_content = f"""# Chart Test

## Sales Chart
{{{{ chart "{csv_file.name}" bar month sales title="Monthly Sales" }}}}
"""

    dmd_file = test_dir / "test_chart.dmd"
    dmd_file.write_text(test_content, encoding="utf-8")

    # Process the DMD file
    try:
        process_dmd_file(str(dmd_file))
        html_file = dmd_file.with_suffix(".html")
        assert html_file.exists()

        # Check that the HTML contains chart elements
        html_content = html_file.read_text(encoding="utf-8")
        assert "Monthly Sales" in html_content
        assert "chart" in html_content.lower()

    finally:
        # Clean up test files
        for file in test_dir.iterdir():
            if file.is_file():
                file.unlink()
        test_dir.rmdir()


if __name__ == "__main__":
    pytest.main([__file__])
