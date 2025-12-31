"""Tests for result models and aggregation."""

import pytest

from datacheck.results import FailureDetail, RuleResult, ValidationSummary


class TestFailureDetail:
    """Tests for FailureDetail class."""

    def test_valid_failure_detail(self) -> None:
        """Test creating a valid failure detail."""
        detail = FailureDetail(
            rule_name="test_rule",
            column="test_column",
            failed_count=10,
            total_count=100,
            failure_rate=10.0,
            sample_failures=[1, 5, 10, 25, 50],
        )
        assert detail.rule_name == "test_rule"
        assert detail.column == "test_column"
        assert detail.failed_count == 10
        assert detail.total_count == 100
        assert detail.failure_rate == 10.0
        assert detail.sample_failures == [1, 5, 10, 25, 50]

    def test_negative_failed_count(self) -> None:
        """Test that negative failed count raises error."""
        with pytest.raises(ValueError, match="failed_count cannot be negative"):
            FailureDetail(
                rule_name="test",
                column="col",
                failed_count=-1,
                total_count=100,
                failure_rate=0.0,
            )

    def test_zero_total_count(self) -> None:
        """Test that zero total count raises error."""
        with pytest.raises(ValueError, match="total_count must be positive"):
            FailureDetail(
                rule_name="test",
                column="col",
                failed_count=0,
                total_count=0,
                failure_rate=0.0,
            )

    def test_failed_count_exceeds_total(self) -> None:
        """Test that failed count exceeding total raises error."""
        with pytest.raises(ValueError, match="failed_count cannot exceed total_count"):
            FailureDetail(
                rule_name="test",
                column="col",
                failed_count=150,
                total_count=100,
                failure_rate=150.0,
            )

    def test_to_dict(self) -> None:
        """Test converting failure detail to dictionary."""
        detail = FailureDetail(
            rule_name="age_check",
            column="age",
            failed_count=5,
            total_count=100,
            failure_rate=5.0,
            sample_failures=[1, 2, 3],
        )
        result = detail.to_dict()
        assert result == {
            "rule_name": "age_check",
            "column": "age",
            "failed_count": 5,
            "total_count": 100,
            "failure_rate": 5.0,
            "sample_failures": [1, 2, 3],
        }

    def test_to_dict_rounds_failure_rate(self) -> None:
        """Test that failure rate is rounded in dictionary."""
        detail = FailureDetail(
            rule_name="test",
            column="col",
            failed_count=1,
            total_count=3,
            failure_rate=33.333333,
        )
        result = detail.to_dict()
        assert result["failure_rate"] == 33.33


class TestRuleResult:
    """Tests for RuleResult class."""

    def test_passed_result(self) -> None:
        """Test creating a passed rule result."""
        result = RuleResult(
            rule_name="age_check",
            column="age",
            passed=True,
            total_rows=100,
            failed_rows=0,
        )
        assert result.rule_name == "age_check"
        assert result.column == "age"
        assert result.passed is True
        assert result.total_rows == 100
        assert result.failed_rows == 0
        assert result.success_rate == 100.0
        assert result.has_error is False

    def test_failed_result(self) -> None:
        """Test creating a failed rule result."""
        detail = FailureDetail(
            rule_name="age_check",
            column="age",
            failed_count=10,
            total_count=100,
            failure_rate=10.0,
        )
        result = RuleResult(
            rule_name="age_check",
            column="age",
            passed=False,
            total_rows=100,
            failed_rows=10,
            failure_details=detail,
        )
        assert result.passed is False
        assert result.failed_rows == 10
        assert result.success_rate == 90.0
        assert result.failure_details is not None

    def test_result_with_error(self) -> None:
        """Test creating a result with error."""
        result = RuleResult(
            rule_name="age_check",
            column="age",
            passed=False,
            total_rows=100,
            error="Column not found",
        )
        assert result.has_error is True
        assert result.error == "Column not found"

    def test_success_rate_zero_rows(self) -> None:
        """Test success rate with zero rows."""
        result = RuleResult(
            rule_name="test",
            column="col",
            passed=True,
            total_rows=0,
        )
        assert result.success_rate == 0.0

    def test_success_rate_calculation(self) -> None:
        """Test success rate calculation."""
        result = RuleResult(
            rule_name="test",
            column="col",
            passed=False,
            total_rows=100,
            failed_rows=25,
        )
        assert result.success_rate == 75.0

    def test_to_dict_passed(self) -> None:
        """Test converting passed result to dictionary."""
        result = RuleResult(
            rule_name="age_check",
            column="age",
            passed=True,
            total_rows=100,
            failed_rows=0,
        )
        data = result.to_dict()
        assert data == {
            "rule_name": "age_check",
            "column": "age",
            "passed": True,
            "total_rows": 100,
            "failed_rows": 0,
            "success_rate": 100.0,
        }

    def test_to_dict_with_failure_details(self) -> None:
        """Test converting result with failure details to dictionary."""
        detail = FailureDetail(
            rule_name="age_check",
            column="age",
            failed_count=10,
            total_count=100,
            failure_rate=10.0,
            sample_failures=[1, 2, 3],
        )
        result = RuleResult(
            rule_name="age_check",
            column="age",
            passed=False,
            total_rows=100,
            failed_rows=10,
            failure_details=detail,
        )
        data = result.to_dict()
        assert "failure_details" in data
        assert data["failure_details"]["failed_count"] == 10

    def test_to_dict_with_error(self) -> None:
        """Test converting result with error to dictionary."""
        result = RuleResult(
            rule_name="age_check",
            column="age",
            passed=False,
            total_rows=100,
            error="Test error",
        )
        data = result.to_dict()
        assert "error" in data
        assert data["error"] == "Test error"


class TestValidationSummary:
    """Tests for ValidationSummary class."""

    def test_empty_summary(self) -> None:
        """Test creating an empty validation summary."""
        summary = ValidationSummary(results=[])
        assert summary.total_rules == 0
        assert summary.passed_rules == 0
        assert summary.failed_rules == 0
        assert summary.error_rules == 0
        assert summary.all_passed is True

    def test_all_passed(self) -> None:
        """Test summary with all rules passed."""
        results = [
            RuleResult("rule1", "col1", True, 100, 0),
            RuleResult("rule2", "col2", True, 100, 0),
            RuleResult("rule3", "col3", True, 100, 0),
        ]
        summary = ValidationSummary(results=results)
        assert summary.total_rules == 3
        assert summary.passed_rules == 3
        assert summary.failed_rules == 0
        assert summary.error_rules == 0
        assert summary.all_passed is True
        assert summary.has_failures is False
        assert summary.has_errors is False

    def test_some_failed(self) -> None:
        """Test summary with some failed rules."""
        results = [
            RuleResult("rule1", "col1", True, 100, 0),
            RuleResult("rule2", "col2", False, 100, 10),
            RuleResult("rule3", "col3", False, 100, 5),
        ]
        summary = ValidationSummary(results=results)
        assert summary.total_rules == 3
        assert summary.passed_rules == 1
        assert summary.failed_rules == 2
        assert summary.error_rules == 0
        assert summary.all_passed is False
        assert summary.has_failures is True
        assert summary.has_errors is False

    def test_with_errors(self) -> None:
        """Test summary with errors."""
        results = [
            RuleResult("rule1", "col1", True, 100, 0),
            RuleResult("rule2", "col2", False, 100, 0, error="Error 1"),
            RuleResult("rule3", "col3", False, 100, 0, error="Error 2"),
        ]
        summary = ValidationSummary(results=results)
        assert summary.total_rules == 3
        assert summary.passed_rules == 1
        assert summary.failed_rules == 0
        assert summary.error_rules == 2
        assert summary.all_passed is False
        assert summary.has_failures is False
        assert summary.has_errors is True

    def test_mixed_results(self) -> None:
        """Test summary with mixed results."""
        results = [
            RuleResult("rule1", "col1", True, 100, 0),
            RuleResult("rule2", "col2", False, 100, 10),
            RuleResult("rule3", "col3", False, 100, 0, error="Error"),
        ]
        summary = ValidationSummary(results=results)
        assert summary.total_rules == 3
        assert summary.passed_rules == 1
        assert summary.failed_rules == 1
        assert summary.error_rules == 1
        assert summary.all_passed is False
        assert summary.has_failures is True
        assert summary.has_errors is True

    def test_get_failed_results(self) -> None:
        """Test getting failed results."""
        results = [
            RuleResult("rule1", "col1", True, 100, 0),
            RuleResult("rule2", "col2", False, 100, 10),
            RuleResult("rule3", "col3", False, 100, 5),
            RuleResult("rule4", "col4", False, 100, 0, error="Error"),
        ]
        summary = ValidationSummary(results=results)
        failed = summary.get_failed_results()
        assert len(failed) == 2
        assert all(not r.passed and not r.has_error for r in failed)

    def test_get_error_results(self) -> None:
        """Test getting error results."""
        results = [
            RuleResult("rule1", "col1", True, 100, 0),
            RuleResult("rule2", "col2", False, 100, 10),
            RuleResult("rule3", "col3", False, 100, 0, error="Error 1"),
            RuleResult("rule4", "col4", False, 100, 0, error="Error 2"),
        ]
        summary = ValidationSummary(results=results)
        errors = summary.get_error_results()
        assert len(errors) == 2
        assert all(r.has_error for r in errors)

    def test_get_passed_results(self) -> None:
        """Test getting passed results."""
        results = [
            RuleResult("rule1", "col1", True, 100, 0),
            RuleResult("rule2", "col2", True, 100, 0),
            RuleResult("rule3", "col3", False, 100, 10),
        ]
        summary = ValidationSummary(results=results)
        passed = summary.get_passed_results()
        assert len(passed) == 2
        assert all(r.passed and not r.has_error for r in passed)

    def test_to_dict(self) -> None:
        """Test converting summary to dictionary."""
        results = [
            RuleResult("rule1", "col1", True, 100, 0),
            RuleResult("rule2", "col2", False, 100, 10),
        ]
        summary = ValidationSummary(results=results)
        data = summary.to_dict()
        assert data["total_rules"] == 2
        assert data["passed_rules"] == 1
        assert data["failed_rules"] == 1
        assert data["error_rules"] == 0
        assert data["all_passed"] is False
        assert len(data["results"]) == 2
        assert isinstance(data["results"][0], dict)
