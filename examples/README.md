# DataCheck Examples

This directory contains comprehensive examples demonstrating how to use DataCheck for data quality validation.

## Quick Start

```bash
# Navigate to an example directory
cd examples/basic

# Run validation
datacheck validate sample_data.csv --config validation_config.yaml
```

## Example Categories

### 📁 [Basic](./basic/)
**Difficulty**: Beginner
**Topics**: Simple validation rules, getting started

Learn the fundamentals:
- Not null validations
- Min/max constraints
- Regex patterns
- Basic data types

**Files**:
- `sample_data.csv` - Clean employee data
- `validation_config.yaml` - Basic validation rules
- `README.md` - Detailed walkthrough

**Best for**: First-time users, learning DataCheck basics

---

### 📁 [Advanced](./advanced/)
**Difficulty**: Intermediate
**Topics**: Complex validation, uniqueness, allowed values

Master advanced features:
- Unique constraints
- Complex regex patterns
- Allowed values validation
- Multiple rule combinations

**Files**:
- `customer_data.csv` - Valid customer data
- `customer_data_with_errors.csv` - Data with intentional errors
- `validation_config.yaml` - Advanced validation rules
- `README.md` - Feature explanations

**Best for**: Understanding all validation features, real-world scenarios

---

### 📁 [Real-World](./real-world/)
**Difficulty**: Production-ready
**Topics**: CI/CD integration, automation, best practices

Production use cases:
- E-commerce sales validation
- User account validation
- CI/CD pipeline integration
- Automation scripts

**Files**:
- `sales_data.csv` + `sales_validation.yaml` - Sales data example
- `user_data.csv` + `user_validation.yaml` - User data example
- `README.md` - Integration patterns and best practices

**Best for**: Production deployments, automation, DevOps

---

### 📁 [Parquet Example](./parquet-example/)
**Difficulty**: Beginner
**Topics**: Parquet files, columnar storage, type safety

Validate Parquet format data:
- Efficient columnar storage format
- Type-safe data validation
- Big data ready
- Same validation rules as CSV

**Files**:
- `product_inventory.parquet` - Product inventory data in Parquet format
- `validation_config.yaml` - Inventory validation rules
- `README.md` - Parquet format guide

**Best for**: Data engineering pipelines, big data workflows, type-safe validation

---

### 📁 [Database Example](./database-example/)
**Difficulty**: Intermediate
**Topics**: SQLite databases, SQL queries, Python API

Validate data directly from databases:
- SQLite database validation
- Custom SQL query support
- Python API integration
- No data export required

**Files**:
- `orders.db` - SQLite database with orders table
- `validation_config.yaml` - Order validation rules
- `validate_orders.py` - Python validation script
- `README.md` - Database validation guide

**Best for**: Application databases, data warehouses, Python integration

---

## Learning Path

### 1. Start with Basic
```bash
cd basic
datacheck validate sample_data.csv --config validation_config.yaml
```
Learn fundamental validation rules and CLI usage.

### 2. Explore Advanced
```bash
cd advanced
# Validate clean data
datacheck validate customer_data.csv --config validation_config.yaml

# See validation failures
datacheck validate customer_data_with_errors.csv --config validation_config.yaml
```
Understand complex validation scenarios and error handling.

### 3. Apply Real-World
```bash
cd real-world
# Sales data
datacheck validate sales_data.csv --config sales_validation.yaml --format json

# User data
datacheck validate user_data.csv --config user_validation.yaml
```
Learn integration patterns and production best practices.

### 4. Try Parquet Format
```bash
cd parquet-example
datacheck validate product_inventory.parquet --config validation_config.yaml
```
Learn how to validate columnar data formats efficiently.

### 5. Explore Database Validation
```bash
cd database-example
poetry run python validate_orders.py
```
Learn how to validate database tables using the Python API.

---

## Common Commands

### Basic Validation
```bash
datacheck validate <file.csv> --config <config.yaml>
```

### JSON Output
```bash
datacheck validate <file.csv> --config <config.yaml> --format json
```

### Save Results to File
```bash
datacheck validate <file.csv> --config <config.yaml> \
  --format json --json-output results.json
```

### Auto-discover Configuration
```bash
# If .datacheck.yaml exists in current directory
datacheck validate data.csv
```

---

## Exit Codes

DataCheck uses exit codes for script automation:

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | All checks passed ✓ | Proceed with data processing |
| 1 | Some checks failed | Review and fix data quality issues |
| 2 | Configuration error | Fix validation config file |
| 3 | Data loading error | Check file path and format |
| 4 | Unexpected error | Check logs and file bug report |

### Usage in Scripts
```bash
datacheck validate data.csv --config config.yaml

if [ $? -eq 0 ]; then
  echo "✓ Data validation passed"
  # Continue with processing
  python load_data.py
else
  echo "✗ Data validation failed"
  exit 1
fi
```

---

## Creating Your Own Examples

### Step 1: Create Sample Data
```csv
name,age,email
Alice,30,alice@example.com
Bob,25,bob@example.com
```

### Step 2: Create Validation Config
```yaml
checks:
  - name: age_check
    column: age
    rules:
      not_null: true
      min: 18
      max: 120
```

### Step 3: Test Validation
```bash
datacheck validate data.csv --config config.yaml
```

### Step 4: Iterate and Refine
Add more rules, test edge cases, document your configuration.

---

## Validation Rules Reference

### Data Presence
- `not_null: true` - No missing values
- `unique: true` - All values must be unique

### Numeric Ranges
- `min: <number>` - Minimum value (inclusive)
- `max: <number>` - Maximum value (inclusive)

### String Validation
- `min_length: <int>` - Minimum string length
- `max_length: <int>` - Maximum string length
- `regex: "<pattern>"` - Match regex pattern

### Value Constraints
- `allowed_values: [...]` - Value must be in list
- `dtype: "<type>"` - Check data type

### Example Configuration
```yaml
checks:
  - name: comprehensive_validation
    column: example_column
    rules:
      not_null: true              # Required
      unique: true                 # Unique values
      min: 0                       # Numeric minimum
      max: 100                     # Numeric maximum
      min_length: 1                # String minimum length
      max_length: 50               # String maximum length
      regex: "^[A-Z].*"           # Starts with uppercase
      allowed_values: ["A", "B"]   # Must be A or B
      dtype: "str"                 # Must be string type
```

---

## Tips and Tricks

### 1. Start Simple
Begin with basic rules (not_null, min, max) and add complexity gradually.

### 2. Test with Bad Data
Always test your validation config with intentionally invalid data to ensure rules work correctly.

### 3. Document Your Rules
Add comments to your YAML config explaining why each rule exists:
```yaml
checks:
  - name: user_age
    column: age
    rules:
      min: 13  # COPPA compliance - users must be 13+
      max: 120  # Reasonable maximum age
```

### 4. Use Descriptive Check Names
Good: `customer_email_format_validation`
Bad: `check1`

### 5. Version Your Configs
Keep validation configs in git alongside your data schemas.

### 6. Automate in CI/CD
Add validation to your CI/CD pipeline:
```yaml
# .github/workflows/validate.yml
- name: Validate Data
  run: datacheck validate data/*.csv --config validation/rules.yaml
```

### 7. Monitor Validation Results
Track validation failure rates over time to identify data quality trends.

---

## Getting Help

- **Documentation**: See main [README.md](../README.md)
- **Issues**: Report bugs on [GitHub Issues](https://github.com/yash-chauhan-dev/datacheck/issues)
- **Examples Not Working?**: Ensure you've installed DataCheck:
  ```bash
  pip install -e .
  # or
  poetry install
  ```

---

## Contributing Examples

Have a useful example? Contributions are welcome!

1. Create your example in a new directory
2. Include sample data and configuration
3. Add a README explaining the use case
4. Test thoroughly
5. Submit a pull request

---

## Next Steps

After exploring the examples:

1. **Read the Documentation**: Full docs in main [README.md](../README.md)
2. **Run Tests**: See [tests/](../tests/) for testing best practices
3. **Start Validating**: Apply DataCheck to your own data!

**Happy Validating!** 🎉
