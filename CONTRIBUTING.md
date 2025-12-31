# Contributing to DataCheck

Thank you for your interest in contributing to DataCheck! This document provides guidelines and instructions for contributing.

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to hello@datacheck.com.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (sample data files, configuration files)
- **Describe the behavior you observed** and what you expected to see
- **Include screenshots** if relevant
- **Include your environment details** (OS, Python version, DataCheck version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Provide examples** of how the enhancement would be used
- **Explain why this enhancement would be useful**

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Run linting (`ruff check datacheck tests`)
6. Run type checking (`mypy datacheck`)
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Poetry 1.6+
- Git

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/datacheck.git
cd datacheck

# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Install pre-commit hooks
pre-commit install

# Run tests to verify setup
pytest
```

### Development Workflow

1. **Create a branch** for your work:
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Make your changes** following the code style guidelines

3. **Write tests** for your changes

4. **Run the test suite**:
   ```bash
   pytest
   ```

5. **Check code coverage**:
   ```bash
   pytest --cov=datacheck --cov-report=term-missing
   ```

6. **Run linting**:
   ```bash
   ruff check datacheck tests
   ```

7. **Run type checking**:
   ```bash
   mypy datacheck
   ```

8. **Format code**:
   ```bash
   ruff format datacheck tests
   ```

9. **Commit your changes** using conventional commits:
   ```bash
   git commit -m "feat: add new validation rule"
   ```

10. **Push to your fork** and create a Pull Request

## Code Style Guidelines

### Python Style

- Follow PEP 8
- Use type hints for all function signatures
- Maximum line length: 100 characters
- Use docstrings for all public functions and classes

### Docstring Format

```python
def my_function(arg1: str, arg2: int) -> bool:
    """Short description of the function.

    Longer description if needed, explaining the purpose and behavior
    in more detail.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Description of return value

    Raises:
        ValueError: When and why this is raised
        TypeError: When and why this is raised

    Example:
        >>> my_function("test", 42)
        True
    """
    pass
```

### Commit Message Format

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(rules): add support for custom regex patterns
fix(loader): handle missing CSV headers correctly
docs(readme): update installation instructions
test(engine): add integration tests for validation workflow
```

## Testing Guidelines

### Writing Tests

- Write tests for all new features
- Update tests when changing existing functionality
- Aim for 90%+ code coverage
- Use descriptive test names
- Follow the Arrange-Act-Assert pattern

### Test Structure

```python
def test_feature_description():
    """Test that feature behaves correctly in specific scenario."""
    # Arrange - Set up test data and conditions
    data = create_test_data()

    # Act - Execute the function being tested
    result = function_under_test(data)

    # Assert - Verify the results
    assert result.is_valid
    assert len(result.failures) == 0
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_rules.py

# Run specific test
pytest tests/test_rules.py::test_not_null_rule

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=datacheck --cov-report=html
```

## Project Structure

```
datacheck/
├── datacheck/           # Main package
│   ├── __init__.py     # Package initialization
│   ├── cli.py          # CLI implementation
│   ├── config.py       # Configuration parsing
│   ├── loader.py       # Data loaders
│   ├── rules.py        # Validation rules
│   ├── engine.py       # Validation engine
│   ├── results.py      # Result models
│   ├── output.py       # Output formatting
│   └── exceptions.py   # Custom exceptions
├── tests/              # Test suite
│   ├── conftest.py     # Pytest fixtures
│   ├── test_*.py       # Test files
│   └── fixtures/       # Test data files
├── examples/           # Example files
└── docs/               # Documentation
```

## Documentation

- Update documentation when adding new features
- Include examples in docstrings
- Update README.md for user-facing changes
- Add entries to CHANGELOG.md

## Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create a new tag: `git tag v0.1.0`
4. Push tag: `git push origin v0.1.0`
5. GitHub Actions will automatically build and publish to PyPI

## Questions?

If you have questions, please:
1. Check existing issues and discussions
2. Create a new issue with the `question` label
3. Reach out to maintainers at hello@datacheck.com

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
