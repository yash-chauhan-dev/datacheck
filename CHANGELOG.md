# Changelog

All notable changes to DataCheck will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2025-12-31

### 🚀 Enhancements

#### Documentation
- **Comprehensive documentation site**: Added 28-page documentation with MkDocs Material
- **Getting Started guides**: Installation, Quick Start, and First Validation tutorials
- **Real-world use cases**: Detailed examples with ROI metrics (6x faster setup, $50-100/month savings)
- **Integration guides**: CI/CD, GitHub Actions, Airflow, ML pipelines, and more
- **Professional formatting**: Simplified and cleaned up documentation for better readability

#### Distribution & Release
- **PyPI package rename**: Changed from `datacheck` to `datacheck-cli` to avoid conflicts
- **Automated release workflow**: Auto-release on version bumps with comprehensive testing
- **CI/CD integration**: Tag-based releases with PyPI publishing
- **GitHub Pages deployment**: Automatic documentation deployment on main branch updates

#### Developer Experience
- **Improved project structure**: Added `packages` configuration for Poetry
- **Documentation dependencies**: Added mkdocs, mkdocs-material, and plugins to docs group
- **Better CI/CD workflows**: Streamlined release process with proper dependency chains

### 🐛 Bug Fixes
- **Poetry packaging**: Fixed installation error by adding `packages = [{include = "datacheck"}]`
- **Workflow optimization**: Removed problematic wait-for-ci job that was causing failures

### 📚 Documentation
- **28 new documentation pages** covering all features and use cases
- **4 real-world scenarios** with before/after comparisons and impact metrics
- **Complete API reference** for CLI and Python usage
- **Contribution guidelines** for developers

## [0.1.0] - 2025-01-01

### 🎉 Initial Release

DataCheck's first public release! A lightweight, fast, and developer-friendly CLI tool for data quality validation.

### ✨ Features

#### Core Validation Engine
- **Multiple data format support**: CSV, Parquet, SQLite databases
- **Comprehensive validation rules**:
  - `not_null`: Check for missing values
  - `min` / `max`: Numeric range validation
  - `unique`: Ensure values are unique
  - `regex`: Pattern matching validation
  - `allowed_values`: Whitelist validation
- **Flexible configuration**: YAML-based validation rules
- **Auto-discovery**: Automatically finds `.datacheck.yaml` in current directory

#### CLI Interface
- **Simple command**: `datacheck validate <file> --config <config.yaml>`
- **Multiple output formats**:
  - Beautiful terminal output with color and formatting (Rich)
  - JSON output for automation and CI/CD integration
- **CI/CD ready exit codes**:
  - `0`: All validations passed
  - `1`: Some validations failed
  - `2`: Configuration error
  - `3`: Data loading error
  - `4`: Runtime error

#### Data Loaders
- **CSV Loader**: UTF-8/UTF-8-BOM support, automatic encoding detection
- **Parquet Loader**: Efficient columnar format support via PyArrow
- **SQLite Loader**: Direct database table and query support
- **DuckDB Loader**: Optional DuckDB support (Linux/macOS only)

#### Output & Reporting
- **Terminal output**: Color-coded results with detailed failure information
- **JSON export**: Machine-readable output for automation
- **Detailed failure reports**: Shows failure counts, percentages, and sample row indices
- **Summary statistics**: Total rules, passed, failed, and error counts

#### Developer Experience
- **Type safety**: Full mypy type checking
- **Well tested**: 180 tests, 92% code coverage
- **Comprehensive documentation**: README, CONTRIBUTING, examples
- **Python API**: Use DataCheck programmatically in your applications

### 📚 Documentation

- **README.md**: Complete user guide with quick start, usage, and API reference
- **CONTRIBUTING.md**: Developer guide for contributors
- **Examples directory**:
  - Basic examples (CSV)
  - Advanced examples (CSV with complex rules)
  - Real-world examples (sales data, user data)
  - Parquet format example
  - SQLite database example

### 🔧 Configuration

- **YAML-based config**: Simple, readable validation rules
- **Multiple checks per file**: Validate multiple columns with different rules
- **Flexible rule combinations**: Mix and match validation rules
- **Auto-discovery**: `.datacheck.yaml` automatically detected

### 🏗️ Infrastructure

- **CI/CD Pipeline**: GitHub Actions workflow testing on:
  - Python 3.10, 3.11, 3.12
  - Ubuntu, macOS, Windows
- **Code Quality**:
  - Ruff linting (zero errors)
  - mypy type checking (100% coverage)
  - pytest with 92% code coverage
- **Automated dependency updates**: Dependabot configuration
- **Issue templates**: Bug report, feature request, documentation, question
- **Pull request template**: Comprehensive PR checklist

### 📦 Distribution

- **PyPI package**: `pip install datacheck-cli`
- **Poetry support**: `poetry add datacheck-cli`
- **Python versions**: 3.10, 3.11, 3.12
- **Platforms**: Linux, macOS, Windows

### 🔒 Security

- **MIT License**: Open source and permissive
- **No telemetry**: Your data stays on your machine
- **Sandboxed execution**: Safe to run on production data

### 🎯 Performance

- **Fast validation**: Powered by pandas for efficient data processing
- **Memory efficient**: Processes data in-memory using pandas DataFrames
- **Scalable**: Handles datasets up to available memory

### 📈 Stats

- **10 Python modules**: Clean, modular architecture
- **701 lines of code**: Focused and maintainable
- **180 tests**: Comprehensive test coverage
- **13 example files**: Learn by doing
- **1,170 lines of documentation**: Well documented

### 🙏 Acknowledgments

Built with:
- **Typer**: Beautiful CLI framework
- **Rich**: Terminal formatting and colors
- **Pandas**: Data manipulation
- **PyArrow**: Parquet support
- **Poetry**: Dependency management
- **Pytest**: Testing framework
- **Ruff**: Lightning-fast linting
- **mypy**: Static type checking

---

## Future Releases

See [README.md](README.md#roadmap) for planned features in upcoming releases.

---

**Note**: This is the first public release of DataCheck. Future releases will be documented here following the same format.

[0.1.0]: https://github.com/yash-chauhan-dev/datacheck/releases/tag/v0.1.0
