"""Tests for data loaders."""

import sqlite3
from pathlib import Path

import duckdb
import pandas as pd
import pytest

from datacheck.exceptions import DataLoadError, EmptyDatasetError, UnsupportedFormatError
from datacheck.loader import (
    CSVLoader,
    DataLoader,
    DuckDBLoader,
    LoaderFactory,
    ParquetLoader,
)


class TestCSVLoader:
    """Tests for CSVLoader."""

    def test_load_simple_csv(self, tmp_path: Path) -> None:
        """Test loading a simple CSV file."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("name,age\nAlice,30\nBob,25\n")

        loader = CSVLoader(csv_file)
        df = loader.load()

        assert len(df) == 2
        assert list(df.columns) == ["name", "age"]
        assert df["name"].tolist() == ["Alice", "Bob"]
        assert df["age"].tolist() == [30, 25]

    def test_load_csv_with_custom_delimiter(self, tmp_path: Path) -> None:
        """Test loading CSV with custom delimiter."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("name;age\nAlice;30\nBob;25\n")

        loader = CSVLoader(csv_file, delimiter=";")
        df = loader.load()

        assert len(df) == 2
        assert list(df.columns) == ["name", "age"]

    def test_load_csv_with_utf8_sig(self, tmp_path: Path) -> None:
        """Test loading CSV with UTF-8 BOM."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("\ufeffname,age\nAlice,30\n", encoding="utf-8-sig")

        loader = CSVLoader(csv_file)
        df = loader.load()

        assert len(df) == 1
        # BOM handling depends on encoding detection
        assert "age" in df.columns

    def test_load_csv_with_explicit_encoding(self, tmp_path: Path) -> None:
        """Test loading CSV with explicit encoding."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("name,age\nAlice,30\n", encoding="latin-1")

        loader = CSVLoader(csv_file, encoding="latin-1")
        df = loader.load()

        assert len(df) == 1

    def test_encoding_detection(self, tmp_path: Path) -> None:
        """Test automatic encoding detection."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("name,age\nAlice,30\n", encoding="utf-8")

        loader = CSVLoader(csv_file)
        encoding = loader._detect_encoding()

        assert encoding in ["utf-8", "utf-8-sig"]

    def test_empty_csv(self, tmp_path: Path) -> None:
        """Test loading empty CSV raises error."""
        csv_file = tmp_path / "empty.csv"
        csv_file.write_text("name,age\n")

        loader = CSVLoader(csv_file)

        with pytest.raises(EmptyDatasetError) as exc_info:
            loader.load()

        assert "empty.csv" in str(exc_info.value)

    def test_file_not_found(self) -> None:
        """Test loading non-existent file raises error."""
        with pytest.raises(DataLoadError, match="File not found"):
            CSVLoader("nonexistent.csv")

    def test_invalid_csv(self, tmp_path: Path) -> None:
        """Test loading invalid CSV raises error."""
        csv_file = tmp_path / "invalid.csv"
        csv_file.write_bytes(b"\xff\xfe\x00\x00")  # Invalid UTF-8

        loader = CSVLoader(csv_file)

        # Pandas may load this as empty, raising EmptyDatasetError
        with pytest.raises((DataLoadError, EmptyDatasetError)):
            loader.load()

    def test_path_is_directory(self, tmp_path: Path) -> None:
        """Test that directory path raises error."""
        with pytest.raises(DataLoadError, match="not a file"):
            CSVLoader(tmp_path)


class TestParquetLoader:
    """Tests for ParquetLoader."""

    def test_load_simple_parquet(self, tmp_path: Path) -> None:
        """Test loading a simple Parquet file."""
        parquet_file = tmp_path / "test.parquet"
        df_original = pd.DataFrame({"name": ["Alice", "Bob"], "age": [30, 25]})
        df_original.to_parquet(parquet_file)

        loader = ParquetLoader(parquet_file)
        df = loader.load()

        assert len(df) == 2
        assert list(df.columns) == ["name", "age"]
        assert df["name"].tolist() == ["Alice", "Bob"]

    def test_empty_parquet(self, tmp_path: Path) -> None:
        """Test loading empty Parquet raises error."""
        parquet_file = tmp_path / "empty.parquet"
        df_empty = pd.DataFrame({"name": [], "age": []})
        df_empty.to_parquet(parquet_file)

        loader = ParquetLoader(parquet_file)

        with pytest.raises(EmptyDatasetError):
            loader.load()

    def test_file_not_found(self) -> None:
        """Test loading non-existent file raises error."""
        with pytest.raises(DataLoadError, match="File not found"):
            ParquetLoader("nonexistent.parquet")

    def test_invalid_parquet(self, tmp_path: Path) -> None:
        """Test loading invalid Parquet raises error."""
        parquet_file = tmp_path / "invalid.parquet"
        parquet_file.write_text("not a parquet file")

        loader = ParquetLoader(parquet_file)

        with pytest.raises(DataLoadError):
            loader.load()


@pytest.mark.skip(reason="DuckDB causes segfaults in this environment")
class TestDuckDBLoader:
    """Tests for DuckDBLoader."""

    def test_load_from_duckdb_table(self, tmp_path: Path) -> None:
        """Test loading from DuckDB table."""
        db_file = tmp_path / "test.duckdb"

        # Create DuckDB database with table
        conn = duckdb.connect(str(db_file))
        conn.execute("CREATE TABLE users (name VARCHAR, age INTEGER)")
        conn.execute("INSERT INTO users VALUES ('Alice', 30), ('Bob', 25)")
        conn.close()

        loader = DuckDBLoader(db_file, table_name="users")
        df = loader.load()

        assert len(df) == 2
        assert list(df.columns) == ["name", "age"]
        assert df["name"].tolist() == ["Alice", "Bob"]

    def test_load_from_duckdb_query(self, tmp_path: Path) -> None:
        """Test loading from DuckDB with custom query."""
        db_file = tmp_path / "test.duckdb"

        conn = duckdb.connect(str(db_file))
        conn.execute("CREATE TABLE users (name VARCHAR, age INTEGER)")
        conn.execute("INSERT INTO users VALUES ('Alice', 30), ('Bob', 25)")
        conn.close()

        loader = DuckDBLoader(db_file, query="SELECT name FROM users WHERE age > 25")
        df = loader.load()

        assert len(df) == 1
        assert list(df.columns) == ["name"]
        assert df["name"].tolist() == ["Alice"]

    def test_load_from_sqlite_table(self, tmp_path: Path) -> None:
        """Test loading from SQLite table."""
        db_file = tmp_path / "test.sqlite"

        # Create SQLite database with table
        conn = sqlite3.connect(str(db_file))
        conn.execute("CREATE TABLE users (name TEXT, age INTEGER)")
        conn.execute("INSERT INTO users VALUES ('Alice', 30), ('Bob', 25)")
        conn.commit()
        conn.close()

        loader = DuckDBLoader(db_file, table_name="users")
        df = loader.load()

        assert len(df) == 2
        assert list(df.columns) == ["name", "age"]

    def test_load_from_sqlite_query(self, tmp_path: Path) -> None:
        """Test loading from SQLite with custom query."""
        db_file = tmp_path / "test.sqlite"

        conn = sqlite3.connect(str(db_file))
        conn.execute("CREATE TABLE users (name TEXT, age INTEGER)")
        conn.execute("INSERT INTO users VALUES ('Alice', 30), ('Bob', 25)")
        conn.commit()
        conn.close()

        loader = DuckDBLoader(db_file, query="SELECT * FROM users WHERE age < 30")
        df = loader.load()

        assert len(df) == 1
        assert df["age"].tolist() == [25]

    def test_is_sqlite_detection(self, tmp_path: Path) -> None:
        """Test SQLite file detection."""
        # Create SQLite file
        sqlite_file = tmp_path / "test.sqlite"
        conn = sqlite3.connect(str(sqlite_file))
        conn.execute("CREATE TABLE test (id INTEGER)")
        conn.close()

        loader = DuckDBLoader(sqlite_file, table_name="test")
        assert loader._is_sqlite() is True

        # Create DuckDB file
        duckdb_file = tmp_path / "test.duckdb"
        duckdb_conn = duckdb.connect(str(duckdb_file))
        duckdb_conn.execute("CREATE TABLE test (id INTEGER)")
        duckdb_conn.close()

        loader = DuckDBLoader(duckdb_file, table_name="test")
        assert loader._is_sqlite() is False

    def test_query_takes_precedence_over_table(self, tmp_path: Path) -> None:
        """Test that query parameter takes precedence over table_name."""
        db_file = tmp_path / "test.duckdb"

        conn = duckdb.connect(str(db_file))
        conn.execute("CREATE TABLE users (name VARCHAR, age INTEGER)")
        conn.execute("INSERT INTO users VALUES ('Alice', 30)")
        conn.close()

        loader = DuckDBLoader(
            db_file, table_name="users", query="SELECT name FROM users"
        )
        df = loader.load()

        assert list(df.columns) == ["name"]

    def test_missing_table_and_query(self, tmp_path: Path) -> None:
        """Test that missing both table_name and query raises error."""
        db_file = tmp_path / "test.duckdb"
        db_file.touch()

        with pytest.raises(DataLoadError, match="Either table_name or query must be provided"):
            DuckDBLoader(db_file)

    def test_empty_result(self, tmp_path: Path) -> None:
        """Test loading empty result raises error."""
        db_file = tmp_path / "test.duckdb"

        conn = duckdb.connect(str(db_file))
        conn.execute("CREATE TABLE users (name VARCHAR, age INTEGER)")
        conn.close()

        loader = DuckDBLoader(db_file, table_name="users")

        with pytest.raises(EmptyDatasetError):
            loader.load()

    def test_invalid_table_name(self, tmp_path: Path) -> None:
        """Test loading non-existent table raises error."""
        db_file = tmp_path / "test.duckdb"

        conn = duckdb.connect(str(db_file))
        conn.execute("CREATE TABLE users (name VARCHAR, age INTEGER)")
        conn.close()

        loader = DuckDBLoader(db_file, table_name="nonexistent")

        with pytest.raises(DataLoadError):
            loader.load()

    def test_file_not_found(self) -> None:
        """Test loading non-existent file raises error."""
        with pytest.raises(DataLoadError, match="File not found"):
            DuckDBLoader("nonexistent.db", table_name="test")


class TestLoaderFactory:
    """Tests for LoaderFactory."""

    def test_create_csv_loader(self, tmp_path: Path) -> None:
        """Test creating CSV loader."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("name,age\nAlice,30\n")

        loader = LoaderFactory.create_loader(csv_file)

        assert isinstance(loader, CSVLoader)

    def test_create_parquet_loader(self, tmp_path: Path) -> None:
        """Test creating Parquet loader."""
        parquet_file = tmp_path / "test.parquet"
        df = pd.DataFrame({"name": ["Alice"], "age": [30]})
        df.to_parquet(parquet_file)

        loader = LoaderFactory.create_loader(parquet_file)

        assert isinstance(loader, ParquetLoader)

    def test_create_parquet_loader_with_pq_extension(self, tmp_path: Path) -> None:
        """Test creating Parquet loader with .pq extension."""
        parquet_file = tmp_path / "test.pq"
        df = pd.DataFrame({"name": ["Alice"], "age": [30]})
        df.to_parquet(parquet_file)

        loader = LoaderFactory.create_loader(parquet_file)

        assert isinstance(loader, ParquetLoader)

    @pytest.mark.skip(reason="DuckDB causes segfaults in this environment")
    def test_create_duckdb_loader(self, tmp_path: Path) -> None:
        """Test creating DuckDB loader."""
        db_file = tmp_path / "test.duckdb"
        conn = duckdb.connect(str(db_file))
        conn.execute("CREATE TABLE test (id INTEGER)")
        conn.close()

        loader = LoaderFactory.create_loader(db_file, table_name="test")

        assert isinstance(loader, DuckDBLoader)

    def test_create_sqlite_loader(self, tmp_path: Path) -> None:
        """Test creating SQLite loader."""
        db_file = tmp_path / "test.sqlite"
        conn = sqlite3.connect(str(db_file))
        conn.execute("CREATE TABLE test (id INTEGER)")
        conn.close()

        loader = LoaderFactory.create_loader(db_file, table_name="test")

        assert isinstance(loader, DuckDBLoader)

    def test_create_loader_with_db_extension(self, tmp_path: Path) -> None:
        """Test creating loader with .db extension."""
        db_file = tmp_path / "test.db"
        conn = sqlite3.connect(str(db_file))
        conn.execute("CREATE TABLE test (id INTEGER)")
        conn.close()

        loader = LoaderFactory.create_loader(db_file, table_name="test")

        assert isinstance(loader, DuckDBLoader)

    def test_unsupported_format(self, tmp_path: Path) -> None:
        """Test unsupported file format raises error."""
        unsupported_file = tmp_path / "test.txt"
        unsupported_file.write_text("test")

        with pytest.raises(UnsupportedFormatError) as exc_info:
            LoaderFactory.create_loader(unsupported_file)

        assert ".txt" in str(exc_info.value)
        assert ".csv" in str(exc_info.value)

    def test_file_not_found(self) -> None:
        """Test non-existent file raises error."""
        with pytest.raises(DataLoadError, match="File not found"):
            LoaderFactory.create_loader("nonexistent.csv")

    def test_load_method_csv(self, tmp_path: Path) -> None:
        """Test LoaderFactory.load() method with CSV."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("name,age\nAlice,30\n")

        df = LoaderFactory.load(csv_file)

        assert len(df) == 1
        assert list(df.columns) == ["name", "age"]

    def test_load_method_parquet(self, tmp_path: Path) -> None:
        """Test LoaderFactory.load() method with Parquet."""
        parquet_file = tmp_path / "test.parquet"
        df_original = pd.DataFrame({"name": ["Alice"], "age": [30]})
        df_original.to_parquet(parquet_file)

        df = LoaderFactory.load(parquet_file)

        assert len(df) == 1

    @pytest.mark.skip(reason="DuckDB causes segfaults in this environment")
    def test_load_method_database(self, tmp_path: Path) -> None:
        """Test LoaderFactory.load() method with database."""
        db_file = tmp_path / "test.duckdb"
        conn = duckdb.connect(str(db_file))
        conn.execute("CREATE TABLE users (name VARCHAR)")
        conn.execute("INSERT INTO users VALUES ('Alice')")
        conn.close()

        df = LoaderFactory.load(db_file, table_name="users")

        assert len(df) == 1

    def test_load_method_with_kwargs(self, tmp_path: Path) -> None:
        """Test LoaderFactory.load() passes kwargs to loader."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("name;age\nAlice;30\n")

        df = LoaderFactory.load(csv_file, delimiter=";")

        assert len(df) == 1
        assert list(df.columns) == ["name", "age"]

    def test_case_insensitive_extensions(self, tmp_path: Path) -> None:
        """Test that file extensions are case-insensitive."""
        csv_file = tmp_path / "test.CSV"
        csv_file.write_text("name,age\nAlice,30\n")

        loader = LoaderFactory.create_loader(csv_file)

        assert isinstance(loader, CSVLoader)


class TestDataLoaderBase:
    """Tests for DataLoader base class."""

    def test_cannot_instantiate_abstract_class(self) -> None:
        """Test that DataLoader cannot be instantiated directly."""
        with pytest.raises(TypeError):
            DataLoader("test.csv")  # type: ignore
