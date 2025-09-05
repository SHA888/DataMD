import os
import sys

# Add the python_implementation directory to the path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "python_implementation")
)

import pandas as pd
import pytest
from data_transform import DataTransformer, apply_transformations


def test_data_transformer_integration():
    """Test DataTransformer with various operations"""
    # Create a sample DataFrame
    df = pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
            "age": [25, 30, 35, 28, 22],
            "salary": [50000, 60000, 70000, 55000, 45000],
            "department": [
                "Engineering",
                "Marketing",
                "Engineering",
                "HR",
                "Marketing",
            ],
        }
    )

    # Test chaining multiple operations
    transformer = DataTransformer(df)
    result = transformer.filter("age > 25").sort("age").limit(2)
    result_df = result.get_dataframe()

    assert len(result_df) == 2
    assert result_df.iloc[0]["name"] == "David"  # Age 28
    assert result_df.iloc[1]["name"] == "Bob"  # Age 30


def test_apply_transformations_integration():
    """Test apply_transformations function"""
    # Create a sample DataFrame
    df = pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
            "age": [25, 30, 35, 28, 22],
            "salary": [50000, 60000, 70000, 55000, 45000],
            "department": [
                "Engineering",
                "Marketing",
                "Engineering",
                "HR",
                "Marketing",
            ],
        }
    )

    # Test complex transformation string
    transform_str = "filter:age>25|sort:age|limit:2"
    result_df = apply_transformations(df, transform_str)

    assert len(result_df) == 2
    assert result_df.iloc[0]["name"] == "David"  # Age 28
    assert result_df.iloc[1]["name"] == "Bob"  # Age 30

    # Test empty transformation
    result_df = apply_transformations(df, "")
    assert len(result_df) == len(df)


if __name__ == "__main__":
    pytest.main([__file__])
