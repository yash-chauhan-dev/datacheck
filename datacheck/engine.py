"""Validation engine orchestration."""

from pathlib import Path
from typing import Any

import pandas as pd

from datacheck.config import ConfigLoader, ValidationConfig
from datacheck.exceptions import ConfigurationError, DataLoadError, ValidationError
from datacheck.loader import LoaderFactory
from datacheck.results import RuleResult, ValidationSummary
from datacheck.rules import RuleFactory


class ValidationEngine:
    """Engine for orchestrating data validation.

    The ValidationEngine coordinates the entire validation process:
    1. Loads data from various sources (CSV, Parquet, databases)
    2. Loads and parses validation configuration
    3. Creates rule instances from configuration
    4. Executes all rules against the data
    5. Aggregates results into a summary
    """

    def __init__(self, config: ValidationConfig | None = None, config_path: str | Path | None = None) -> None:
        """Initialize validation engine.

        Args:
            config: Pre-loaded validation configuration (optional)
            config_path: Path to configuration file (optional)

        Raises:
            ConfigurationError: If neither config nor config_path provided, or both provided
        """
        if config is not None and config_path is not None:
            raise ConfigurationError("Cannot provide both config and config_path")

        if config is None and config_path is None:
            # Try to auto-discover config file
            found_config = ConfigLoader.find_config()
            if found_config is None:
                raise ConfigurationError(
                    "No configuration provided and no config file found. "
                    "Searched for: .datacheck.yaml, .datacheck.yml, datacheck.yaml, datacheck.yml"
                )
            config_path = found_config

        if config_path is not None:
            self.config = ConfigLoader.load(config_path)
        else:
            self.config = config  # type: ignore

    def validate_file(
        self,
        file_path: str | Path,
        **loader_kwargs: Any,
    ) -> ValidationSummary:
        """Validate a data file against configured rules.

        Args:
            file_path: Path to the data file to validate
            **loader_kwargs: Additional arguments passed to the data loader

        Returns:
            ValidationSummary with aggregated results

        Raises:
            DataLoadError: If data cannot be loaded
            ValidationError: If validation fails unexpectedly
        """
        # Load data
        try:
            df = LoaderFactory.load(file_path, **loader_kwargs)
        except DataLoadError:
            raise
        except Exception as e:
            raise DataLoadError(f"Unexpected error loading data: {e}") from e

        # Validate the loaded data
        return self.validate_dataframe(df)

    def validate_dataframe(self, df: pd.DataFrame) -> ValidationSummary:
        """Validate a DataFrame against configured rules.

        Args:
            df: DataFrame to validate

        Returns:
            ValidationSummary with aggregated results

        Raises:
            ValidationError: If validation fails unexpectedly
        """
        results: list[RuleResult] = []

        # Execute each check configuration
        for check_config in self.config.checks:
            try:
                # Create rules from configuration
                rules = RuleFactory.create_rules(check_config)

                # Execute each rule
                for rule in rules:
                    try:
                        result = rule.validate(df)
                        results.append(result)
                    except Exception as e:
                        # If rule execution fails, create error result
                        error_result = RuleResult(
                            rule_name=rule.name,
                            column=rule.column,
                            passed=False,
                            total_rows=len(df),
                            error=f"Unexpected error executing rule: {e}",
                        )
                        results.append(error_result)

            except Exception as e:
                # If rule creation fails, create error result
                error_result = RuleResult(
                    rule_name=check_config.name,
                    column=check_config.column,
                    passed=False,
                    total_rows=len(df),
                    error=f"Error creating rules: {e}",
                )
                results.append(error_result)

        return ValidationSummary(results=results)

    def validate(
        self,
        file_path: str | Path | None = None,
        df: pd.DataFrame | None = None,
        **loader_kwargs: Any,
    ) -> ValidationSummary:
        """Validate data from either a file or DataFrame.

        Args:
            file_path: Path to the data file (optional)
            df: DataFrame to validate (optional)
            **loader_kwargs: Additional arguments passed to the data loader

        Returns:
            ValidationSummary with aggregated results

        Raises:
            ValidationError: If neither file_path nor df provided, or both provided
            DataLoadError: If data cannot be loaded from file
        """
        if file_path is not None and df is not None:
            raise ValidationError("Cannot provide both file_path and df")

        if file_path is None and df is None:
            raise ValidationError("Must provide either file_path or df")

        if file_path is not None:
            return self.validate_file(file_path, **loader_kwargs)
        else:
            return self.validate_dataframe(df)  # type: ignore


__all__ = [
    "ValidationEngine",
]
