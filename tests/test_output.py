"""Tests for output formatting and display."""

import json
from io import StringIO
from pathlib import Path

from rich.console import Console

from datacheck.output import JSONExporter, OutputFormatter
from datacheck.results import FailureDetail, RuleResult, ValidationSummary


class TestOutputFormatter:
    """Tests for OutputFormatter class."""

    def test_init_with_default_console(self) -> None:
        """Test initialization with default console."""
        formatter = OutputFormatter()
        assert formatter.console is not None
        assert isinstance(formatter.console, Console)

    def test_init_with_custom_console(self) -> None:
        """Test initialization with custom console."""
        custom_console = Console()
        formatter = OutputFormatter(console=custom_console)
        assert formatter.console is custom_console

    def test_print_summary_all_passed(self) -> None:
        """Test printing summary when all rules passed."""
        # Create passing results
        results = [
            RuleResult(
                rule_name="test_rule_1",
                column="col1",
                passed=True,
                total_rows=100,
            ),
            RuleResult(
                rule_name="test_rule_2",
                column="col2",
                passed=True,
                total_rows=100,
            ),
        ]
        summary = ValidationSummary(results=results)

        # Capture output
        output = StringIO()
        console = Console(file=output, force_terminal=True, width=120)
        formatter = OutputFormatter(console=console)

        formatter.print_summary(summary)

        # Verify output contains success message
        output_text = output.getvalue()
        assert "ALL CHECKS PASSED" in output_text
        assert "Total Rules" in output_text
        assert "Passed" in output_text

    def test_print_summary_with_failures(self) -> None:
        """Test printing summary with failed rules."""
        # Create failed result
        failure_detail = FailureDetail(
            rule_name="failed_rule",
            column="col1",
            failed_count=2,
            total_count=100,
            failure_rate=2.0,
            sample_failures=[0, 5],
        )
        results = [
            RuleResult(
                rule_name="failed_rule",
                column="col1",
                passed=False,
                total_rows=100,
                failed_rows=2,
                failure_details=failure_detail,
            ),
        ]
        summary = ValidationSummary(results=results)

        # Capture output
        output = StringIO()
        console = Console(file=output, force_terminal=True, width=120)
        formatter = OutputFormatter(console=console)

        formatter.print_summary(summary)

        # Verify output contains failure information
        output_text = output.getvalue()
        assert "VALIDATION FAILED" in output_text
        assert "Failed Rules:" in output_text
        assert "failed_rule" in output_text
        assert "col1" in output_text

    def test_print_summary_with_errors(self) -> None:
        """Test printing summary with error rules."""
        results = [
            RuleResult(
                rule_name="error_rule",
                column="col1",
                passed=False,
                total_rows=100,
                error="Column not found",
            ),
        ]
        summary = ValidationSummary(results=results)

        # Capture output
        output = StringIO()
        console = Console(file=output, force_terminal=True, width=120)
        formatter = OutputFormatter(console=console)

        formatter.print_summary(summary)

        # Verify output contains error information
        output_text = output.getvalue()
        assert "VALIDATION ERRORS" in output_text
        assert "Rules with Errors:" in output_text
        assert "error_rule" in output_text
        assert "Column not found" in output_text

    def test_print_summary_with_mixed_results(self) -> None:
        """Test printing summary with mixed passed/failed/error results."""
        failure_detail = FailureDetail(
            rule_name="failed_rule",
            column="col2",
            failed_count=5,
            total_count=100,
            failure_rate=5.0,
            sample_failures=[0, 1, 2, 3, 4],
        )

        results = [
            RuleResult(
                rule_name="passed_rule",
                column="col1",
                passed=True,
                total_rows=100,
            ),
            RuleResult(
                rule_name="failed_rule",
                column="col2",
                passed=False,
                total_rows=100,
                failed_rows=5,
                failure_details=failure_detail,
            ),
            RuleResult(
                rule_name="error_rule",
                column="col3",
                passed=False,
                total_rows=100,
                error="Some error",
            ),
        ]
        summary = ValidationSummary(results=results)

        # Capture output
        output = StringIO()
        console = Console(file=output, force_terminal=True, width=120)
        formatter = OutputFormatter(console=console)

        formatter.print_summary(summary)

        # Verify output contains all sections
        output_text = output.getvalue()
        assert "Failed Rules:" in output_text
        assert "Rules with Errors:" in output_text
        assert "failed_rule" in output_text
        assert "error_rule" in output_text

    def test_print_rule_result_passed(self) -> None:
        """Test printing a passed rule result."""
        result = RuleResult(
            rule_name="test_rule",
            column="col1",
            passed=True,
            total_rows=100,
        )

        # Capture output
        output = StringIO()
        console = Console(file=output, force_terminal=True, width=120)
        formatter = OutputFormatter(console=console)

        formatter.print_rule_result(result)

        # Verify output
        output_text = output.getvalue()
        assert "PASS" in output_text
        assert "test_rule" in output_text
        assert "col1" in output_text

    def test_print_rule_result_failed(self) -> None:
        """Test printing a failed rule result."""
        result = RuleResult(
            rule_name="test_rule",
            column="col1",
            passed=False,
            total_rows=100,
            failed_rows=10,
        )

        # Capture output
        output = StringIO()
        console = Console(file=output, force_terminal=True, width=120)
        formatter = OutputFormatter(console=console)

        formatter.print_rule_result(result)

        # Verify output
        output_text = output.getvalue()
        assert "FAIL" in output_text
        assert "test_rule" in output_text
        assert "10" in output_text
        assert "100" in output_text

    def test_print_rule_result_error(self) -> None:
        """Test printing a rule result with error."""
        result = RuleResult(
            rule_name="test_rule",
            column="col1",
            passed=False,
            total_rows=100,
            error="Test error message",
        )

        # Capture output
        output = StringIO()
        console = Console(file=output, force_terminal=True, width=120)
        formatter = OutputFormatter(console=console)

        formatter.print_rule_result(result)

        # Verify output
        output_text = output.getvalue()
        assert "ERROR" in output_text
        assert "test_rule" in output_text
        assert "Test error message" in output_text

    def test_print_failure_details_with_samples(self) -> None:
        """Test printing failure details with sample row indices."""
        # Create failure detail with 15 samples (should only show 10)
        sample_failures = list(range(15))

        failure_detail = FailureDetail(
            rule_name="test_rule",
            column="col1",
            failed_count=15,
            total_count=100,
            failure_rate=15.0,
            sample_failures=sample_failures,
        )

        result = RuleResult(
            rule_name="test_rule",
            column="col1",
            passed=False,
            total_rows=100,
            failed_rows=15,
            failure_details=failure_detail,
        )

        # Capture output
        output = StringIO()
        console = Console(file=output, force_terminal=True, width=120)
        formatter = OutputFormatter(console=console)

        # Use internal method to print rule result
        formatter._print_rule_result(result)

        # Verify output
        output_text = output.getvalue()
        assert "Sample failure row indices:" in output_text
        assert "0" in output_text  # First row index
        # Should show message about additional samples (check for key parts separately due to Rich formatting)
        assert " and " in output_text
        assert "5" in output_text
        assert "more samples" in output_text
        assert "showing" in output_text
        assert "10" in output_text
        assert "15" in output_text

    def test_print_statistics(self) -> None:
        """Test printing statistics table."""
        results = [
            RuleResult(rule_name="rule1", column="col1", passed=True, total_rows=100),
            RuleResult(rule_name="rule2", column="col2", passed=False, total_rows=100, failed_rows=5),
            RuleResult(rule_name="rule3", column="col3", passed=False, total_rows=100, error="Error"),
        ]
        summary = ValidationSummary(results=results)

        # Capture output
        output = StringIO()
        console = Console(file=output, force_terminal=True, width=120)
        formatter = OutputFormatter(console=console)

        formatter._print_statistics(summary)

        # Verify output contains statistics
        output_text = output.getvalue()
        assert "Total Rules" in output_text
        assert "3" in output_text
        assert "Passed" in output_text
        assert "1" in output_text
        assert "Failed" in output_text
        assert "Errors" in output_text


class TestJSONExporter:
    """Tests for JSONExporter class."""

    def test_export_summary_to_string(self) -> None:
        """Test exporting summary to JSON string."""
        results = [
            RuleResult(
                rule_name="test_rule",
                column="col1",
                passed=True,
                total_rows=100,
            ),
        ]
        summary = ValidationSummary(results=results)

        json_str = JSONExporter.export_summary(summary)

        # Verify JSON is valid
        data = json.loads(json_str)
        assert data["total_rules"] == 1
        assert data["passed_rules"] == 1
        assert data["all_passed"] is True

    def test_export_summary_pretty_format(self) -> None:
        """Test exporting summary with pretty formatting."""
        results = [
            RuleResult(
                rule_name="test_rule",
                column="col1",
                passed=True,
                total_rows=100,
            ),
        ]
        summary = ValidationSummary(results=results)

        json_str = JSONExporter.export_summary(summary, pretty=True)

        # Pretty format should have indentation
        assert "\n" in json_str
        assert "  " in json_str

    def test_export_summary_compact_format(self) -> None:
        """Test exporting summary with compact formatting."""
        results = [
            RuleResult(
                rule_name="test_rule",
                column="col1",
                passed=True,
                total_rows=100,
            ),
        ]
        summary = ValidationSummary(results=results)

        json_str = JSONExporter.export_summary(summary, pretty=False)

        # Compact format should not have extra indentation
        # (might have single spaces, but not 2+ space indentation)
        lines = json_str.split("\n")
        assert all(not line.startswith("  ") for line in lines)

    def test_export_summary_to_file(self, tmp_path: Path) -> None:
        """Test exporting summary to JSON file."""
        results = [
            RuleResult(
                rule_name="test_rule",
                column="col1",
                passed=True,
                total_rows=100,
            ),
        ]
        summary = ValidationSummary(results=results)

        output_file = tmp_path / "output.json"
        json_str = JSONExporter.export_summary(summary, output_path=output_file)

        # Verify file was created
        assert output_file.exists()

        # Verify file contents match returned string
        file_contents = output_file.read_text(encoding="utf-8")
        assert file_contents == json_str

        # Verify JSON is valid
        data = json.loads(file_contents)
        assert data["total_rules"] == 1

    def test_export_summary_with_failures(self, tmp_path: Path) -> None:
        """Test exporting summary with failure details."""
        failure_detail = FailureDetail(
            rule_name="failed_rule",
            column="col1",
            failed_count=5,
            total_count=100,
            failure_rate=5.0,
            sample_failures=[0, 1, 2, 3, 4],
        )

        results = [
            RuleResult(
                rule_name="failed_rule",
                column="col1",
                passed=False,
                total_rows=100,
                failed_rows=5,
                failure_details=failure_detail,
            ),
        ]
        summary = ValidationSummary(results=results)

        output_file = tmp_path / "failures.json"
        JSONExporter.export_summary(summary, output_path=output_file)

        # Load and verify
        data = json.loads(output_file.read_text(encoding="utf-8"))
        assert data["all_passed"] is False
        assert data["failed_rules"] == 1
        assert len(data["results"]) == 1
        assert data["results"][0]["failed_rows"] == 5

    def test_export_result_to_string(self) -> None:
        """Test exporting single result to JSON string."""
        result = RuleResult(
            rule_name="test_rule",
            column="col1",
            passed=True,
            total_rows=100,
        )

        json_str = JSONExporter.export_result(result)

        # Verify JSON is valid
        data = json.loads(json_str)
        assert data["rule_name"] == "test_rule"
        assert data["column"] == "col1"
        assert data["passed"] is True

    def test_export_result_to_file(self, tmp_path: Path) -> None:
        """Test exporting single result to JSON file."""
        result = RuleResult(
            rule_name="test_rule",
            column="col1",
            passed=True,
            total_rows=100,
        )

        output_file = tmp_path / "result.json"
        json_str = JSONExporter.export_result(result, output_path=output_file)

        # Verify file was created
        assert output_file.exists()

        # Verify contents
        file_contents = output_file.read_text(encoding="utf-8")
        assert file_contents == json_str

    def test_export_result_with_error(self) -> None:
        """Test exporting result with error."""
        result = RuleResult(
            rule_name="error_rule",
            column="col1",
            passed=False,
            total_rows=100,
            error="Test error",
        )

        json_str = JSONExporter.export_result(result)

        # Verify JSON contains error
        data = json.loads(json_str)
        assert data["error"] == "Test error"
        assert data["passed"] is False

    def test_load_summary_from_file(self, tmp_path: Path) -> None:
        """Test loading summary from JSON file."""
        results = [
            RuleResult(
                rule_name="test_rule",
                column="col1",
                passed=True,
                total_rows=100,
            ),
        ]
        summary = ValidationSummary(results=results)

        # Export to file
        output_file = tmp_path / "summary.json"
        JSONExporter.export_summary(summary, output_path=output_file)

        # Load from file
        loaded_data = JSONExporter.load_summary(output_file)

        # Verify loaded data
        assert loaded_data["total_rules"] == 1
        assert loaded_data["passed_rules"] == 1
        assert loaded_data["all_passed"] is True

    def test_export_result_pretty_vs_compact(self) -> None:
        """Test difference between pretty and compact export."""
        result = RuleResult(
            rule_name="test_rule",
            column="col1",
            passed=True,
            total_rows=100,
        )

        pretty_json = JSONExporter.export_result(result, pretty=True)
        compact_json = JSONExporter.export_result(result, pretty=False)

        # Pretty should be longer due to formatting
        assert len(pretty_json) > len(compact_json)

        # Both should be valid JSON with same data
        pretty_data = json.loads(pretty_json)
        compact_data = json.loads(compact_json)
        assert pretty_data == compact_data


class TestOutputIntegration:
    """Integration tests for output module."""

    def test_end_to_end_output_workflow(self, tmp_path: Path) -> None:
        """Test complete output workflow from validation to display."""
        # Create failure detail
        failure_detail = FailureDetail(
            rule_name="range_check",
            column="age",
            failed_count=3,
            total_count=100,
            failure_rate=3.0,
            sample_failures=[10, 20, 30],
        )

        # Create results
        results = [
            RuleResult(
                rule_name="not_null_check",
                column="age",
                passed=True,
                total_rows=100,
            ),
            RuleResult(
                rule_name="range_check",
                column="age",
                passed=False,
                total_rows=100,
                failed_rows=3,
                failure_details=failure_detail,
            ),
            RuleResult(
                rule_name="format_check",
                column="email",
                passed=False,
                total_rows=100,
                error="Invalid regex pattern",
            ),
        ]

        summary = ValidationSummary(results=results)

        # Test terminal output
        output = StringIO()
        console = Console(file=output, force_terminal=True, width=120)
        formatter = OutputFormatter(console=console)
        formatter.print_summary(summary)

        terminal_output = output.getvalue()
        # Passed rules are not shown in detail output, only failed and error rules
        assert "range_check" in terminal_output
        assert "format_check" in terminal_output
        assert "Failed Rules:" in terminal_output
        assert "Rules with Errors:" in terminal_output

        # Test JSON export
        json_file = tmp_path / "results.json"
        JSONExporter.export_summary(summary, output_path=json_file)

        # Verify JSON file
        assert json_file.exists()
        loaded_data = JSONExporter.load_summary(json_file)
        assert loaded_data["total_rules"] == 3
        assert loaded_data["passed_rules"] == 1
        assert loaded_data["failed_rules"] == 1
        assert loaded_data["error_rules"] == 1
