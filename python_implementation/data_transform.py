import re
from typing import Any, Dict, List, Optional, Union

import pandas as pd


class DataTransformer:
    """
    Data transformation class for DataMD.

    Supports filtering, sorting, and aggregation operations on pandas DataFrames.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initialize DataTransformer with a DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to transform
        """
        self.df = df.copy()

    def filter(self, condition: str) -> "DataTransformer":
        """
        Filter DataFrame based on a condition.

        Args:
            condition (str): Filter condition in format "column operator value"
                            Supported operators: ==, !=, <, >, <=, >=, contains

        Returns:
            DataTransformer: New transformer with filtered data
        """
        if not condition:
            return self

        # Parse condition: column operator value
        # Support simple conditions like "age > 25" or "name contains John"
        # Also support "age>25" without spaces
        pattern = (
            r"^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*(==|!=|<|>|<=|>=|contains)\s*(.+?)\s*$"
        )
        match = re.match(pattern, condition)
        if not match:
            raise ValueError(f"Invalid filter condition: {condition}")

        column, operator, value = match.groups()

        # Check if column exists
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame")

        # Convert value to appropriate type
        try:
            # Try to convert to number first
            if "." in value:
                value = float(value)
            else:
                value = int(value)
        except ValueError:
            # Keep as string, remove quotes if present
            value = value.strip("\"'")

        # Apply filter based on operator
        if operator == "==":
            filtered_df = self.df[self.df[column] == value]
        elif operator == "!=":
            filtered_df = self.df[self.df[column] != value]
        elif operator == "<":
            filtered_df = self.df[self.df[column] < value]
        elif operator == ">":
            filtered_df = self.df[self.df[column] > value]
        elif operator == "<=":
            filtered_df = self.df[self.df[column] <= value]
        elif operator == ">=":
            filtered_df = self.df[self.df[column] >= value]
        elif operator == "contains":
            filtered_df = self.df[
                self.df[column].astype(str).str.contains(value, case=False, na=False)
            ]
        else:
            raise ValueError(f"Unsupported operator: {operator}")

        return DataTransformer(filtered_df)

    def sort(
        self, columns: Union[str, List[str]], ascending: bool = True
    ) -> "DataTransformer":
        """
        Sort DataFrame by one or more columns.

        Args:
            columns (str or list): Column name or list of column names to sort by
            ascending (bool): Sort order (True for ascending, False for descending)

        Returns:
            DataTransformer: New transformer with sorted data
        """
        if isinstance(columns, str):
            columns = [columns]

        # Check if all columns exist
        for col in columns:
            if col not in self.df.columns:
                raise ValueError(f"Column '{col}' not found in DataFrame")

        sorted_df = self.df.sort_values(by=columns, ascending=ascending)
        return DataTransformer(sorted_df)

    def aggregate(
        self,
        group_by: Optional[Union[str, List[str]]] = None,
        aggregations: Optional[Dict[str, str]] = None,
    ) -> "DataTransformer":
        """
        Aggregate data by grouping and applying aggregation functions.

        Args:
            group_by (str or list, optional): Column(s) to group by
            aggregations (dict, optional): Dictionary mapping column names to
                                          aggregation functions
                                          Supported functions: sum, mean, count,
                                          min, max, std

        Returns:
            DataTransformer: New transformer with aggregated data
        """
        if group_by is None and aggregations is None:
            return self

        # Handle grouping
        if group_by is not None:
            if isinstance(group_by, str):
                group_by = [group_by]

            # Check if all group columns exist
            for col in group_by:
                if col not in self.df.columns:
                    raise ValueError(f"Column '{col}' not found in DataFrame")

            grouped = self.df.groupby(group_by)
        else:
            grouped = self.df.groupby(lambda x: True)  # Group all rows together

        # Apply aggregations
        if aggregations is not None:
            agg_dict = {}
            supported_funcs = {"sum", "mean", "count", "min", "max", "std"}

            for col, func in aggregations.items():
                if col not in self.df.columns:
                    raise ValueError(f"Column '{col}' not found in DataFrame")
                if func not in supported_funcs:
                    raise ValueError(f"Unsupported aggregation function: {func}")
                agg_dict[col] = func

            aggregated_df = grouped.agg(agg_dict).reset_index()
        else:
            # If no aggregations specified, just return the grouped data
            aggregated_df = grouped.apply(lambda x: x).reset_index()

        return DataTransformer(aggregated_df)

    def limit(self, n: int) -> "DataTransformer":
        """
        Limit the number of rows in the DataFrame.

        Args:
            n (int): Number of rows to limit to

        Returns:
            DataTransformer: New transformer with limited data
        """
        if n <= 0:
            raise ValueError("Limit must be a positive integer")

        limited_df = self.df.head(n)
        return DataTransformer(limited_df)

    def get_dataframe(self) -> pd.DataFrame:
        """
        Get the transformed DataFrame.

        Returns:
            pd.DataFrame: The transformed DataFrame
        """
        return self.df

    def to_markdown(self, index: bool = False) -> str:
        """
        Convert DataFrame to markdown table.

        Args:
            index (bool): Whether to include index in output

        Returns:
            str: Markdown table representation
        """
        return self.df.to_markdown(index=index)


def parse_transform_string(transform_str: str) -> List[Dict[str, Any]]:
    """
    Parse a transformation string into a list of transformation operations.

    Args:
        transform_str (str): Transformation string with operations separated by |
                             Example: "filter:age>25|sort:name|limit:10"

    Returns:
        list: List of transformation operations as dictionaries
    """
    if not transform_str:
        return []

    operations = []
    parts = transform_str.split("|")

    for part in parts:
        part = part.strip()
        if ":" in part:
            op_type, op_args = part.split(":", 1)
            op_type = op_type.strip().lower()
            op_args = op_args.strip()

            if op_type == "filter":
                operations.append({"type": "filter", "condition": op_args})
            elif op_type == "sort":
                # Check for descending order
                ascending = True
                if op_args.startswith("-"):
                    ascending = False
                    op_args = op_args[1:]
                operations.append(
                    {"type": "sort", "columns": op_args, "ascending": ascending}
                )
            elif op_type == "limit":
                try:
                    limit = int(op_args)
                    operations.append({"type": "limit", "n": limit})
                except ValueError:
                    raise ValueError(f"Invalid limit value: {op_args}")
            elif op_type == "groupby":
                operations.append({"type": "groupby", "columns": op_args})
            else:
                raise ValueError(f"Unsupported transformation operation: {op_type}")
        else:
            # Handle operations without arguments
            op_type = part.strip().lower()
            if op_type == "sort":
                operations.append({"type": "sort", "columns": None})
            else:
                raise ValueError(f"Invalid transformation operation: {part}")

    return operations


def apply_transformations(df: pd.DataFrame, transform_str: str) -> pd.DataFrame:
    """
    Apply transformations to a DataFrame based on a transformation string.

    Args:
        df (pd.DataFrame): DataFrame to transform
        transform_str (str): Transformation string

    Returns:
        pd.DataFrame: Transformed DataFrame
    """
    if not transform_str:
        return df

    transformer = DataTransformer(df)
    operations = parse_transform_string(transform_str)

    for op in operations:
        op_type = op["type"]
        if op_type == "filter":
            transformer = transformer.filter(op["condition"])
        elif op_type == "sort":
            columns = op.get("columns")
            if columns:
                transformer = transformer.sort(columns, op.get("ascending", True))
            else:
                # Sort by all columns
                transformer = transformer.sort(
                    list(df.columns), op.get("ascending", True)
                )
        elif op_type == "limit":
            transformer = transformer.limit(op["n"])
        elif op_type == "groupby":
            # Groupby needs to be combined with aggregations
            # For now, we'll just note the groupby operation
            pass

    return transformer.get_dataframe()
