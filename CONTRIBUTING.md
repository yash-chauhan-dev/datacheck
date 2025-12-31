# Contributing to DataCheck

Thank you for your interest in contributing to DataCheck! This guide will help you get started.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Adding Features](#adding-features)

---

## Code of Conduct

Be respectful, inclusive, and professional. We're all here to build better tools together.

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Poetry (for dependency management)
- Git

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/yash-chauhan-dev/datacheck.git
cd datacheck

# Install dependencies
poetry install

# Install pre-commit hooks
poetry run pre-commit install

# Run tests to verify setup
poetry run pytest
```

---

## Development Setup

### Install Development Dependencies

```bash
poetry install --with dev
```

This installs:
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `mypy` - Type checking
- `ruff` - Linting and formatting
- `pre-commit` - Git hooks

### IDE Setup

**VS Code** (recommended `.vscode/settings.json`):
```json
{
  "python.linting.enabled": true,
  "python.linting.mypyEnabled": true,
  "python.formatting.provider": "none",
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  },
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false
}
```

**PyCharm**:
- Enable mypy plugin
- Set ruff as the formatter
- Configure pytest as the test runner

---

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

Branch naming:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test improvements

### 2. Make Changes

Write your code following our [coding standards](#coding-standards).

### 3. Test Your Changes

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=datacheck --cov-report=html

# Run specific tests
poetry run pytest tests/test_cli.py -v

# Run type checking
poetry run mypy datacheck/

# Run linting
poetry run ruff check datacheck/ tests/
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: add custom rule support"
```

Commit message format:
```
<type>: <description>

[optional body]

[optional footer]
```

Types:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `test` - Tests
- `refactor` - Code refactoring
- `chore` - Maintenance

Examples:
```
feat: add min_length validation rule
fix: handle empty CSV files correctly
docs: update configuration guide
test: add tests for unique constraint
```

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

---

## Coding Standards

### Python Style

We follow:
- **PEP 8** for code style
- **PEP 257** for docstrings
- **Type hints** for all functions

### Code Formatting

```bash
# Auto-format code
poetry run ruff format datacheck/ tests/

# Check formatting
poetry run ruff check datacheck/ tests/
```

### Type Checking

All code must pass mypy:

```bash
poetry run mypy datacheck/
```

### Docstrings

Use Google-style docstrings:

```python
def validate_data(df: pd.DataFrame, rules: dict[str, Any]) -> ValidationSummary:
    """Validate DataFrame against rules.

    Args:
        df: DataFrame to validate
        rules: Dictionary of validation rules

    Returns:
        Validation summary with results

    Raises:
        ValidationError: If validation configuration is invalid

    Example:
        >>> rules = {"not_null": True, "min": 0}
        >>> result = validate_data(df, rules)
        >>> assert result.all_passed
    """
    pass
```

### Code Organization

```python
# 1. Imports (grouped and sorted)
from pathlib import Path
from typing import Any

import pandas as pd

from datacheck.exceptions import ValidationError
from datacheck.results import ValidationSummary

# 2. Constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3

# 3. Classes
class MyClass:
    """Class docstring."""
    pass

# 4. Functions
def my_function() -> None:
    """Function docstring."""
    pass
```

---

## Testing

### Test Structure

```
tests/
├── conftest.py          # Shared fixtures
├── helpers.py           # Test utilities
├── test_cli.py         # CLI tests
├── test_rules.py       # Rule tests
└── ...
```

### Writing Tests

```python
import pytest
from datacheck.rules import NotNullRule

@pytest.mark.unit
class TestNotNullRule:
    """Tests for NotNullRule."""

    def test_passes_with_no_nulls(self, sample_dataframe):
        """Test rule passes when no nulls present."""
        # Arrange
        rule = NotNullRule(column="age")

        # Act
        result = rule.validate(sample_dataframe)

        # Assert
        assert result.passed
        assert result.failed_rows == 0

    def test_fails_with_nulls(self, dataframe_with_nulls):
        """Test rule fails when nulls present."""
        rule = NotNullRule(column="age")
        result = rule.validate(dataframe_with_nulls)

        assert not result.passed
        assert result.failed_rows > 0
```

### Test Markers

Use markers to categorize tests:

```python
@pytest.mark.unit         # Unit test
@pytest.mark.integration  # Integration test
@pytest.mark.slow         # Slow test
@pytest.mark.cli          # CLI test
```

Run specific categories:
```bash
poetry run pytest -m unit
poetry run pytest -m "not slow"
```

### Coverage Requirements

- Minimum coverage: **70%**
- Aim for: **90%+**
- Check coverage:
  ```bash
  poetry run pytest --cov=datacheck --cov-report=html
  open htmlcov/index.html
  ```

---

## Submitting Changes

### Pull Request Process

1. **Update Documentation**
   - Update README.md if adding features
   - Add docstrings to new functions
   - Update examples if needed

2. **Ensure Tests Pass**
   ```bash
   poetry run pytest
   poetry run mypy datacheck/
   poetry run ruff check datacheck/ tests/
   ```

3. **Update CHANGELOG** (if applicable)

4. **Create Pull Request**
   - Clear title describing the change
   - Description explaining what and why
   - Link to related issues

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Updated documentation

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Commented complex code
- [ ] Updated documentation
- [ ] No new warnings
```

### Version Bumping (For Releases)

If your PR includes user-facing changes (new features, bug fixes, breaking changes), please bump the version:

**Bump version using Poetry:**
```bash
# For bug fixes (0.1.0 → 0.1.1)
poetry version patch

# For new features (0.1.0 → 0.2.0)
poetry version minor

# For breaking changes (0.1.0 → 1.0.0)
poetry version major
```

**Update CHANGELOG.md:**
Add a new section at the top describing your changes:
```markdown
## [0.2.0] - 2025-01-XX

### Added
- Your new feature

### Fixed
- Your bug fix
```

**Note**: PRs without version bumps are fine for:
- Documentation updates
- Test improvements
- Internal refactoring
- CI/CD changes

The PR check will remind you if a version bump might be needed, but won't block your PR.

### Code Review

- Be open to feedback
- Respond to comments promptly
- Make requested changes
- Keep discussions professional

---

## Adding Features

### Adding a New Validation Rule

1. **Create rule class** in `datacheck/rules.py`:

```python
class MyNewRule(Rule):
    """Validates something specific.

    Args:
        column: Column name to validate
        threshold: Rule-specific parameter
    """

    def __init__(self, column: str, threshold: int) -> None:
        super().__init__(column)
        self.threshold = threshold

    def validate(self, df: pd.DataFrame) -> RuleResult:
        """Execute validation rule.

        Args:
            df: DataFrame to validate

        Returns:
            Rule result with pass/fail status
        """
        # Implementation here
        pass

    def description(self) -> str:
        """Get human-readable description."""
        return f"Values must meet threshold {self.threshold}"
```

2. **Register in RuleFactory** (`datacheck/rules.py`):

```python
class RuleFactory:
    @staticmethod
    def create_rule(rule_name: str, column: str, value: Any) -> Rule:
        if rule_name == "my_new_rule":
            return MyNewRule(column=column, threshold=value)
        # ... existing rules
```

3. **Add tests** (`tests/test_rules.py`):

```python
class TestMyNewRule:
    def test_passes_when_valid(self):
        # Test implementation
        pass

    def test_fails_when_invalid(self):
        # Test implementation
        pass
```

4. **Update documentation**:
   - Add to README.md
   - Add example to examples/
   - Update validation rules reference

### Adding a New Data Loader

1. **Create loader class** in `datacheck/loader.py`:

```python
class MyFormatLoader(DataLoader):
    """Loads data from MyFormat files."""

    def load(self) -> pd.DataFrame:
        """Load data into DataFrame."""
        # Implementation
        pass
```

2. **Register in LoaderFactory**

3. **Add tests**

4. **Update documentation**

---

## Project Structure

```
datacheck/
├── datacheck/
│   ├── __init__.py
│   ├── cli.py          # CLI interface
│   ├── config.py       # Configuration
│   ├── engine.py       # Validation engine
│   ├── loader.py       # Data loaders
│   ├── rules.py        # Validation rules
│   ├── results.py      # Result models
│   ├── output.py       # Output formatting
│   └── exceptions.py   # Custom exceptions
├── tests/
│   ├── conftest.py     # Test fixtures
│   ├── helpers.py      # Test utilities
│   └── test_*.py       # Test files
├── examples/           # Example files
├── docs/              # Documentation
├── pyproject.toml     # Project configuration
└── README.md          # Main documentation
```

---

## Release Process

(For maintainers)

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create git tag: `git tag -a v0.2.0 -m "Release v0.2.0"`
4. Push tag: `git push origin v0.2.0`
5. GitHub Actions will build and publish to PyPI

---

## Getting Help

- **Questions**: Open a [Discussion](https://github.com/yash-chauhan-dev/datacheck/discussions)
- **Bugs**: Open an [Issue](https://github.com/yash-chauhan-dev/datacheck/issues)
- **Feature Requests**: Open an [Issue](https://github.com/yash-chauhan-dev/datacheck/issues) with `enhancement` label

---

## Recognition

Contributors will be:
- Listed in README.md
- Mentioned in release notes
- Given credit in commit messages

Thank you for contributing to DataCheck! 🎉
