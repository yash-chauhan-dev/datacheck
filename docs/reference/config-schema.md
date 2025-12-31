# Configuration Schema Reference

YAML configuration file schema for DataCheck.

---

## Root Schema

```yaml
checks:
  - name: <string>        # Required
    column: <string>      # Required
    rules:                # Required
      <rule>: <value>
```

---

## Check Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique name for this check |
| `column` | string | Yes | Column name to validate |
| `rules` | object | Yes | Validation rules to apply |

---

## Rules Object

| Rule | Type | Description |
|------|------|-------------|
| `not_null` | boolean | Check for missing values |
| `unique` | boolean | Check for duplicates |
| `min` | number | Minimum value (inclusive) |
| `max` | number | Maximum value (inclusive) |
| `regex` | string | Regular expression pattern |
| `allowed_values` | array | List of allowed values |

---

## Example

```yaml
checks:
  - name: email_validation
    column: email
    rules:
      not_null: true
      unique: true
      regex: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
```

---

See [Configuration](../user-guide/configuration.md) for detailed guide.
