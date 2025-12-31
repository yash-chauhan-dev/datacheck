# Development Setup

Guide for contributors to set up a development environment.

---

## Prerequisites

- Python 3.10 or higher
- Poetry
- Git

---

## Setup Steps

```bash
# Clone repository
git clone https://github.com/yash-chauhan-dev/datacheck.git
cd datacheck

# Install dependencies
poetry install

# Install pre-commit hooks
poetry run pre-commit install

# Run tests
poetry run pytest

# Run type checking
poetry run mypy datacheck/

# Run linting
poetry run ruff check datacheck/ tests/
```

---

## Development Workflow

1. Create feature branch
2. Make changes
3. Add tests
4. Run quality checks
5. Commit and push
6. Create pull request

---

## Running Tests

```bash
# All tests
poetry run pytest

# With coverage
poetry run pytest --cov=datacheck --cov-report=html

# Specific tests
poetry run pytest tests/test_rules.py
```

---

## Code Quality

```bash
# Type checking
poetry run mypy datacheck/

# Linting
poetry run ruff check datacheck/ tests/

# Format code
poetry run ruff format datacheck/ tests/
```

---

For complete guidelines, see [CONTRIBUTING.md](https://github.com/yash-chauhan-dev/datacheck/blob/main/CONTRIBUTING.md).
