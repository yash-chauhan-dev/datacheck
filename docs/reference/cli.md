# CLI Reference

Complete reference for DataCheck command-line interface.

---

## Commands

### validate

Validate data files against validation rules.

```bash
datacheck validate <file> [OPTIONS]
```

**Arguments**:

- `file` - Path to data file (CSV, Parquet, or database)

**Options**:

- `--config PATH` - Path to validation config file (YAML)
- `--format FORMAT` - Output format: `terminal` (default) or `json`
- `--json-output PATH` - Save JSON output to file
- `--table NAME` - Table name (for database files)

**Examples**:

```bash
# Basic validation
datacheck validate data.csv --config rules.yaml

# JSON output
datacheck validate data.csv --config rules.yaml --format json

# Save JSON to file
datacheck validate data.csv --config rules.yaml --format json --json-output results.json

# Database table
datacheck validate data.db --table customers --config rules.yaml
```

---

### version

Show DataCheck version.

```bash
datacheck --version
datacheck version
```

---

### help

Show help information.

```bash
datacheck --help
datacheck validate --help
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success - all validations passed |
| 1 | Failed - some validations failed |
| 2 | Config Error - configuration file error |
| 3 | Data Error - data loading error |
| 4 | Runtime Error - unexpected error |

See [Exit Codes](../user-guide/exit-codes.md) for details.

---

## Configuration File Auto-Discovery

If `--config` is not specified, DataCheck looks for:

1. `.datacheck.yaml`
2. `.datacheck.yml`
3. `datacheck.yaml`
4. `datacheck.yml`

---

## Environment Variables

Currently, DataCheck does not use environment variables for configuration.

---

## Examples

See the [Quick Start](../getting-started/quick-start.md) guide for comprehensive examples.
