"""Pytest configuration and shared fixtures."""

from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture
def sample_csv_path(tmp_path: Path) -> Path:
    """Create a sample CSV file for testing.

    Args:
        tmp_path: Pytest tmp_path fixture

    Returns:
        Path to created CSV file
    """
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("name,age,city\nAlice,30,NYC\nBob,25,LA\nCarol,35,SF\n")
    return csv_file


@pytest.fixture
def sample_parquet_path(tmp_path: Path) -> Path:
    """Create a sample Parquet file for testing.

    Args:
        tmp_path: Pytest tmp_path fixture

    Returns:
        Path to created Parquet file
    """
    df = pd.DataFrame({"name": ["Alice", "Bob", "Carol"], "age": [30, 25, 35], "city": ["NYC", "LA", "SF"]})
    parquet_file = tmp_path / "sample.parquet"
    df.to_parquet(parquet_file, index=False)
    return parquet_file


@pytest.fixture
def sample_config_path(tmp_path: Path) -> Path:
    """Create a sample configuration file for testing.

    Args:
        tmp_path: Pytest tmp_path fixture

    Returns:
        Path to created config file
    """
    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        """
checks:
  - name: age_check
    column: age
    rules:
      not_null: true
      min: 0
      max: 120

  - name: name_check
    column: name
    rules:
      not_null: true
      min_length: 1
"""
    )
    return config_file


@pytest.fixture
def empty_csv_path(tmp_path: Path) -> Path:
    """Create an empty CSV file (header only) for testing.

    Args:
        tmp_path: Pytest tmp_path fixture

    Returns:
        Path to created empty CSV file
    """
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("name,age,city\n")
    return csv_file


@pytest.fixture
def invalid_csv_path(tmp_path: Path) -> Path:
    """Create an invalid CSV file for testing.

    Args:
        tmp_path: Pytest tmp_path fixture

    Returns:
        Path to created invalid CSV file
    """
    csv_file = tmp_path / "invalid.csv"
    csv_file.write_text("not,valid,csv\ndata")
    return csv_file


@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    """Create a sample DataFrame for testing.

    Returns:
        Sample DataFrame
    """
    return pd.DataFrame({"name": ["Alice", "Bob", "Carol"], "age": [30, 25, 35], "city": ["NYC", "LA", "SF"]})


@pytest.fixture
def dataframe_with_nulls() -> pd.DataFrame:
    """Create a DataFrame with null values for testing.

    Returns:
        DataFrame with null values
    """
    return pd.DataFrame({"name": ["Alice", None, "Carol"], "age": [30, 25, None], "city": ["NYC", "LA", "SF"]})


@pytest.fixture
def dataframe_with_violations() -> pd.DataFrame:
    """Create a DataFrame with validation rule violations.

    Returns:
        DataFrame with values that violate common validation rules
    """
    return pd.DataFrame({
        "name": ["Alice", "", "Carol"],  # Empty string violates min_length
        "age": [30, 150, -5],  # 150 > max, -5 < min
        "city": ["NYC", "LA", "SF"],
    })


def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest with custom markers.

    Args:
        config: Pytest configuration object
    """
    config.addinivalue_line("markers", "unit: Unit tests that don't require external dependencies")
    config.addinivalue_line("markers", "integration: Integration tests that test multiple components")
    config.addinivalue_line("markers", "slow: Tests that take longer to run")
    config.addinivalue_line("markers", "cli: CLI-specific tests")
    config.addinivalue_line("markers", "loader: Data loader tests")
    config.addinivalue_line("markers", "rules: Validation rules tests")
    config.addinivalue_line("markers", "config: Configuration tests")
