"""Result models and aggregation."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class FailureDetail:
    """Details about validation failures for a specific rule.

    Attributes:
        rule_name: Name of the rule that failed
        column: Column that was validated
        failed_count: Number of rows that failed validation
        total_count: Total number of rows checked
        failure_rate: Percentage of rows that failed (0-100)
        sample_failures: Sample of failed row indices (limited to 100)
    """

    rule_name: str
    column: str
    failed_count: int
    total_count: int
    failure_rate: float
    sample_failures: list[int] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate failure detail after initialization."""
        if self.failed_count < 0:
            raise ValueError("failed_count cannot be negative")
        if self.total_count <= 0:
            raise ValueError("total_count must be positive")
        if self.failed_count > self.total_count:
            raise ValueError("failed_count cannot exceed total_count")

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization.

        Returns:
            Dictionary representation of failure details
        """
        return {
            "rule_name": self.rule_name,
            "column": self.column,
            "failed_count": self.failed_count,
            "total_count": self.total_count,
            "failure_rate": round(self.failure_rate, 2),
            "sample_failures": self.sample_failures,
        }


@dataclass
class RuleResult:
    """Result of executing a single validation rule.

    Attributes:
        rule_name: Name of the rule that was executed
        column: Column that was validated
        passed: Whether all rows passed validation
        total_rows: Total number of rows in the dataset
        failed_rows: Number of rows that failed validation
        failure_details: Detailed failure information if validation failed
        error: Error message if rule execution failed
    """

    rule_name: str
    column: str
    passed: bool
    total_rows: int
    failed_rows: int = 0
    failure_details: FailureDetail | None = None
    error: str | None = None

    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage.

        Returns:
            Success rate (0-100)
        """
        if self.total_rows == 0:
            return 0.0
        return ((self.total_rows - self.failed_rows) / self.total_rows) * 100

    @property
    def has_error(self) -> bool:
        """Check if rule execution encountered an error.

        Returns:
            True if there was an error, False otherwise
        """
        return self.error is not None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization.

        Returns:
            Dictionary representation of rule result
        """
        result: dict[str, Any] = {
            "rule_name": self.rule_name,
            "column": self.column,
            "passed": self.passed,
            "total_rows": self.total_rows,
            "failed_rows": self.failed_rows,
            "success_rate": round(self.success_rate, 2),
        }

        if self.failure_details:
            result["failure_details"] = self.failure_details.to_dict()

        if self.error:
            result["error"] = self.error

        return result


@dataclass
class ValidationSummary:
    """Summary of all validation results.

    Attributes:
        results: List of individual rule results
        total_rules: Total number of rules executed
        passed_rules: Number of rules that passed
        failed_rules: Number of rules that failed
        error_rules: Number of rules that encountered errors
    """

    results: list[RuleResult]

    @property
    def total_rules(self) -> int:
        """Get total number of rules.

        Returns:
            Total number of rules
        """
        return len(self.results)

    @property
    def passed_rules(self) -> int:
        """Get number of passed rules.

        Returns:
            Number of rules that passed
        """
        return sum(1 for r in self.results if r.passed and not r.has_error)

    @property
    def failed_rules(self) -> int:
        """Get number of failed rules.

        Returns:
            Number of rules that failed validation
        """
        return sum(1 for r in self.results if not r.passed and not r.has_error)

    @property
    def error_rules(self) -> int:
        """Get number of rules with errors.

        Returns:
            Number of rules that encountered errors
        """
        return sum(1 for r in self.results if r.has_error)

    @property
    def all_passed(self) -> bool:
        """Check if all rules passed.

        Returns:
            True if all rules passed, False otherwise
        """
        return self.failed_rules == 0 and self.error_rules == 0

    @property
    def has_failures(self) -> bool:
        """Check if any rules failed.

        Returns:
            True if any rules failed, False otherwise
        """
        return self.failed_rules > 0

    @property
    def has_errors(self) -> bool:
        """Check if any rules had errors.

        Returns:
            True if any rules had errors, False otherwise
        """
        return self.error_rules > 0

    def get_failed_results(self) -> list[RuleResult]:
        """Get all failed rule results.

        Returns:
            List of rule results that failed
        """
        return [r for r in self.results if not r.passed and not r.has_error]

    def get_error_results(self) -> list[RuleResult]:
        """Get all rule results with errors.

        Returns:
            List of rule results that encountered errors
        """
        return [r for r in self.results if r.has_error]

    def get_passed_results(self) -> list[RuleResult]:
        """Get all passed rule results.

        Returns:
            List of rule results that passed
        """
        return [r for r in self.results if r.passed and not r.has_error]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization.

        Returns:
            Dictionary representation of validation summary
        """
        return {
            "total_rules": self.total_rules,
            "passed_rules": self.passed_rules,
            "failed_rules": self.failed_rules,
            "error_rules": self.error_rules,
            "all_passed": self.all_passed,
            "results": [r.to_dict() for r in self.results],
        }


__all__ = [
    "FailureDetail",
    "RuleResult",
    "ValidationSummary",
]
