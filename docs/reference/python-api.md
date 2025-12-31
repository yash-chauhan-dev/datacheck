# Python API Reference

Complete reference for using DataCheck programmatically.

---

## Core Classes

### ValidationEngine

Main class for running validations.

```python
from datacheck.engine import ValidationEngine

engine = ValidationEngine(config_path="validation.yaml")
summary = engine.validate(df=dataframe)
```

---

### LoaderFactory

Factory for loading data from different sources.

```python
from datacheck.loader import LoaderFactory

# Load CSV
df = LoaderFactory.load("data.csv")

# Load Parquet
df = LoaderFactory.load("data.parquet")

# Load database
df = LoaderFactory.load("data.db", table_name="customers")
```

---

### ValidationConfig

Configuration object for validation rules.

```python
from datacheck.config import ValidationConfig

config = ValidationConfig.from_file("validation.yaml")
```

---

## Example

See [Python Integration](../integration/python.md) for complete examples.

---

## API Documentation

Full API documentation is available in the repository's docstrings.

Run `python -m pydoc datacheck` for module documentation.
