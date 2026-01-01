# Installation

## pip (Recommended)

```bash
pip install datacheck-cli
```

Verify installation:
```bash
datacheck version
```

## With DuckDB Support (Linux/macOS only)

```bash
pip install datacheck-cli[duckdb]
```

::: warning Windows Users
DuckDB support is not available on Windows due to compatibility issues.
:::

## Development Installation

```bash
git clone https://github.com/yash-chauhan-dev/datacheck
cd datacheck
poetry install
poetry run datacheck --help
```

## Requirements

- Python 3.10 or higher
- pip or Poetry

## Upgrade

```bash
pip install --upgrade datacheck-cli
```

## Uninstall

```bash
pip uninstall datacheck-cli
```
