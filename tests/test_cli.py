"""Tests for CLI interface."""

import json
from pathlib import Path

import pandas as pd
import pytest
from typer.testing import CliRunner

from datacheck.cli import app

runner = CliRunner()


class TestCLIValidateCommand:
    """Tests for the validate command."""

    def test_validate_with_valid_data(self, tmp_path: Path) -> None:
        """Test validate command with valid data."""
        # Create CSV file
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("name,age\nAlice,30\nBob,25\n")

        # Create config file
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
"""
        )

        # Run CLI
        result = runner.invoke(app, ["validate", str(csv_file), "--config", str(config_file)])

        # Verify output
        assert result.exit_code == 0
        assert "ALL CHECKS PASSED" in result.stdout

    def test_validate_with_failures(self, tmp_path: Path) -> None:
        """Test validate command with rule failures."""
        # Create CSV file with violations
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("name,age\nAlice,30\nBob,150\n")

        # Create config file
        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            """
checks:
  - name: age_check
    column: age
    rules:
      max: 120
"""
        )

        # Run CLI
        result = runner.invoke(app, ["validate", str(csv_file), "--config", str(config_file)])

        # Verify output
        assert result.exit_code == 1  # Validation failed
        assert "VALIDATION FAILED" in result.stdout

    def test_validate_with_auto_config_discovery(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test validate command with auto-discovered config."""
        monkeypatch.chdir(tmp_path)

        # Create CSV file
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("name,age\nAlice,30\n")

        # Create .datacheck.yaml in current directory
        config_file = tmp_path / ".datacheck.yaml"
        config_file.write_text(
            """
checks:
  - name: age_check
    column: age
    rules:
      not_null: true
"""
        )

        # Run CLI without --config
        result = runner.invoke(app, ["validate", str(csv_file)])

        # Verify output
        assert result.exit_code == 0
        assert "ALL CHECKS PASSED" in result.stdout

    def test_validate_with_missing_config(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test validate command when config is missing."""
        monkeypatch.chdir(tmp_path)

        # Create CSV file
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("name,age\nAlice,30\n")

        # Run CLI without config
        result = runner.invoke(app, ["validate", str(csv_file)])

        # Verify error
        assert result.exit_code == 2  # Configuration error
        assert "Configuration Error" in result.stdout

    def test_validate_with_nonexistent_file(self, tmp_path: Path) -> None:
        """Test validate command with non-existent data file."""
        # Create config file
        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            """
checks:
  - name: test
    column: col
    rules:
      not_null: true
"""
        )

        # Run CLI with non-existent file
        result = runner.invoke(
            app, ["validate", "nonexistent.csv", "--config", str(config_file)]
        )

        # Verify error
        assert result.exit_code == 3  # Data load error
        assert "Data Load Error" in result.stdout

    def test_validate_json_output_format(self, tmp_path: Path) -> None:
        """Test validate command with JSON output format."""
        # Create CSV file
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("name,age\nAlice,30\n")

        # Create config file
        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            """
checks:
  - name: age_check
    column: age
    rules:
      not_null: true
"""
        )

        # Run CLI with JSON format
        result = runner.invoke(
            app, ["validate", str(csv_file), "--config", str(config_file), "--format", "json"]
        )

        # Verify output
        assert result.exit_code == 0
        # Parse JSON output
        json_data = json.loads(result.stdout)
        assert json_data["all_passed"] is True
        assert json_data["total_rules"] == 1

    def test_validate_json_output_to_file(self, tmp_path: Path) -> None:
        """Test validate command with JSON output to file."""
        # Create CSV file
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("name,age\nAlice,30\n")

        # Create config file
        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            """
checks:
  - name: age_check
    column: age
    rules:
      not_null: true
"""
        )

        # Run CLI with JSON output file
        json_output = tmp_path / "results.json"
        result = runner.invoke(
            app,
            [
                "validate",
                str(csv_file),
                "--config",
                str(config_file),
                "--format",
                "json",
                "--json-output",
                str(json_output),
            ],
        )

        # Verify output file was created
        assert result.exit_code == 0
        assert json_output.exists()

        # Verify JSON content
        json_data = json.loads(json_output.read_text())
        assert json_data["all_passed"] is True

    def test_validate_json_output_without_format(self, tmp_path: Path) -> None:
        """Test that json-output auto-sets format to json."""
        # Create CSV file
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("name,age\nAlice,30\n")

        # Create config file
        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            """
checks:
  - name: age_check
    column: age
    rules:
      not_null: true
"""
        )

        # Run CLI with json-output but without --format json
        json_output = tmp_path / "results.json"
        result = runner.invoke(
            app,
            ["validate", str(csv_file), "--config", str(config_file), "--json-output", str(json_output)],
        )

        # Should show warning and still create JSON file
        assert result.exit_code == 0
        assert "Warning" in result.stdout
        assert json_output.exists()

    def test_validate_invalid_output_format(self, tmp_path: Path) -> None:
        """Test validate command with invalid output format."""
        # Create CSV file
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("name,age\nAlice,30\n")

        # Create config file
        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            """
checks:
  - name: test
    column: age
    rules:
      not_null: true
"""
        )

        # Run CLI with invalid format
        result = runner.invoke(
            app, ["validate", str(csv_file), "--config", str(config_file), "--format", "xml"]
        )

        # Verify error
        assert result.exit_code == 2
        assert "Invalid output format" in result.stdout

    def test_validate_with_column_error(self, tmp_path: Path) -> None:
        """Test validate command when column doesn't exist."""
        # Create CSV file
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("name,age\nAlice,30\n")

        # Create config with non-existent column
        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            """
checks:
  - name: salary_check
    column: salary
    rules:
      not_null: true
"""
        )

        # Run CLI
        result = runner.invoke(app, ["validate", str(csv_file), "--config", str(config_file)])

        # Verify error exit code
        assert result.exit_code == 4  # Validation error
        assert "VALIDATION ERRORS" in result.stdout

    def test_validate_parquet_file(self, tmp_path: Path) -> None:
        """Test validate command with Parquet file."""
        # Create Parquet file
        parquet_file = tmp_path / "data.parquet"
        df = pd.DataFrame({"name": ["Alice", "Bob"], "age": [30, 25]})
        df.to_parquet(parquet_file)

        # Create config file
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

        # Run CLI
        result = runner.invoke(app, ["validate", str(parquet_file), "--config", str(config_file)])

        # Verify output
        assert result.exit_code == 0
        assert "ALL CHECKS PASSED" in result.stdout


class TestCLIVersionCommand:
    """Tests for the version command."""

    def test_version_command(self) -> None:
        """Test version command."""
        result = runner.invoke(app, ["version"])

        assert result.exit_code == 0
        assert "DataCheck v" in result.stdout
        assert "0.1.0" in result.stdout


class TestCLIMainCallback:
    """Tests for the main callback (no command)."""

    def test_no_command(self) -> None:
        """Test running CLI with no command."""
        result = runner.invoke(app, [])

        assert result.exit_code == 0
        assert "DataCheck" in result.stdout
        assert "validate" in result.stdout
        assert "version" in result.stdout


class TestCLIExitCodes:
    """Tests for CLI exit codes."""

    def test_exit_code_0_success(self, tmp_path: Path) -> None:
        """Test exit code 0 when all rules pass."""
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("age\n30\n")

        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            """
checks:
  - name: age_check
    column: age
    rules:
      not_null: true
"""
        )

        result = runner.invoke(app, ["validate", str(csv_file), "--config", str(config_file)])
        assert result.exit_code == 0

    def test_exit_code_1_validation_failed(self, tmp_path: Path) -> None:
        """Test exit code 1 when validation rules fail."""
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("age\n150\n")  # Value exceeds max

        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            """
checks:
  - name: age_check
    column: age
    rules:
      max: 120
"""
        )

        result = runner.invoke(app, ["validate", str(csv_file), "--config", str(config_file)])
        assert result.exit_code == 1

    def test_exit_code_2_configuration_error(self, tmp_path: Path) -> None:
        """Test exit code 2 for configuration errors."""
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("age\n30\n")

        # Missing config file
        result = runner.invoke(
            app, ["validate", str(csv_file), "--config", "nonexistent.yaml"]
        )
        assert result.exit_code == 2

    def test_exit_code_3_data_load_error(self, tmp_path: Path) -> None:
        """Test exit code 3 for data loading errors."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            """
checks:
  - name: test
    column: col
    rules:
      not_null: true
"""
        )

        # Non-existent data file
        result = runner.invoke(
            app, ["validate", "nonexistent.csv", "--config", str(config_file)]
        )
        assert result.exit_code == 3

    def test_exit_code_4_validation_error(self, tmp_path: Path) -> None:
        """Test exit code 4 for validation errors (e.g., missing column)."""
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("name\nAlice\n")

        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            """
checks:
  - name: age_check
    column: age
    rules:
      not_null: true
"""
        )

        result = runner.invoke(app, ["validate", str(csv_file), "--config", str(config_file)])
        assert result.exit_code == 4


class TestCLIIntegration:
    """Integration tests for CLI."""

    def test_end_to_end_cli_workflow(self, tmp_path: Path) -> None:
        """Test complete end-to-end CLI workflow."""
        # Create data file
        csv_file = tmp_path / "users.csv"
        csv_file.write_text("name,age,email\nAlice,30,alice@test.com\nBob,25,bob@test.com\n")

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
"""
        )

        # Run validation with terminal output
        result = runner.invoke(app, ["validate", str(csv_file), "--config", str(config_file)])

        assert result.exit_code == 0
        assert "ALL CHECKS PASSED" in result.stdout
        assert "Total Rules" in result.stdout

        # Run validation with JSON output
        json_output = tmp_path / "results.json"
        result = runner.invoke(
            app,
            [
                "validate",
                str(csv_file),
                "--config",
                str(config_file),
                "--format",
                "json",
                "--json-output",
                str(json_output),
            ],
        )

        assert result.exit_code == 0
        assert json_output.exists()

        # Verify JSON content
        json_data = json.loads(json_output.read_text())
        assert json_data["all_passed"] is True
        assert json_data["total_rules"] == 5  # age: not_null + min + max (3), email: not_null + regex (2)
