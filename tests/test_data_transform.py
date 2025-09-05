import os
import sys

# Add the python_implementation directory to the path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "python_implementation")
)

import pandas as pd
import pytest
from data_transform import (
    DataTransformer,
    apply_transformations,
    parse_transform_string,
)


def test_data_transformer_init():
    """Test DataTransformer initialization"""
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    transformer = DataTransformer(df)

    # Should create a copy of the DataFrame
    assert transformer.df is not df
    assert transformer.df.equals(df)


def test_data_transformer_filter():
    """Test DataTransformer filter method"""
    df = pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie", "David"],
            "age": [25, 30, 35, 20],
            "city": ["New York", "London", "Paris", "Tokyo"],
        }
    )
    transformer = DataTransformer(df)

    # Test equality filter
    filtered = transformer.filter("age == 30")
    expected = pd.DataFrame({"name": ["Bob"], "age": [30], "city": ["London"]})
    assert filtered.get_dataframe().reset_index(drop=True).equals(expected)

    # Test inequality filter
    filtered = transformer.filter("age > 25")
    expected = pd.DataFrame(
        {"name": ["Bob", "Charlie"], "age": [30, 35], "city": ["London", "Paris"]}
    )
    assert filtered.get_dataframe().reset_index(drop=True).equals(expected)

    # Test string contains filter
    filtered = transformer.filter("city contains york")
    expected = pd.DataFrame({"name": ["Alice"], "age": [25], "city": ["New York"]})
    assert filtered.get_dataframe().reset_index(drop=True).equals(expected)


def test_data_transformer_sort():
    """Test DataTransformer sort method"""
    df = pd.DataFrame(
        {
            "name": ["Charlie", "Alice", "Bob"],
            "age": [35, 25, 30],
            "score": [85, 95, 75],
        }
    )
    transformer = DataTransformer(df)

    # Test single column sort
    sorted_transformer = transformer.sort("age")
    expected = pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35],
            "score": [95, 75, 85],
        }
    )
    assert sorted_transformer.get_dataframe().reset_index(drop=True).equals(expected)

    # Test multi-column sort
    sorted_transformer = transformer.sort(["age", "score"])
    expected = pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35],
            "score": [95, 75, 85],
        }
    )
    assert sorted_transformer.get_dataframe().reset_index(drop=True).equals(expected)


def test_data_transformer_limit():
    """Test DataTransformer limit method"""
    df = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [10, 20, 30, 40, 50]})
    transformer = DataTransformer(df)

    # Test limit
    limited = transformer.limit(3)
    expected = pd.DataFrame({"A": [1, 2, 3], "B": [10, 20, 30]})
    assert limited.get_dataframe().reset_index(drop=True).equals(expected)


def test_data_transformer_to_markdown():
    """Test DataTransformer to_markdown method"""
    df = pd.DataFrame({"name": ["Alice", "Bob"], "age": [25, 30]})
    transformer = DataTransformer(df)

    # Test markdown conversion
    markdown = transformer.to_markdown()
    expected = """| name   |   age |
|:-------|------:|
| Alice  |    25 |
| Bob    |    30 |"""
    assert markdown.strip() == expected.strip()


def test_parse_transform_string():
    """Test parse_transform_string function"""
    # Test empty string
    assert parse_transform_string("") == []

    # Test single operation
    result = parse_transform_string("filter:age>25")
    expected = [{"type": "filter", "condition": "age>25"}]
    assert result == expected

    # Test multiple operations
    result = parse_transform_string("filter:age>25|sort:name|limit:10")
    expected = [
        {"type": "filter", "condition": "age>25"},
        {"type": "sort", "columns": "name", "ascending": True},
        {"type": "limit", "n": 10},
    ]
    assert result == expected

    # Test sort with descending order
    result = parse_transform_string("sort:-name")
    expected = [{"type": "sort", "columns": "name", "ascending": False}]
    assert result == expected


def test_apply_transformations():
    """Test apply_transformations function"""
    df = pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie", "David"],
            "age": [25, 30, 35, 28],
            "salary": [50000, 60000, 70000, 55000],
            "department": ["IT", "HR", "IT", "Finance"],
        }
    )

    # Test None transform
    result = apply_transformations(df, None)
    # Use 'is' instead of '!=' for None comparison
    assert result is not None
    assert result.equals(df)

    # Test empty transform
    result = apply_transformations(df, "")
    assert result is not None
    assert result.equals(df)

    # Test filter transformation
    result = apply_transformations(df, "filter:age>25")
    expected = pd.DataFrame(
        {
            "name": ["Bob", "Charlie", "David"],
            "age": [30, 35, 28],
            "salary": [60000, 70000, 55000],
            "department": ["HR", "IT", "Finance"],
        }
    )
    assert result.reset_index(drop=True).equals(expected)


if __name__ == "__main__":
    pytest.main([__file__])
