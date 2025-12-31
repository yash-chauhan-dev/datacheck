# PyPI Release Guide

Step-by-step guide to publish DataCheck v0.1.0 to PyPI.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Pre-Release Checklist](#pre-release-checklist)
- [Publishing to PyPI](#publishing-to-pypi)
- [Post-Release Tasks](#post-release-tasks)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### 1. PyPI Account Setup

Create accounts on both Test PyPI and Production PyPI:

**Test PyPI** (for testing):
- Go to: https://test.pypi.org/account/register/
- Create an account
- Verify your email

**Production PyPI**:
- Go to: https://pypi.org/account/register/
- Create an account
- Verify your email

### 2. API Tokens

Generate API tokens for secure publishing:

#### Test PyPI Token:
1. Go to https://test.pypi.org/manage/account/token/
2. Click "Add API token"
3. Token name: `datacheck-test`
4. Scope: "Entire account" (for first release)
5. Copy the token (starts with `pypi-`)
6. Save it securely - you won't see it again!

#### Production PyPI Token:
1. Go to https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Token name: `datacheck`
4. Scope: "Entire account" (for first release)
5. Copy the token
6. Save it securely!

### 3. Configure Poetry

Store your tokens in Poetry:

```bash
# Configure Test PyPI
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi pypi-YOUR_TEST_TOKEN_HERE

# Configure Production PyPI
poetry config pypi-token.pypi pypi-YOUR_PRODUCTION_TOKEN_HERE
```

---

## Pre-Release Checklist

### 1. Verify Version Number

Check `pyproject.toml`:

```toml
[tool.poetry]
name = "datacheck"
version = "0.1.0"  # ✅ Correct for first release
```

### 2. Run All Tests

```bash
# Run full test suite
poetry run pytest

# Check coverage
poetry run pytest --cov=datacheck --cov-report=term

# Expected: 180 passed, 12 skipped, 92% coverage
```

### 3. Run Code Quality Checks

```bash
# Linting
poetry run ruff check datacheck/ tests/

# Type checking
poetry run mypy datacheck/

# Both should pass with no errors
```

### 4. Test the Package Locally

```bash
# Build the package
poetry build

# This creates:
# - dist/datacheck-0.1.0.tar.gz (source distribution)
# - dist/datacheck-0.1.0-py3-none-any.whl (wheel)

# Install locally to test
pip install dist/datacheck-0.1.0-py3-none-any.whl

# Test the CLI
datacheck version
# Output: DataCheck v0.1.0

# Run a validation
cd examples/basic
datacheck validate sample_data.csv --config validation_config.yaml

# Uninstall after testing
pip uninstall datacheck -y
```

### 5. Update Metadata (Optional but Recommended)

Edit `pyproject.toml` to add your information:

```toml
[tool.poetry]
authors = ["Your Name <your.email@example.com>"]

# Add more classifiers
classifiers = [
    "Development Status :: 4 - Beta",  # or "5 - Production/Stable"
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Quality Assurance",
    "Topic :: Software Development :: Testing",
    "Topic :: Database",
    "Environment :: Console",
    "Operating System :: OS Independent",
]

# Add project URLs
[tool.poetry.urls]
"Bug Tracker" = "https://github.com/yash-chauhan-dev/datacheck/issues"
"Changelog" = "https://github.com/yash-chauhan-dev/datacheck/blob/main/CHANGELOG.md"
"Documentation" = "https://github.com/yash-chauhan-dev/datacheck#readme"
```

### 6. Clean Build Artifacts

```bash
# Remove old builds
rm -rf dist/ build/ *.egg-info

# Rebuild fresh
poetry build
```

---

## Publishing to PyPI

### Step 1: Test on Test PyPI First

**Always test on Test PyPI before publishing to production!**

```bash
# Publish to Test PyPI
poetry publish -r testpypi

# You'll see:
# Publishing datacheck (0.1.0) to testpypi
# - Uploading datacheck-0.1.0.tar.gz 100%
# - Uploading datacheck-0.1.0-py3-none-any.whl 100%
```

### Step 2: Test Installation from Test PyPI

```bash
# Install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ datacheck

# The --extra-index-url is needed for dependencies (pandas, typer, etc.)

# Test it works
datacheck version

# Test validation
cd examples/basic
datacheck validate sample_data.csv --config validation_config.yaml

# Uninstall
pip uninstall datacheck -y
```

### Step 3: Publish to Production PyPI

Once everything works on Test PyPI:

```bash
# Publish to PyPI
poetry publish

# Confirm the upload (type 'yes')
# You'll see:
# Publishing datacheck (0.1.0) to PyPI
# - Uploading datacheck-0.1.0.tar.gz 100%
# - Uploading datacheck-0.1.0-py3-none-any.whl 100%
```

**🎉 Congratulations! Your package is now live on PyPI!**

### Step 4: Verify PyPI Listing

1. Go to: https://pypi.org/project/datacheck/
2. Check:
   - ✅ Version shows 0.1.0
   - ✅ Description renders correctly
   - ✅ Links work (homepage, repository)
   - ✅ Classifiers are correct
   - ✅ Dependencies listed

### Step 5: Test Installation from PyPI

```bash
# Install from PyPI (for real this time!)
pip install datacheck

# Test
datacheck version

# Run examples
cd examples/basic
datacheck validate sample_data.csv --config validation_config.yaml
```

---

## Post-Release Tasks

### 1. Create GitHub Release

```bash
# Tag the release
git tag -a v0.1.0 -m "Release v0.1.0 - Initial public release"

# Push the tag
git push origin v0.1.0
```

Then on GitHub:
1. Go to: https://github.com/yash-chauhan-dev/datacheck/releases
2. Click "Draft a new release"
3. Choose tag: `v0.1.0`
4. Release title: `v0.1.0 - Initial Release`
5. Description: Copy from `CHANGELOG.md`
6. Attach files:
   - `dist/datacheck-0.1.0.tar.gz`
   - `dist/datacheck-0.1.0-py3-none-any.whl`
7. Click "Publish release"

### 2. Announce the Release

Share your release:

- **Reddit**: r/Python, r/datascience, r/dataengineering
- **Twitter/X**: Tweet with #Python #DataEngineering #OpenSource
- **LinkedIn**: Post about your new open-source project
- **Dev.to**: Write a blog post about DataCheck
- **Hacker News**: Submit to Show HN

Example announcement:

```
🎉 DataCheck v0.1.0 is now available!

A lightweight CLI tool for data quality validation.

✨ Features:
- Validate CSV, Parquet, SQLite files
- 6 validation rules (not_null, min, max, unique, regex, allowed_values)
- Beautiful terminal output
- CI/CD ready with exit codes
- 92% test coverage

pip install datacheck

https://github.com/yash-chauhan-dev/datacheck
```

### 3. Update README Badges

Add PyPI badges to your README.md:

```markdown
[![PyPI version](https://badge.fury.io/py/datacheck.svg)](https://pypi.org/project/datacheck/)
[![Downloads](https://pepy.tech/badge/datacheck)](https://pepy.tech/project/datacheck)
[![Python Versions](https://img.shields.io/pypi/pyversions/datacheck.svg)](https://pypi.org/project/datacheck/)
```

### 4. Monitor Initial Usage

- Check PyPI download stats: https://pepy.tech/project/datacheck
- Watch for GitHub issues and stars
- Respond to early user feedback

---

## Troubleshooting

### Error: "File already exists"

If you get this error, you can't reupload the same version. You must:

1. Increment version in `pyproject.toml` (e.g., 0.1.1)
2. Rebuild: `poetry build`
3. Publish again: `poetry publish`

**Note**: You can't delete releases from PyPI, only "yank" them.

### Error: "Invalid credentials"

Your API token is wrong or expired:

```bash
# Reconfigure with correct token
poetry config pypi-token.pypi pypi-YOUR_NEW_TOKEN
```

### Error: "Package name already taken"

If `datacheck` is taken (unlikely, but possible):

1. Check: https://pypi.org/project/datacheck/
2. If taken, choose a different name (e.g., `datacheck-cli`)
3. Update `pyproject.toml`:
   ```toml
   name = "datacheck-cli"
   ```

### Build Warnings

If you see warnings during `poetry build`:

- Check pyproject.toml syntax
- Ensure README.md exists and is valid
- Ensure LICENSE file exists

### Import Errors After Install

If users report import errors:

- Check that `datacheck/` has `__init__.py`
- Verify package structure is correct
- Test local installation from wheel

---

## Quick Reference

### Complete Release Process (TL;DR)

```bash
# 1. Pre-release checks
poetry run pytest                    # All tests pass
poetry run ruff check datacheck/     # No lint errors
poetry run mypy datacheck/           # No type errors

# 2. Build
rm -rf dist/
poetry build

# 3. Test locally
pip install dist/*.whl
datacheck version
pip uninstall datacheck -y

# 4. Test on Test PyPI
poetry publish -r testpypi
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ datacheck
datacheck version
pip uninstall datacheck -y

# 5. Publish to PyPI
poetry publish

# 6. Create GitHub release
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0

# 7. Test installation from PyPI
pip install datacheck
datacheck version

# 8. Celebrate! 🎉
```

---

## Next Steps

After v0.1.0 is released:

1. **Monitor feedback**: Watch GitHub issues and discussions
2. **Plan v0.2.0**: Implement features from the roadmap
3. **Update dependencies**: Keep dependencies up to date with Dependabot
4. **Improve documentation**: Based on user questions
5. **Add more examples**: Real-world use cases from the community

---

## Resources

- **PyPI**: https://pypi.org/
- **Test PyPI**: https://test.pypi.org/
- **Poetry Publishing Docs**: https://python-poetry.org/docs/libraries/#publishing-to-pypi
- **PyPI Classifiers**: https://pypi.org/classifiers/
- **Semantic Versioning**: https://semver.org/

---

**Good luck with your release! 🚀**

For questions, open an issue: https://github.com/yash-chauhan-dev/datacheck/issues
