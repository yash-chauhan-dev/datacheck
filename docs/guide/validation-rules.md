# Validation Rules

DataCheck supports these validation rules:

## not_null

Ensures the column has no missing values.

```yaml
checks:
  - name: required_field
    column: user_id
    rules:
      not_null: true
```

## unique

Ensures all values in the column are unique.

```yaml
checks:
  - name: unique_email
    column: email
    rules:
      unique: true
```

## min / max

Validates numeric values are within a range.

```yaml
checks:
  - name: age_validation
    column: age
    rules:
      min: 18
      max: 120
```

## regex

Validates strings match a regular expression pattern.

```yaml
checks:
  - name: email_format
    column: email
    rules:
      regex: "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"
```

Common patterns:
```yaml
# Email
regex: "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"

# Phone (US)
regex: "^\\d{3}-\\d{3}-\\d{4}$"

# Alphanumeric
regex: "^[a-zA-Z0-9]+$"

# URL
regex: "^https?://[\\w\\.-]+"
```

## allowed_values

Validates values are from a whitelist.

```yaml
checks:
  - name: status_check
    column: status
    rules:
      allowed_values: ["active", "inactive", "pending"]
```

## Combining Rules

You can combine multiple rules for the same column:

```yaml
checks:
  - name: user_id_validation
    column: user_id
    rules:
      not_null: true
      unique: true
      min: 1000
      max: 999999
```

## Multiple Checks

Validate multiple columns in one config:

```yaml
checks:
  - name: user_id_check
    column: user_id
    rules:
      not_null: true
      unique: true

  - name: email_check
    column: email
    rules:
      not_null: true
      regex: "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"

  - name: age_check
    column: age
    rules:
      min: 18
      max: 120

  - name: status_check
    column: status
    rules:
      allowed_values: ["active", "inactive"]
```
