"""Tests for validation engine."""

from pathlib import Path
from typing import Any

import pandas as pd
import pytest

from datacheck.config import RuleConfig, ValidationConfig
from datacheck.engine import ValidationEngine
from datacheck.exceptions import ConfigurationError, DataLoadError, ValidationError


class TestValidationEngineInit:
    """Tests for ValidationEngine initialization."""

    def test_init_with_config(self) -> None:
        """Test initialization with a ValidationConfig object."""
        config = ValidationConfig(
            checks=[RuleConfig(name="test", column="col1", rules={"not_null": True})]
        )
        engine = ValidationEngine(config=config)
        assert engine.config == config

    def test_init_with_config_path(self, tmp_path: Path) -> None:
        """Test initialization with a config file path."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            """
checks:
  - name: age_check
    column: age
    rules:
      not_null: true
      min: 0
"""
        )

        engine = ValidationEngine(config_path=config_file)
        assert len(engine.config.checks) == 1
        assert engine.config.checks[0].name == "age_check"

    def test_init_with_both_config_and_path(self, tmp_path: Path) -> None:
        """Test that providing both config and config_path raises error."""
        config = ValidationConfig(
            checks=[RuleConfig(name="test", column="col1", rules={"not_null": True})]
        )
        config_file = tmp_path / "config.yaml"
        config_file.write_text("checks:\n  - name: test\n    column: col1\n    rules:\n      not_null: true")

        with pytest.raises(ConfigurationError, match="Cannot provide both"):
            ValidationEngine(config=config, config_path=config_file)

    def test_init_with_auto_discovery(self, tmp_path: Path, monkeypatch: Any) -> None:
        """Test auto-discovery of config file."""
        monkeypatch.chdir(tmp_path)
        config_file = tmp_path / ".datacheck.yaml"
        config_file.write_text(
            """
checks:
  - name: test
    column: col1
    rules:
      not_null: true
"""
        )

        engine = ValidationEngine()
        assert len(engine.config.checks) == 1

    def test_init_no_config_no_discovery(self, tmp_path: Path, monkeypatch: Any) -> None:
        """Test error when no config provided and none found."""
        monkeypatch.chdir(tmp_path)

        with pytest.raises(ConfigurationError, match="No configuration provided"):
            ValidationEngine()


class TestValidationEngineValidateFile:
    """Tests for validate_file method."""

    def test_validate_csv_file(self, tmp_path: Path) -> None:
        """Test validating a CSV file."""
        # Create CSV file
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("name,age\nAlice,30\nBob,25\nCharlie,35\n")

        # Create config
        config = ValidationConfig(
            checks=[
                RuleConfig(name="age_check", column="age", rules={"not_null": True, "min": 0, "max": 120})
            ]
        )

        engine = ValidationEngine(config=config)
        summary = engine.validate_file(csv_file)

        assert summary.total_rules == 3  # not_null + min + max
        assert summary.all_passed is True

    def test_validate_csv_with_failures(self, tmp_path: Path) -> None:
        """Test validating CSV with rule failures."""
        # Create CSV file with violations
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("name,age\nAlice,30\nBob,\nCharlie,150\n")

        # Create config
        config = ValidationConfig(
            checks=[
                RuleConfig(name="age_check", column="age", rules={"not_null": True, "max": 120})
            ]
        )

        engine = ValidationEngine(config=config)
        summary = engine.validate_file(csv_file)

        assert summary.all_passed is False
        assert summary.failed_rules > 0

    def test_validate_file_not_found(self) -> None:
        """Test error when file doesn't exist."""
        config = ValidationConfig(
            checks=[RuleConfig(name="test", column="col1", rules={"not_null": True})]
        )
        engine = ValidationEngine(config=config)

        with pytest.raises(DataLoadError, match="File not found"):
            engine.validate_file("nonexistent.csv")

    def test_validate_parquet_file(self, tmp_path: Path) -> None:
        """Test validating a Parquet file."""
        # Create Parquet file
        parquet_file = tmp_path / "data.parquet"
        df = pd.DataFrame({"name": ["Alice", "Bob"], "age": [30, 25]})
        df.to_parquet(parquet_file)

        # Create config
        config = ValidationConfig(
            checks=[RuleConfig(name="age_check", column="age", rules={"not_null": True})]
        )

        engine = ValidationEngine(config=config)
        summary = engine.validate_file(parquet_file)

        assert summary.total_rules == 1
        assert summary.all_passed is True


class TestValidationEngineValidateDataFrame:
    """Tests for validate_dataframe method."""

    def test_validate_dataframe_all_pass(self) -> None:
        """Test validating DataFrame with all rules passing."""
        df = pd.DataFrame({"name": ["Alice", "Bob", "Charlie"], "age": [30, 25, 35]})

        config = ValidationConfig(
            checks=[
                RuleConfig(name="age_check", column="age", rules={"not_null": True, "min": 0, "max": 120})
            ]
        )

        engine = ValidationEngine(config=config)
        summary = engine.validate_dataframe(df)

        assert summary.total_rules == 3
        assert summary.all_passed is True
        assert summary.passed_rules == 3
        assert summary.failed_rules == 0

    def test_validate_dataframe_with_failures(self) -> None:
        """Test validating DataFrame with rule failures."""
        df = pd.DataFrame({"name": ["Alice", "Bob", "Charlie"], "age": [30, None, 150]})

        config = ValidationConfig(
            checks=[
                RuleConfig(name="age_check", column="age", rules={"not_null": True, "max": 120})
            ]
        )

        engine = ValidationEngine(config=config)
        summary = engine.validate_dataframe(df)

        assert summary.all_passed is False
        assert summary.failed_rules > 0

    def test_validate_multiple_checks(self) -> None:
        """Test validating with multiple check configurations."""
        df = pd.DataFrame({
            "name": ["Alice", "Bob", "Charlie"],
            "age": [30, 25, 35],
            "email": ["alice@test.com", "bob@test.com", "charlie@test.com"],
        })

        config = ValidationConfig(
            checks=[
                RuleConfig(name="age_check", column="age", rules={"not_null": True, "min": 0}),
                RuleConfig(name="name_check", column="name", rules={"not_null": True}),
                RuleConfig(name="email_check", column="email", rules={"regex": r".+@.+\..+"}),
            ]
        )

        engine = ValidationEngine(config=config)
        summary = engine.validate_dataframe(df)

        assert summary.total_rules == 4  # age: not_null + min, name: not_null, email: regex
        assert summary.all_passed is True

    def test_validate_with_column_not_found(self) -> None:
        """Test validation when column doesn't exist."""
        df = pd.DataFrame({"name": ["Alice", "Bob"]})

        config = ValidationConfig(
            checks=[RuleConfig(name="age_check", column="age", rules={"not_null": True})]
        )

        engine = ValidationEngine(config=config)
        summary = engine.validate_dataframe(df)

        # Should have error result for missing column
        assert summary.error_rules == 1
        errors = summary.get_error_results()
        assert len(errors) == 1
        assert "age" in errors[0].error  # type: ignore


class TestValidationEngineValidate:
    """Tests for the generic validate method."""

    def test_validate_with_file_path(self, tmp_path: Path) -> None:
        """Test validate method with file_path."""
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("age\n30\n25\n")

        config = ValidationConfig(
            checks=[RuleConfig(name="age_check", column="age", rules={"min": 0})]
        )

        engine = ValidationEngine(config=config)
        summary = engine.validate(file_path=csv_file)

        assert summary.all_passed is True

    def test_validate_with_dataframe(self) -> None:
        """Test validate method with DataFrame."""
        df = pd.DataFrame({"age": [30, 25, 35]})

        config = ValidationConfig(
            checks=[RuleConfig(name="age_check", column="age", rules={"min": 0})]
        )

        engine = ValidationEngine(config=config)
        summary = engine.validate(df=df)

        assert summary.all_passed is True

    def test_validate_with_both_raises_error(self, tmp_path: Path) -> None:
        """Test that providing both file_path and df raises error."""
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("age\n30\n")
        df = pd.DataFrame({"age": [30]})

        config = ValidationConfig(
            checks=[RuleConfig(name="test", column="age", rules={"min": 0})]
        )

        engine = ValidationEngine(config=config)

        with pytest.raises(ValidationError, match="Cannot provide both"):
            engine.validate(file_path=csv_file, df=df)

    def test_validate_with_neither_raises_error(self) -> None:
        """Test that providing neither file_path nor df raises error."""
        config = ValidationConfig(
            checks=[RuleConfig(name="test", column="age", rules={"min": 0})]
        )

        engine = ValidationEngine(config=config)

        with pytest.raises(ValidationError, match="Must provide either"):
            engine.validate()


class TestValidationEngineIntegration:
    """Integration tests for full validation workflow."""

    def test_end_to_end_csv_validation(self, tmp_path: Path) -> None:
        """Test complete end-to-end validation workflow with CSV."""
        # Create CSV file
        csv_file = tmp_path / "users.csv"
        csv_file.write_text(
            "name,age,email\n"
            "Alice,30,alice@test.com\n"
            "Bob,25,bob@test.com\n"
            "Charlie,35,charlie@test.com\n"
        )

        # Create config file
        config_file = tmp_path / "validation.yaml"
        config_file.write_text(
            """
checks:
  - name: age_validation
    column: age
    rules:
      not_null: true
      min: 18
      max: 120

  - name: email_validation
    column: email
    rules:
      not_null: true
      regex: ".+@.+\\\\..+"

  - name: name_validation
    column: name
    rules:
      not_null: true
"""
        )

        # Run validation
        engine = ValidationEngine(config_path=config_file)
        summary = engine.validate_file(csv_file)

        # Verify results
        assert summary.total_rules == 6  # age: 3, email: 2, name: 1
        assert summary.all_passed is True
        assert summary.passed_rules == 6
        assert summary.failed_rules == 0
        assert summary.error_rules == 0

    def test_end_to_end_with_violations(self, tmp_path: Path) -> None:
        """Test end-to-end validation with rule violations."""
        # Create CSV with violations
        csv_file = tmp_path / "users.csv"
        csv_file.write_text(
            "name,age,email\n"
            "Alice,30,alice@test.com\n"
            "Bob,15,invalid-email\n"  # Age too low, invalid email
            "Charlie,,charlie@test.com\n"  # Missing age
        )

        # Create config
        config_file = tmp_path / "validation.yaml"
        config_file.write_text(
            """
checks:
  - name: age_validation
    column: age
    rules:
      not_null: true
      min: 18

  - name: email_validation
    column: email
    rules:
      regex: ".+@.+\\\\..+"
"""
        )

        # Run validation
        engine = ValidationEngine(config_path=config_file)
        summary = engine.validate_file(csv_file)

        # Verify failures were detected
        assert summary.all_passed is False
        assert summary.failed_rules > 0
        failed = summary.get_failed_results()
        assert len(failed) > 0

    def test_validate_with_loader_kwargs(self, tmp_path: Path) -> None:
        """Test validation with custom loader kwargs."""
        # Create CSV with semicolon delimiter
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("age;name\n30;Alice\n25;Bob\n")

        # Create config
        config = ValidationConfig(
            checks=[RuleConfig(name="age_check", column="age", rules={"min": 0})]
        )

        engine = ValidationEngine(config=config)
        summary = engine.validate_file(csv_file, delimiter=";")

        assert summary.all_passed is True
