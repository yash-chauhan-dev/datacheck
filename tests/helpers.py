"""Test helper utilities and data generators."""

from pathlib import Path
from typing import Any

import pandas as pd


class DataFrameFactory:
    """Factory for creating test DataFrames with various characteristics."""

    @staticmethod
    def create_simple(rows: int = 3) -> pd.DataFrame:
        """Create a simple DataFrame with basic columns.

        Args:
            rows: Number of rows to generate

        Returns:
            DataFrame with name, age, city columns
        """
        names = ["Alice", "Bob", "Carol", "David", "Eve", "Frank", "Grace"][:rows]
        ages = [30, 25, 35, 28, 32, 45, 29][:rows]
        cities = ["NYC", "LA", "SF", "Chicago", "Boston", "Seattle", "Austin"][:rows]

        return pd.DataFrame({"name": names, "age": ages, "city": cities})

    @staticmethod
    def create_with_nulls(null_percentage: float = 0.3) -> pd.DataFrame:
        """Create DataFrame with specified percentage of null values.

        Args:
            null_percentage: Percentage of cells to set as null (0.0-1.0)

        Returns:
            DataFrame with null values
        """
        import numpy as np

        df = DataFrameFactory.create_simple(rows=10)
        # Set random cells to null
        mask = pd.DataFrame(
            np.random.random(df.shape) < null_percentage, columns=df.columns, index=df.index
        )
        result: pd.DataFrame = df.where(~mask)
        return result

    @staticmethod
    def create_with_outliers() -> pd.DataFrame:
        """Create DataFrame with outlier values for testing validation.

        Returns:
            DataFrame with outlier values
        """
        return pd.DataFrame({
            "name": ["Alice", "Bob", "Carol", ""],  # Empty string
            "age": [30, 150, -5, 25],  # 150 too high, -5 negative
            "value": [100.0, 1e10, -1e10, 50.0],  # Extreme values
            "category": ["A", "B", "Invalid", "A"],  # Invalid category
        })

    @staticmethod
    def create_large(rows: int = 10000) -> pd.DataFrame:
        """Create a large DataFrame for performance testing.

        Args:
            rows: Number of rows to generate

        Returns:
            Large DataFrame
        """
        import numpy as np

        return pd.DataFrame({
            "id": range(rows),
            "value": np.random.randn(rows),
            "category": np.random.choice(["A", "B", "C", "D"], rows),
            "flag": np.random.choice([True, False], rows),
        })


class ConfigFactory:
    """Factory for creating test configuration dictionaries."""

    @staticmethod
    def create_simple() -> dict[str, Any]:
        """Create a simple validation configuration.

        Returns:
            Configuration dictionary
        """
        return {
            "checks": [
                {"name": "age_check", "column": "age", "rules": {"not_null": True, "min": 0, "max": 120}},
                {"name": "name_check", "column": "name", "rules": {"not_null": True, "min_length": 1}},
            ]
        }

    @staticmethod
    def create_complex() -> dict[str, Any]:
        """Create a complex validation configuration with multiple rules.

        Returns:
            Complex configuration dictionary
        """
        return {
            "checks": [
                {
                    "name": "age_validation",
                    "column": "age",
                    "rules": {"not_null": True, "min": 0, "max": 120, "dtype": "int"},
                },
                {
                    "name": "name_validation",
                    "column": "name",
                    "rules": {"not_null": True, "min_length": 1, "max_length": 100, "regex": "^[A-Za-z ]+$"},
                },
                {
                    "name": "email_validation",
                    "column": "email",
                    "rules": {"not_null": True, "regex": r".+@.+\..+"},
                },
                {
                    "name": "value_validation",
                    "column": "value",
                    "rules": {"min": 0, "max": 1000000, "dtype": "float"},
                },
            ]
        }

    @staticmethod
    def create_with_all_rules() -> dict[str, Any]:
        """Create configuration using all available rule types.

        Returns:
            Configuration with all rule types
        """
        return {
            "checks": [
                {
                    "name": "comprehensive_check",
                    "column": "test_col",
                    "rules": {
                        "not_null": True,
                        "unique": True,
                        "min": 0,
                        "max": 100,
                        "min_length": 1,
                        "max_length": 50,
                        "regex": "^[A-Z]",
                        "dtype": "str",
                        "allowed_values": ["A", "B", "C"],
                    },
                }
            ]
        }


class FileFactory:
    """Factory for creating test files."""

    @staticmethod
    def create_csv(path: Path, df: pd.DataFrame | None = None) -> Path:
        """Create a CSV file for testing.

        Args:
            path: Path where file should be created
            df: DataFrame to write, or None to create default

        Returns:
            Path to created CSV file
        """
        if df is None:
            df = DataFrameFactory.create_simple()
        df.to_csv(path, index=False)
        return path

    @staticmethod
    def create_parquet(path: Path, df: pd.DataFrame | None = None) -> Path:
        """Create a Parquet file for testing.

        Args:
            path: Path where file should be created
            df: DataFrame to write, or None to create default

        Returns:
            Path to created Parquet file
        """
        if df is None:
            df = DataFrameFactory.create_simple()
        df.to_parquet(path, index=False)
        return path

    @staticmethod
    def create_config_yaml(path: Path, config: dict[str, Any] | None = None) -> Path:
        """Create a YAML config file for testing.

        Args:
            path: Path where file should be created
            config: Configuration dict, or None to create default

        Returns:
            Path to created config file
        """
        import yaml

        if config is None:
            config = ConfigFactory.create_simple()

        with open(path, "w") as f:
            yaml.dump(config, f, default_flow_style=False)
        return path


def assert_validation_passed(result: Any) -> None:
    """Assert that validation passed successfully.

    Args:
        result: Validation result object

    Raises:
        AssertionError: If validation did not pass
    """
    assert hasattr(result, "all_passed"), "Result must have 'all_passed' attribute"
    assert result.all_passed, f"Validation should have passed but got failures: {result}"


def assert_validation_failed(result: Any, expected_failures: int | None = None) -> None:
    """Assert that validation failed as expected.

    Args:
        result: Validation result object
        expected_failures: Expected number of failures, or None to just check it failed

    Raises:
        AssertionError: If validation did not fail as expected
    """
    assert hasattr(result, "all_passed"), "Result must have 'all_passed' attribute"
    assert not result.all_passed, "Validation should have failed but passed"

    if expected_failures is not None:
        assert hasattr(result, "failed_rules"), "Result must have 'failed_rules' attribute"
        actual_failures = result.failed_rules
        assert (
            actual_failures == expected_failures
        ), f"Expected {expected_failures} failures but got {actual_failures}"


def assert_has_error(result: Any, error_msg: str | None = None) -> None:
    """Assert that result has an error.

    Args:
        result: Result object to check
        error_msg: Expected error message substring, or None to just check for error

    Raises:
        AssertionError: If no error found or message doesn't match
    """
    assert hasattr(result, "has_errors"), "Result must have 'has_errors' attribute"
    assert result.has_errors, "Result should have errors but has none"

    if error_msg is not None:
        assert hasattr(result, "error"), "Result must have 'error' attribute"
        assert error_msg in str(result.error), f"Expected error message '{error_msg}' not found in '{result.error}'"
