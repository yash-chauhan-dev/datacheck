"""Custom exceptions for DataCheck."""


class DataCheckError(Exception):
    """Base exception for all DataCheck errors."""

    pass


class ConfigurationError(DataCheckError):
    """Raised when there is an error in the configuration file."""

    pass


class ValidationError(DataCheckError):
    """Raised when data validation fails."""

    pass


class DataLoadError(DataCheckError):
    """Raised when data cannot be loaded from a source."""

    pass


class RuleDefinitionError(DataCheckError):
    """Raised when a rule is improperly defined."""

    pass


class UnsupportedFormatError(DataCheckError):
    """Raised when an unsupported file format is encountered."""

    pass


class ColumnNotFoundError(DataCheckError):
    """Raised when a specified column is not found in the dataset."""

    def __init__(self, column_name: str, available_columns: list[str]) -> None:
        """Initialize ColumnNotFoundError.

        Args:
            column_name: The name of the column that was not found
            available_columns: List of available column names in the dataset
        """
        self.column_name = column_name
        self.available_columns = available_columns
        message = (
            f"Column '{column_name}' not found in dataset. "
            f"Available columns: {', '.join(available_columns)}"
        )
        super().__init__(message)


class EmptyDatasetError(DataCheckError):
    """Raised when a dataset is empty or has no rows."""

    pass


__all__ = [
    "DataCheckError",
    "ConfigurationError",
    "ValidationError",
    "DataLoadError",
    "RuleDefinitionError",
    "UnsupportedFormatError",
    "ColumnNotFoundError",
    "EmptyDatasetError",
]
