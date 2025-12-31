# DataCheck Test Suite

Comprehensive test suite for the DataCheck data quality validation tool.

## Test Structure

```
tests/
├── conftest.py          # Shared fixtures and pytest configuration
├── helpers.py           # Test utilities and data generators
├── test_cli.py          # CLI interface tests
├── test_config.py       # Configuration parsing tests
├── test_engine.py       # Validation engine tests
├── test_loader.py       # Data loader tests
├── test_output.py       # Output formatting tests
├── test_results.py      # Results model tests
└── test_rules.py        # Validation rules tests
```

## Running Tests

### Run all tests
```bash
poetry run pytest
```

### Run with coverage report
```bash
poetry run pytest --cov=datacheck --cov-report=html
```

### Run specific test categories
```bash
# Unit tests only
poetry run pytest -m unit

# Integration tests only
poetry run pytest -m integration

# CLI tests only
poetry run pytest -m cli

# Exclude slow tests
poetry run pytest -m "not slow"
```

### Run specific test files
```bash
poetry run pytest tests/test_cli.py
poetry run pytest tests/test_rules.py -v
```

### Run with specific verbosity
```bash
# Quiet mode
poetry run pytest -q

# Verbose mode
poetry run pytest -v

# Very verbose mode
poetry run pytest -vv
```

## Test Markers

Tests are categorized using pytest markers:

- `@pytest.mark.unit` - Unit tests that don't require external dependencies
- `@pytest.mark.integration` - Integration tests testing multiple components
- `@pytest.mark.slow` - Tests that take longer to run
- `@pytest.mark.cli` - CLI-specific tests
- `@pytest.mark.loader` - Data loader tests
- `@pytest.mark.rules` - Validation rules tests
- `@pytest.mark.config` - Configuration tests
- `@pytest.mark.engine` - Validation engine tests
- `@pytest.mark.output` - Output formatting tests

## Shared Fixtures

The `conftest.py` file provides shared fixtures:

### File Fixtures
- `sample_csv_path` - Sample CSV file
- `sample_parquet_path` - Sample Parquet file
- `sample_config_path` - Sample validation config
- `empty_csv_path` - Empty CSV file (header only)
- `invalid_csv_path` - Invalid CSV file

### DataFrame Fixtures
- `sample_dataframe` - Standard test DataFrame
- `dataframe_with_nulls` - DataFrame with null values
- `dataframe_with_violations` - DataFrame with validation violations

## Test Helpers

The `helpers.py` module provides utilities:

### DataFrameFactory
```python
from tests.helpers import DataFrameFactory

# Create simple DataFrame
df = DataFrameFactory.create_simple(rows=10)

# Create DataFrame with nulls
df = DataFrameFactory.create_with_nulls(null_percentage=0.3)

# Create DataFrame with outliers
df = DataFrameFactory.create_with_outliers()

# Create large DataFrame for performance testing
df = DataFrameFactory.create_large(rows=10000)
```

### ConfigFactory
```python
from tests.helpers import ConfigFactory

# Create simple config
config = ConfigFactory.create_simple()

# Create complex config
config = ConfigFactory.create_complex()

# Create config with all rule types
config = ConfigFactory.create_with_all_rules()
```

### FileFactory
```python
from tests.helpers import FileFactory

# Create test files
csv_path = FileFactory.create_csv(path, df)
parquet_path = FileFactory.create_parquet(path, df)
config_path = FileFactory.create_config_yaml(path, config)
```

### Assertion Helpers
```python
from tests.helpers import (
    assert_validation_passed,
    assert_validation_failed,
    assert_has_error
)

# Assert validation passed
assert_validation_passed(result)

# Assert validation failed with expected count
assert_validation_failed(result, expected_failures=2)

# Assert result has error
assert_has_error(result, error_msg="Column not found")
```

## Coverage Requirements

- Minimum coverage: 70% (enforced by `--cov-fail-under=70`)
- Branch coverage enabled
- Coverage reports generated in HTML and JSON formats

## Best Practices

1. **Use Fixtures**: Leverage shared fixtures from `conftest.py` instead of creating data in tests
2. **Use Factories**: Use `DataFrameFactory`, `ConfigFactory`, and `FileFactory` for test data
3. **Mark Tests**: Add appropriate markers to categorize tests
4. **Descriptive Names**: Use clear, descriptive test function names
5. **Arrange-Act-Assert**: Follow AAA pattern in test structure
6. **One Assertion**: Prefer one logical assertion per test (can have multiple assert statements for same concept)
7. **Cleanup**: Use fixtures with proper cleanup (tmp_path handles this automatically)
8. **Parametrize**: Use `@pytest.mark.parametrize` for testing multiple inputs

## Example Test

```python
import pytest
from tests.helpers import DataFrameFactory, assert_validation_passed


@pytest.mark.unit
@pytest.mark.rules
class TestMinRule:
    """Tests for min value validation rule."""

    def test_min_rule_passes_with_valid_values(self, sample_dataframe):
        """Test that min rule passes when all values are above minimum."""
        # Arrange
        df = sample_dataframe
        rule = MinRule(column="age", threshold=0)

        # Act
        result = rule.validate(df)

        # Assert
        assert_validation_passed(result)

    @pytest.mark.parametrize("min_value,expected_failures", [
        (30, 2),  # 2 values below 30
        (35, 3),  # 3 values below 35
    ])
    def test_min_rule_fails_with_low_values(self, sample_dataframe, min_value, expected_failures):
        """Test that min rule fails when values are below minimum."""
        # Arrange
        rule = MinRule(column="age", threshold=min_value)

        # Act
        result = rule.validate(sample_dataframe)

        # Assert
        assert_validation_failed(result, expected_failures=expected_failures)
```

## Continuous Integration

Tests are run automatically on:
- Every commit
- Every pull request
- Scheduled nightly builds

CI enforces:
- All tests must pass
- Minimum 70% code coverage
- No linting errors
- Type checking passes
