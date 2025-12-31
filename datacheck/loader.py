"""Data loaders for various formats."""

import sqlite3
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import pandas as pd

from datacheck.exceptions import DataLoadError, EmptyDatasetError, UnsupportedFormatError

# Optional DuckDB import
try:
    import duckdb

    HAS_DUCKDB = True
except ImportError:
    HAS_DUCKDB = False
    duckdb = None  # type: ignore[assignment]


class DataLoader(ABC):
    """Abstract base class for data loaders.

    Attributes:
        file_path: Path to the data file
    """

    def __init__(self, file_path: str | Path) -> None:
        """Initialize data loader.

        Args:
            file_path: Path to the data file

        Raises:
            DataLoadError: If file does not exist
        """
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise DataLoadError(f"File not found: {file_path}")
        if not self.file_path.is_file():
            raise DataLoadError(f"Path is not a file: {file_path}")

    @abstractmethod
    def load(self) -> pd.DataFrame:
        """Load data from file into a pandas DataFrame.

        Returns:
            DataFrame containing the loaded data

        Raises:
            DataLoadError: If data cannot be loaded
            EmptyDatasetError: If loaded data is empty
        """
        pass

    def _validate_dataframe(self, df: pd.DataFrame) -> None:
        """Validate that DataFrame is not empty.

        Args:
            df: DataFrame to validate

        Raises:
            EmptyDatasetError: If DataFrame is empty
        """
        if df.empty:
            raise EmptyDatasetError(f"Dataset is empty: {self.file_path}")


class CSVLoader(DataLoader):
    """Loader for CSV files with automatic encoding detection."""

    def __init__(
        self,
        file_path: str | Path,
        encoding: str | None = None,
        delimiter: str = ",",
        **kwargs: Any,
    ) -> None:
        """Initialize CSV loader.

        Args:
            file_path: Path to the CSV file
            encoding: File encoding (auto-detected if None)
            delimiter: CSV delimiter character
            **kwargs: Additional arguments passed to pandas.read_csv
        """
        super().__init__(file_path)
        self.encoding = encoding
        self.delimiter = delimiter
        self.kwargs = kwargs

    def _detect_encoding(self) -> str:
        """Detect file encoding.

        Returns:
            Detected encoding (defaults to utf-8 if detection fails)
        """
        if self.encoding:
            return self.encoding

        # Try common encodings
        encodings = ["utf-8", "utf-8-sig", "latin-1", "iso-8859-1", "cp1252"]

        for encoding in encodings:
            try:
                with open(self.file_path, encoding=encoding) as f:
                    f.read(1024)  # Try to read first 1KB
                return encoding
            except (UnicodeDecodeError, LookupError):
                continue

        # Default to utf-8 if all fail
        return "utf-8"

    def load(self) -> pd.DataFrame:
        """Load CSV file into DataFrame.

        Returns:
            DataFrame containing CSV data

        Raises:
            DataLoadError: If CSV cannot be loaded
            EmptyDatasetError: If CSV is empty
        """
        try:
            encoding = self._detect_encoding()
            df: pd.DataFrame = pd.read_csv(
                self.file_path, encoding=encoding, delimiter=self.delimiter, **self.kwargs
            )
            self._validate_dataframe(df)
            return df
        except EmptyDatasetError:
            raise
        except Exception as e:
            raise DataLoadError(f"Error loading CSV file {self.file_path}: {e}") from e


class ParquetLoader(DataLoader):
    """Loader for Parquet files."""

    def __init__(self, file_path: str | Path, **kwargs: Any) -> None:
        """Initialize Parquet loader.

        Args:
            file_path: Path to the Parquet file
            **kwargs: Additional arguments passed to pandas.read_parquet
        """
        super().__init__(file_path)
        self.kwargs = kwargs

    def load(self) -> pd.DataFrame:
        """Load Parquet file into DataFrame.

        Returns:
            DataFrame containing Parquet data

        Raises:
            DataLoadError: If Parquet cannot be loaded
            EmptyDatasetError: If Parquet is empty
        """
        try:
            df = pd.read_parquet(self.file_path, **self.kwargs)
            self._validate_dataframe(df)
            return df
        except EmptyDatasetError:
            raise
        except Exception as e:
            raise DataLoadError(f"Error loading Parquet file {self.file_path}: {e}") from e


class DuckDBLoader(DataLoader):
    """Loader for DuckDB and SQLite database files."""

    def __init__(
        self, file_path: str | Path, table_name: str | None = None, query: str | None = None
    ) -> None:
        """Initialize DuckDB/SQLite loader.

        Args:
            file_path: Path to the database file
            table_name: Name of table to load (if query not provided)
            query: SQL query to execute (takes precedence over table_name)

        Raises:
            DataLoadError: If neither table_name nor query is provided
        """
        super().__init__(file_path)
        if not table_name and not query:
            raise DataLoadError("Either table_name or query must be provided")
        self.table_name = table_name
        self.query = query

    def _is_sqlite(self) -> bool:
        """Check if file is SQLite database.

        Returns:
            True if file is SQLite, False otherwise
        """
        try:
            with open(self.file_path, "rb") as f:
                header = f.read(16)
            return header[:6] == b"SQLite"
        except Exception:
            return False

    def _build_query(self) -> str:
        """Build SQL query from table name or use provided query.

        Returns:
            SQL query string
        """
        if self.query:
            return self.query
        return f"SELECT * FROM {self.table_name}"

    def load(self) -> pd.DataFrame:
        """Load data from database into DataFrame.

        Returns:
            DataFrame containing database data

        Raises:
            DataLoadError: If database cannot be loaded or DuckDB is not installed
            EmptyDatasetError: If query returns no data
        """
        query = self._build_query()

        try:
            if self._is_sqlite():
                # Use sqlite3 for SQLite files
                sqlite_conn = sqlite3.connect(str(self.file_path))
                try:
                    df = pd.read_sql_query(query, sqlite_conn)
                finally:
                    sqlite_conn.close()
            else:
                # Use DuckDB for DuckDB files
                if not HAS_DUCKDB:
                    raise DataLoadError(
                        "DuckDB is not installed. Install it with: pip install 'datacheck[duckdb]'"
                    )
                duckdb_conn = duckdb.connect(str(self.file_path), read_only=True)
                try:
                    df = duckdb_conn.execute(query).fetchdf()
                finally:
                    duckdb_conn.close()

            self._validate_dataframe(df)
            return df

        except EmptyDatasetError:
            raise
        except Exception as e:
            raise DataLoadError(
                f"Error loading database file {self.file_path}: {e}"
            ) from e


class LoaderFactory:
    """Factory for creating appropriate data loaders based on file format."""

    @staticmethod
    def create_loader(file_path: str | Path, **kwargs: Any) -> DataLoader:
        """Create appropriate loader for the given file.

        Args:
            file_path: Path to the data file
            **kwargs: Additional arguments passed to the loader

        Returns:
            DataLoader instance for the file format

        Raises:
            UnsupportedFormatError: If file format is not supported
            DataLoadError: If file does not exist
        """
        path = Path(file_path)

        # Check if file exists
        if not path.exists():
            raise DataLoadError(f"File not found: {file_path}")

        # Determine format from extension
        suffix = path.suffix.lower()

        if suffix == ".csv":
            return CSVLoader(file_path, **kwargs)
        elif suffix in [".parquet", ".pq"]:
            return ParquetLoader(file_path, **kwargs)
        elif suffix in [".db", ".duckdb", ".sqlite", ".sqlite3"]:
            return DuckDBLoader(file_path, **kwargs)
        else:
            raise UnsupportedFormatError(
                f"Unsupported file format: {suffix}. "
                f"Supported formats: .csv, .parquet, .pq, .db, .duckdb, .sqlite, .sqlite3"
            )

    @staticmethod
    def load(file_path: str | Path, **kwargs: Any) -> pd.DataFrame:
        """Load data from file using appropriate loader.

        Args:
            file_path: Path to the data file
            **kwargs: Additional arguments passed to the loader

        Returns:
            DataFrame containing the loaded data

        Raises:
            UnsupportedFormatError: If file format is not supported
            DataLoadError: If data cannot be loaded
            EmptyDatasetError: If loaded data is empty
        """
        loader = LoaderFactory.create_loader(file_path, **kwargs)
        return loader.load()


__all__ = [
    "DataLoader",
    "CSVLoader",
    "ParquetLoader",
    "DuckDBLoader",
    "LoaderFactory",
]
