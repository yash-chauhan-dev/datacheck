"""Validation rules implementations."""

import re
from abc import ABC, abstractmethod
from typing import Any

import pandas as pd

from datacheck.config import RuleConfig
from datacheck.exceptions import ColumnNotFoundError, RuleDefinitionError
from datacheck.results import FailureDetail, RuleResult


class Rule(ABC):
    """Abstract base class for validation rules.

    Attributes:
        name: Name of the rule
        column: Column to validate
    """

    def __init__(self, name: str, column: str) -> None:
        """Initialize rule.

        Args:
            name: Name of the rule
            column: Column to validate
        """
        self.name = name
        self.column = column

    @abstractmethod
    def validate(self, df: pd.DataFrame) -> RuleResult:
        """Validate data against this rule.

        Args:
            df: DataFrame to validate

        Returns:
            RuleResult with validation outcome

        Raises:
            ColumnNotFoundError: If column not found in DataFrame
        """
        pass

    def _check_column_exists(self, df: pd.DataFrame) -> None:
        """Check if column exists in DataFrame.

        Args:
            df: DataFrame to check

        Raises:
            ColumnNotFoundError: If column not found
        """
        if self.column not in df.columns:
            raise ColumnNotFoundError(self.column, list(df.columns))

    def _create_failure_detail(
        self, failed_indices: pd.Index, total_count: int
    ) -> FailureDetail:
        """Create failure detail from failed indices.

        Args:
            failed_indices: Indices of failed rows
            total_count: Total number of rows

        Returns:
            FailureDetail with failure information
        """
        failed_count = len(failed_indices)
        failure_rate = (failed_count / total_count * 100) if total_count > 0 else 0.0

        # Limit sample failures to 100 for memory efficiency
        sample_failures = failed_indices.tolist()[:100]

        return FailureDetail(
            rule_name=self.name,
            column=self.column,
            failed_count=failed_count,
            total_count=total_count,
            failure_rate=failure_rate,
            sample_failures=sample_failures,
        )


class NotNullRule(Rule):
    """Rule to check for null/missing values."""

    def validate(self, df: pd.DataFrame) -> RuleResult:
        """Validate that column has no null values.

        Args:
            df: DataFrame to validate

        Returns:
            RuleResult with validation outcome
        """
        try:
            self._check_column_exists(df)

            total_rows = len(df)
            null_mask = df[self.column].isna()
            null_indices = df.index[null_mask]

            if len(null_indices) == 0:
                return RuleResult(
                    rule_name=self.name,
                    column=self.column,
                    passed=True,
                    total_rows=total_rows,
                    failed_rows=0,
                )

            failure_detail = self._create_failure_detail(null_indices, total_rows)

            return RuleResult(
                rule_name=self.name,
                column=self.column,
                passed=False,
                total_rows=total_rows,
                failed_rows=len(null_indices),
                failure_details=failure_detail,
            )

        except ColumnNotFoundError:
            raise
        except Exception as e:
            return RuleResult(
                rule_name=self.name,
                column=self.column,
                passed=False,
                total_rows=len(df),
                error=f"Error executing not_null rule: {e}",
            )


class MinMaxRule(Rule):
    """Rule to check numeric values are within min/max bounds."""

    def __init__(
        self, name: str, column: str, min_value: float | None = None, max_value: float | None = None
    ) -> None:
        """Initialize MinMaxRule.

        Args:
            name: Name of the rule
            column: Column to validate
            min_value: Minimum allowed value (inclusive)
            max_value: Maximum allowed value (inclusive)

        Raises:
            RuleDefinitionError: If neither min nor max is specified
        """
        super().__init__(name, column)
        if min_value is None and max_value is None:
            raise RuleDefinitionError("MinMaxRule requires at least min or max value")
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, df: pd.DataFrame) -> RuleResult:
        """Validate that numeric values are within bounds.

        Args:
            df: DataFrame to validate

        Returns:
            RuleResult with validation outcome
        """
        try:
            self._check_column_exists(df)

            total_rows = len(df)

            # Filter out null values (they should be caught by not_null rule)
            non_null_mask = df[self.column].notna()
            data = df[self.column][non_null_mask]

            # Check if data is numeric
            if not pd.api.types.is_numeric_dtype(data):
                return RuleResult(
                    rule_name=self.name,
                    column=self.column,
                    passed=False,
                    total_rows=total_rows,
                    error=f"Column '{self.column}' is not numeric",
                )

            # Build condition for violations
            violations_mask = pd.Series([False] * len(data), index=data.index)

            if self.min_value is not None:
                violations_mask |= data < self.min_value

            if self.max_value is not None:
                violations_mask |= data > self.max_value

            violation_indices = data.index[violations_mask]

            if len(violation_indices) == 0:
                return RuleResult(
                    rule_name=self.name,
                    column=self.column,
                    passed=True,
                    total_rows=total_rows,
                    failed_rows=0,
                )

            failure_detail = self._create_failure_detail(violation_indices, total_rows)

            return RuleResult(
                rule_name=self.name,
                column=self.column,
                passed=False,
                total_rows=total_rows,
                failed_rows=len(violation_indices),
                failure_details=failure_detail,
            )

        except ColumnNotFoundError:
            raise
        except Exception as e:
            return RuleResult(
                rule_name=self.name,
                column=self.column,
                passed=False,
                total_rows=len(df),
                error=f"Error executing min/max rule: {e}",
            )


class UniqueRule(Rule):
    """Rule to check for duplicate values."""

    def validate(self, df: pd.DataFrame) -> RuleResult:
        """Validate that column has no duplicate values.

        Args:
            df: DataFrame to validate

        Returns:
            RuleResult with validation outcome
        """
        try:
            self._check_column_exists(df)

            total_rows = len(df)

            # Find duplicates (excluding nulls)
            duplicated_mask = df[self.column].duplicated(keep=False)
            null_mask = df[self.column].isna()
            # Only count non-null duplicates
            duplicate_indices = df.index[duplicated_mask & ~null_mask]

            if len(duplicate_indices) == 0:
                return RuleResult(
                    rule_name=self.name,
                    column=self.column,
                    passed=True,
                    total_rows=total_rows,
                    failed_rows=0,
                )

            failure_detail = self._create_failure_detail(duplicate_indices, total_rows)

            return RuleResult(
                rule_name=self.name,
                column=self.column,
                passed=False,
                total_rows=total_rows,
                failed_rows=len(duplicate_indices),
                failure_details=failure_detail,
            )

        except ColumnNotFoundError:
            raise
        except Exception as e:
            return RuleResult(
                rule_name=self.name,
                column=self.column,
                passed=False,
                total_rows=len(df),
                error=f"Error executing unique rule: {e}",
            )


class RegexRule(Rule):
    """Rule to check values match a regular expression pattern."""

    def __init__(self, name: str, column: str, pattern: str) -> None:
        """Initialize RegexRule.

        Args:
            name: Name of the rule
            column: Column to validate
            pattern: Regular expression pattern

        Raises:
            RuleDefinitionError: If pattern is invalid
        """
        super().__init__(name, column)
        try:
            self.pattern = re.compile(pattern)
        except re.error as e:
            raise RuleDefinitionError(f"Invalid regex pattern '{pattern}': {e}") from e
        self.pattern_str = pattern

    def validate(self, df: pd.DataFrame) -> RuleResult:
        """Validate that values match regex pattern.

        Args:
            df: DataFrame to validate

        Returns:
            RuleResult with validation outcome
        """
        try:
            self._check_column_exists(df)

            total_rows = len(df)

            # Filter out null values
            non_null_mask = df[self.column].notna()
            data = df[self.column][non_null_mask]

            # Convert to string and check pattern
            data_str = data.astype(str)
            matches = data_str.str.match(self.pattern, na=False)

            # Invert to get violations
            violation_indices = data.index[~matches]

            if len(violation_indices) == 0:
                return RuleResult(
                    rule_name=self.name,
                    column=self.column,
                    passed=True,
                    total_rows=total_rows,
                    failed_rows=0,
                )

            failure_detail = self._create_failure_detail(violation_indices, total_rows)

            return RuleResult(
                rule_name=self.name,
                column=self.column,
                passed=False,
                total_rows=total_rows,
                failed_rows=len(violation_indices),
                failure_details=failure_detail,
            )

        except ColumnNotFoundError:
            raise
        except Exception as e:
            return RuleResult(
                rule_name=self.name,
                column=self.column,
                passed=False,
                total_rows=len(df),
                error=f"Error executing regex rule: {e}",
            )


class AllowedValuesRule(Rule):
    """Rule to check values are in an allowed set."""

    def __init__(self, name: str, column: str, allowed_values: list[Any]) -> None:
        """Initialize AllowedValuesRule.

        Args:
            name: Name of the rule
            column: Column to validate
            allowed_values: List of allowed values

        Raises:
            RuleDefinitionError: If allowed_values is empty
        """
        super().__init__(name, column)
        if not allowed_values:
            raise RuleDefinitionError("allowed_values cannot be empty")
        self.allowed_values = set(allowed_values)

    def validate(self, df: pd.DataFrame) -> RuleResult:
        """Validate that values are in allowed set.

        Args:
            df: DataFrame to validate

        Returns:
            RuleResult with validation outcome
        """
        try:
            self._check_column_exists(df)

            total_rows = len(df)

            # Filter out null values
            non_null_mask = df[self.column].notna()
            data = df[self.column][non_null_mask]

            # Check if values are in allowed set
            in_allowed = data.isin(self.allowed_values)
            violation_indices = data.index[~in_allowed]

            if len(violation_indices) == 0:
                return RuleResult(
                    rule_name=self.name,
                    column=self.column,
                    passed=True,
                    total_rows=total_rows,
                    failed_rows=0,
                )

            failure_detail = self._create_failure_detail(violation_indices, total_rows)

            return RuleResult(
                rule_name=self.name,
                column=self.column,
                passed=False,
                total_rows=total_rows,
                failed_rows=len(violation_indices),
                failure_details=failure_detail,
            )

        except ColumnNotFoundError:
            raise
        except Exception as e:
            return RuleResult(
                rule_name=self.name,
                column=self.column,
                passed=False,
                total_rows=len(df),
                error=f"Error executing allowed_values rule: {e}",
            )


class RuleFactory:
    """Factory for creating rule instances from configuration."""

    @staticmethod
    def create_rules(rule_config: RuleConfig) -> list[Rule]:
        """Create rule instances from configuration.

        Args:
            rule_config: Rule configuration

        Returns:
            List of Rule instances

        Raises:
            RuleDefinitionError: If rule configuration is invalid
        """
        rules: list[Rule] = []

        for rule_type, rule_params in rule_config.rules.items():
            try:
                if rule_type == "not_null":
                    if rule_params:
                        rules.append(NotNullRule(rule_config.name, rule_config.column))

                elif rule_type == "min":
                    rules.append(
                        MinMaxRule(
                            f"{rule_config.name}_min",
                            rule_config.column,
                            min_value=rule_params,
                        )
                    )

                elif rule_type == "max":
                    rules.append(
                        MinMaxRule(
                            f"{rule_config.name}_max",
                            rule_config.column,
                            max_value=rule_params,
                        )
                    )

                elif rule_type == "unique":
                    if rule_params:
                        rules.append(UniqueRule(rule_config.name, rule_config.column))

                elif rule_type == "regex":
                    rules.append(
                        RegexRule(rule_config.name, rule_config.column, pattern=rule_params)
                    )

                elif rule_type == "allowed_values":
                    rules.append(
                        AllowedValuesRule(
                            rule_config.name, rule_config.column, allowed_values=rule_params
                        )
                    )

            except (RuleDefinitionError, TypeError, ValueError) as e:
                raise RuleDefinitionError(
                    f"Error creating {rule_type} rule for '{rule_config.name}': {e}"
                ) from e

        if not rules:
            raise RuleDefinitionError(
                f"No valid rules created for check '{rule_config.name}'"
            )

        return rules


__all__ = [
    "Rule",
    "NotNullRule",
    "MinMaxRule",
    "UniqueRule",
    "RegexRule",
    "AllowedValuesRule",
    "RuleFactory",
]
