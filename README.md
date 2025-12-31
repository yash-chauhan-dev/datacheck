# DataCheck

> Lightweight data quality validation CLI tool for engineers

[![CI](https://github.com/yash-chauhan-dev/datacheck/workflows/CI/badge.svg)](https://github.com/yash-chauhan-dev/datacheck/actions)
[![Coverage](https://codecov.io/gh/yash-chauhan-dev/datacheck/branch/main/graph/badge.svg)](https://codecov.io/gh/yash-chauhan-dev/datacheck)
[![Python Version](https://img.shields.io/pypi/pyversions/datacheck.svg)](https://pypi.org/project/datacheck/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What is DataCheck?

DataCheck is a simple, fast, and opinionated data validation tool for engineers who want to:
- Validate data quality without setting up heavy frameworks
- Fail CI/CD pipelines when data doesn't meet expectations
- Get instant feedback on data issues
- Write validation rules in simple YAML

Think of it as "Great Expectations, but lightweight and CLI-first."

## Quick Start

### Installation

```bash
pip install datacheck
```

### Basic Usage

1. Create a validation rules file (`rules.yaml`):

```yaml
checks:
  - name: age_validation
    column: age
    rules:
      not_null: true
      min: 0
      max: 120

  - name: email_format
    column: email
    rules:
      not_null: true
      regex: ".+@.+\\..+"

  - name: country_whitelist
    column: country
    rules:
      allowed_values: ["US", "UK", "CA", "AU"]
```

2. Run validation:

```bash
datacheck validate data.csv --rules rules.yaml
```

3. See results:

```
DataCheck v0.1.0
─────────────────────────────────────────────
Loading: data.csv (10,000 rows)
Running 3 validation rules...

✔ age_validation: All 10,000 rows passed
✘ email_format: 237 rows failed
✔ country_whitelist: All 10,000 rows passed

─────────────────────────────────────────────
Summary
─────────────────────────────────────────────
Total Checks: 3
Passed: 2
Failed: 1

VALIDATION FAILED (exit code 1)
```

## Features

- **Multiple data formats**: CSV, Parquet, SQLite, DuckDB
- **Simple YAML rules**: Easy to write and maintain
- **Beautiful terminal output**: Clear, colored results using Rich
- **CI/CD ready**: Proper exit codes for automation
- **Fast**: Built on Pandas and DuckDB
- **Extensible**: Easy to add custom rules

## Supported Rule Types

- `not_null`: Check for missing values
- `min` / `max`: Validate numeric ranges
- `unique`: Detect duplicates
- `regex`: Pattern matching
- `allowed_values`: Enum/whitelist validation

## Documentation

Full documentation coming soon.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

Built with:
- [Typer](https://typer.tiangolo.com/) for CLI
- [Pandas](https://pandas.pydata.org/) for data processing
- [DuckDB](https://duckdb.org/) for SQL support
- [Rich](https://rich.readthedocs.io/) for terminal output
