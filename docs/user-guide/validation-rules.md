# Validation Rules Reference

Complete reference for all available validation rules in DataCheck.

---

## Rule Types

DataCheck provides 5 types of validation rules:

| Rule | Purpose | Data Types |
|------|---------|------------|
| `not_null` | Check for missing values | All |
| `unique` | Detect duplicates | All |
| `min` / `max` | Range validation | Numeric |
| `regex` | Pattern matching | String |
| `allowed_values` | Whitelist validation | All |

---

## not_null

Ensures no missing or null values in the column.

**Syntax**:
```yaml
rules:
  not_null: true
```

**Example**:
```yaml
checks:
  - name: required_email
    column: email
    rules:
      not_null: true
```

**Fails when**: Column contains `NULL`, `None`, `NaN`, or empty strings

---

## unique

Ensures all values in the column are unique (no duplicates).

**Syntax**:
```yaml
rules:
  unique: true
```

**Example**:
```yaml
checks:
  - name: unique_customer_id
    column: customer_id
    rules:
      unique: true
```

**Fails when**: Any value appears more than once

---

## min / max

Validates numeric values fall within a specified range (inclusive).

**Syntax**:
```yaml
rules:
  min: <number>
  max: <number>
```

**Example**:
```yaml
checks:
  - name: age_range
    column: age
    rules:
      min: 18
      max: 120
```

**Fails when**: Value < min or value > max

**Use Cases**:
- Age validation
- Price ranges
- Quantity limits
- Temperature readings

---

## regex

Validates string values match a regular expression pattern.

**Syntax**:
```yaml
rules:
  regex: "<pattern>"
```

**Common Patterns**:

### Email
```yaml
rules:
  regex: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
```

### Phone (US)
```yaml
rules:
  regex: "^\\+1-[0-9]{3}-[0-9]{4}$"
```

### UUID
```yaml
rules:
  regex: "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
```

### ISO Date
```yaml
rules:
  regex: "^\\d{4}-\\d{2}-\\d{2}$"
```

### SKU/Product Code
```yaml
rules:
  regex: "^SKU[0-9]{6}$"
```

**Fails when**: String doesn't match pattern

---

## allowed_values

Restricts column values to a specific list (whitelist).

**Syntax**:
```yaml
rules:
  allowed_values: [value1, value2, value3]
```

**Example**:
```yaml
checks:
  - name: status_validation
    column: status
    rules:
      allowed_values: ["active", "inactive", "suspended"]
```

**Fails when**: Value not in the allowed list

**Use Cases**:
- Status/state validation
- Category validation
- Enum validation
- Country codes

---

## Combining Rules

Multiple rules can be applied to a single column:

```yaml
checks:
  - name: comprehensive_validation
    column: user_age
    rules:
      not_null: true      # Required
      unique: false       # Duplicates allowed
      min: 13            # COPPA compliance
      max: 120           # Reasonable max
```

**All rules must pass** for the check to succeed.

---

## Rule Execution Order

Rules are evaluated in this order:

1. `not_null` - Checked first
2. `unique` - Checked second
3. `min` / `max` - Checked third
4. `regex` - Checked fourth
5. `allowed_values` - Checked last

**Note**: If a row fails an earlier rule, it may still be checked by later rules.

---

## Examples by Use Case

### User Registration
```yaml
checks:
  - name: username_validation
    column: username
    rules:
      not_null: true
      unique: true
      regex: "^[a-zA-Z0-9_]{3,20}$"

  - name: email_validation
    column: email
    rules:
      not_null: true
      unique: true
      regex: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"

  - name: age_validation
    column: age
    rules:
      not_null: true
      min: 18
```

### E-commerce Orders
```yaml
checks:
  - name: order_id_validation
    column: order_id
    rules:
      not_null: true
      unique: true
      regex: "^ORD[0-9]{10}$"

  - name: quantity_validation
    column: quantity
    rules:
      not_null: true
      min: 1
      max: 1000

  - name: status_validation
    column: status
    rules:
      allowed_values: ["pending", "processing", "shipped", "delivered", "cancelled"]
```

### Financial Data
```yaml
checks:
  - name: transaction_amount
    column: amount
    rules:
      not_null: true
      min: 0.01

  - name: currency_code
    column: currency
    rules:
      not_null: true
      allowed_values: ["USD", "EUR", "GBP", "JPY"]

  - name: account_number
    column: account
    rules:
      not_null: true
      unique: true
      regex: "^[0-9]{10,12}$"
```

---

## Best Practices

1. **Start simple** - Begin with `not_null` and add more rules as needed
2. **Use descriptive names** - Name checks clearly (e.g., "email_format_check")
3. **Test regex patterns** - Verify patterns work before deployment
4. **Document rules** - Add comments in YAML explaining complex rules
5. **Version control** - Keep validation configs in git

---

## Next Steps

- Learn about [Configuration](configuration.md) file structure
- See [Examples](../examples/real-world.md) of real-world validations
- Understand [Output Formats](output-formats.md)
