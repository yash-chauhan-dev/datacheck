# Configuration Schema

Complete reference for DataCheck validation configuration.

## Basic Structure

```yaml
checks:
  - name: string           # Required: Check name
    column: string         # Required: Column to validate
    rules:                 # Required: Validation rules
      <rule_name>: <value>
```

---

## Check Object

Each check validates one column with one or more rules.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Descriptive name for the check |
| `column` | string | Column name to validate |
| `rules` | object | Validation rules to apply |

### Example

```yaml
checks:
  - name: user_id_validation
    column: user_id
    rules:
      not_null: true
      unique: true
```

---

## Validation Rules

### not_null

Ensures column has no missing values.

**Type:** `boolean`

**Example:**
```yaml
rules:
  not_null: true
```

**Checks:**
- No `NULL` values
- No `NaN` values
- No empty strings (for string columns)

---

### unique

Ensures all values are unique.

**Type:** `boolean`

**Example:**
```yaml
rules:
  unique: true
```

**Checks:**
- No duplicate values in column

**Use for:**
- Primary keys
- Email addresses
- Unique identifiers

---

### min

Validates numeric values are above minimum.

**Type:** `number`

**Example:**
```yaml
rules:
  min: 0
```

**Checks:**
- Value >= min

**Use for:**
- Age (min: 0)
- Price (min: 0.01)
- Quantity (min: 1)

---

### max

Validates numeric values are below maximum.

**Type:** `number`

**Example:**
```yaml
rules:
  max: 120
```

**Checks:**
- Value <= max

**Use for:**
- Age (max: 120)
- Percentage (max: 100)
- Stock quantity (max: 9999)

---

### regex

Validates strings match a pattern.

**Type:** `string` (regular expression)

**Example:**
```yaml
rules:
  regex: "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"
```

**Common Patterns:**

#### Email
```yaml
regex: "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"
```

#### Phone (US)
```yaml
regex: "^\\d{3}-\\d{3}-\\d{4}$"
```

#### Alphanumeric
```yaml
regex: "^[a-zA-Z0-9]+$"
```

#### URL
```yaml
regex: "^https?://[\\w\\.-]+"
```

#### Date (YYYY-MM-DD)
```yaml
regex: "^\\d{4}-\\d{2}-\\d{2}$"
```

#### Zip Code (US)
```yaml
regex: "^\\d{5}(-\\d{4})?$"
```

---

### allowed_values

Validates values are from a whitelist.

**Type:** `array` of strings

**Example:**
```yaml
rules:
  allowed_values: ["active", "inactive", "pending"]
```

**Use for:**
- Status fields
- Categories
- Enumerations
- Fixed sets of values

---

## Combining Rules

Multiple rules can be applied to the same column:

```yaml
checks:
  - name: user_id_validation
    column: user_id
    rules:
      not_null: true    # Must not be null
      unique: true      # Must be unique
      min: 1000         # Must be >= 1000
      max: 999999       # Must be <= 999999
```

**All rules must pass** for the check to succeed.

---

## Complete Example

```yaml
checks:
  # Primary key validation
  - name: user_id_check
    column: user_id
    rules:
      not_null: true
      unique: true
      min: 1

  # Email validation
  - name: email_validation
    column: email
    rules:
      not_null: true
      regex: "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"

  # Age range
  - name: age_validation
    column: age
    rules:
      not_null: true
      min: 18
      max: 120

  # Status whitelist
  - name: status_validation
    column: status
    rules:
      not_null: true
      allowed_values: ["active", "inactive", "pending"]

  # Price validation
  - name: price_validation
    column: price
    rules:
      not_null: true
      min: 0
      max: 1000000

  # Phone format
  - name: phone_validation
    column: phone
    rules:
      regex: "^\\d{3}-\\d{3}-\\d{4}$"

  # Quantity check
  - name: quantity_validation
    column: quantity
    rules:
      not_null: true
      min: 1
      max: 9999
```

---

## Config File Location

### Auto-discovery

Place `.datacheck.yaml` in working directory:
```
project/
├── .datacheck.yaml
└── data.csv
```

Run without `--config`:
```bash
datacheck validate data.csv
```

### Explicit Path

Specify config file:
```bash
datacheck validate data.csv --config validation/rules.yaml
```

### Multiple Configs

Organize by domain:
```
validation/
├── users.yaml
├── orders.yaml
└── products.yaml
```

Use specific config:
```bash
datacheck validate data/users.csv --config validation/users.yaml
```

---

## Validation Errors

### Invalid YAML

```yaml
checks:
  - name: test
    column: id
    rules:
      not_null true  # Missing colon
```

**Error:** Configuration error (exit code 2)

### Unknown Rule

```yaml
checks:
  - name: test
    column: id
    rules:
      unknown_rule: true  # Not a valid rule
```

**Error:** Configuration error (exit code 2)

### Missing Required Field

```yaml
checks:
  - name: test
    # Missing 'column' field
    rules:
      not_null: true
```

**Error:** Configuration error (exit code 2)

---

## Best Practices

### 1. Use Descriptive Names
```yaml
# Good
- name: user_email_format_validation
  column: email
  rules: {...}

# Avoid
- name: check1
  column: email
  rules: {...}
```

### 2. Group Related Checks
```yaml
# User validation
checks:
  - name: user_id
    column: id
    rules: {...}

  - name: user_email
    column: email
    rules: {...}

  - name: user_age
    column: age
    rules: {...}
```

### 3. Document Complex Patterns
```yaml
checks:
  # Validates UK postcodes (e.g., SW1A 1AA)
  - name: uk_postcode
    column: postcode
    rules:
      regex: "^[A-Z]{1,2}\\d{1,2}[A-Z]? \\d[A-Z]{2}$"
```

### 4. Start Simple
```yaml
# Start with basic checks
checks:
  - name: email
    column: email
    rules:
      not_null: true

# Add complexity as needed
checks:
  - name: email
    column: email
    rules:
      not_null: true
      regex: "^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$"
```
