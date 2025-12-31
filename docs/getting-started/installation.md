# Installation

DataCheck can be installed in multiple ways depending on your needs.

---

## Install from PyPI (Recommended)

The easiest way to install DataCheck is via pip:

```bash
pip install datacheck-cli
```

This will install the latest stable version from [PyPI](https://pypi.org/project/datacheck-cli/).

### Verify Installation

```bash
datacheck --version
```

Expected output:
```
DataCheck v0.1.0
```

---

## Install from Source

For development or to get the latest features:

```bash
# Clone the repository
git clone https://github.com/yash-chauhan-dev/datacheck.git
cd datacheck

# Install with Poetry
poetry install

# Or install with pip in editable mode
pip install -e .
```

---

## Requirements

- **Python**: 3.10 or higher
- **Operating System**: Linux, macOS, or Windows

### Dependencies

DataCheck has minimal dependencies:

- `pandas` - Data processing
- `typer` - CLI framework
- `rich` - Terminal output
- `pyyaml` - Configuration parsing
- `pyarrow` - Parquet support

**Optional**:
- `duckdb` - DuckDB support (Linux/macOS only)

---

## Optional: Install with DuckDB Support

On Linux and macOS, you can install with DuckDB support:

```bash
pip install datacheck-cli[duckdb]
```

!!! note "Windows Users"
    DuckDB is currently not available on Windows due to compatibility issues.
    You can still use CSV, Parquet, and SQLite formats.

---

## Virtual Environment (Recommended)

It's recommended to install DataCheck in a virtual environment:

=== "venv"

    ```bash
    # Create virtual environment
    python -m venv venv

    # Activate (Linux/macOS)
    source venv/bin/activate

    # Activate (Windows)
    venv\Scripts\activate

    # Install DataCheck
    pip install datacheck-cli
    ```

=== "conda"

    ```bash
    # Create conda environment
    conda create -n datacheck python=3.10

    # Activate
    conda activate datacheck

    # Install DataCheck
    pip install datacheck-cli
    ```

=== "poetry"

    ```bash
    # Add to your project
    poetry add datacheck-cli

    # Or create new project
    poetry new my-project
    cd my-project
    poetry add datacheck-cli
    ```

---

## Troubleshooting

### Command not found

If `datacheck` command is not found after installation:

1. Ensure pip install directory is in your PATH:
   ```bash
   # Check pip install location
   pip show datacheck-cli

   # Add to PATH (Linux/macOS)
   export PATH="$PATH:$HOME/.local/bin"
   ```

2. Or use via Python module:
   ```bash
   python -m datacheck validate data.csv --config rules.yaml
   ```

### ImportError

If you see import errors:

```bash
# Reinstall with force
pip install --force-reinstall datacheck-cli

# Or update pip
pip install --upgrade pip
pip install datacheck-cli
```

### Permission Denied

On Linux/macOS, if you get permission errors:

```bash
# Use user install
pip install --user datacheck-cli

# Or use sudo (not recommended)
sudo pip install datacheck-cli
```

---

## Next Steps

Once installed, proceed to the [Quick Start](quick-start.md) guide to run your first validation!
