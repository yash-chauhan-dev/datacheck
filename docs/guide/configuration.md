# Configuration

## Basic Structure

```yaml
checks:
  - name: check_name        # Descriptive name for this check
    column: column_name     # Column to validate
    rules:                  # Validation rules
      not_null: true
      min: 0
```

## Auto-discovery

Place a `.datacheck.yaml` file in your working directory:

```bash
# DataCheck will automatically find and use it
datacheck validate data.csv
```

## Explicit Config

Specify a config file:

```bash
datacheck validate data.csv --config rules.yaml
```

## Multiple Config Files

Organize rules by domain:

```
project/
├── rules/
│   ├── users.yaml
│   ├── orders.yaml
│   └── products.yaml
└── data/
    ├── users.csv
    ├── orders.csv
    └── products.csv
```

Validate each:
```bash
datacheck validate data/users.csv --config rules/users.yaml
datacheck validate data/orders.csv --config rules/orders.yaml
```

## Environment-specific Rules

```bash
# Development: relaxed rules
datacheck validate data.csv --config rules/dev.yaml

# Production: strict rules
datacheck validate data.csv --config rules/prod.yaml
```

## Complete Example

```yaml
# Complete validation config with all rule types
checks:
  # Required unique identifier
  - name: user_id_validation
    column: user_id
    rules:
      not_null: true
      unique: true
      min: 1

  # Email format
  - name: email_validation
    column: email
    rules:
      not_null: true
      regex: "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"

  # Age range
  - name: age_validation
    column: age
    rules:
      min: 18
      max: 120

  # Status whitelist
  - name: status_validation
    column: status
    rules:
      not_null: true
      allowed_values: ["active", "inactive", "pending"]

  # Price range
  - name: price_validation
    column: price
    rules:
      not_null: true
      min: 0
      max: 1000000
```

## Best Practices

### 1. Use Descriptive Names
```yaml
# ✅ Good
- name: user_email_format_check

# ❌ Avoid
- name: check1
```

### 2. Group Related Checks
```yaml
# User data validation
checks:
  - name: user_id_check
    column: user_id
    rules: {...}

  - name: user_email_check
    column: email
    rules: {...}

  - name: user_age_check
    column: age
    rules: {...}
```

### 3. Document Complex Patterns
```yaml
checks:
  # Validates US phone numbers in format: XXX-XXX-XXXX
  - name: phone_format
    column: phone
    rules:
      regex: "^\\d{3}-\\d{3}-\\d{4}$"
```

### 4. Start Simple, Add Rules as Needed
```yaml
# Start with basics
checks:
  - name: email_check
    column: email
    rules:
      not_null: true

# Add format validation later
checks:
  - name: email_check
    column: email
    rules:
      not_null: true
      regex: "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"  # Added
```
