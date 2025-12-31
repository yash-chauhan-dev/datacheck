"""DataCheck - Lightweight data quality validation CLI tool."""

from datacheck.exceptions import (
    ColumnNotFoundError,
    ConfigurationError,
    DataCheckError,
    DataLoadError,
    EmptyDatasetError,
    RuleDefinitionError,
    UnsupportedFormatError,
    ValidationError,
)
from datacheck.loader import (
    CSVLoader,
    DataLoader,
    DuckDBLoader,
    LoaderFactory,
    ParquetLoader,
)

__version__ = "0.1.0"
__author__ = "datacheck"
__email__ = "hello@datacheck.com"

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    # Exceptions
    "DataCheckError",
    "ConfigurationError",
    "ValidationError",
    "DataLoadError",
    "RuleDefinitionError",
    "UnsupportedFormatError",
    "ColumnNotFoundError",
    "EmptyDatasetError",
    # Loaders
    "DataLoader",
    "CSVLoader",
    "ParquetLoader",
    "DuckDBLoader",
    "LoaderFactory",
]
