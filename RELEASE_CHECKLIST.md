# Release Checklist for v0.1.0

Use this checklist to track your release progress.

## Pre-Release (Complete Before Publishing)

### Code Quality
- [ ] All tests passing (`poetry run pytest`)
- [ ] Coverage ≥ 92% (`poetry run pytest --cov`)
- [ ] No lint errors (`poetry run ruff check datacheck/ tests/`)
- [ ] No type errors (`poetry run mypy datacheck/`)
- [ ] All examples tested and working

### Documentation
- [ ] README.md is up to date
- [ ] CHANGELOG.md has v0.1.0 entry
- [ ] CONTRIBUTING.md is accurate
- [ ] All example README files are correct
- [ ] Docstrings are complete

### Package Metadata
- [ ] Version is 0.1.0 in `pyproject.toml`
- [ ] Author information is correct
- [ ] Repository URL is correct
- [ ] Keywords are appropriate
- [ ] Classifiers are accurate
- [ ] README.md renders correctly as long description

### GitHub Setup
- [ ] LICENSE file is present (MIT, 2025)
- [ ] .gitignore is configured
- [ ] Issue templates created
- [ ] PR template created
- [ ] Dependabot configured
- [ ] CI/CD passing on all platforms
- [ ] Branch protection enabled on `main`

### Build & Test Locally
- [ ] Clean dist: `rm -rf dist/`
- [ ] Build package: `poetry build`
- [ ] Install from wheel: `pip install dist/*.whl`
- [ ] CLI works: `datacheck version`
- [ ] Run example: `datacheck validate examples/basic/sample_data.csv --config examples/basic/validation_config.yaml`
- [ ] Uninstall: `pip uninstall datacheck -y`

---

## PyPI Account Setup

### Test PyPI
- [ ] Created account at https://test.pypi.org
- [ ] Email verified
- [ ] Generated API token
- [ ] Configured in Poetry: `poetry config pypi-token.testpypi pypi-YOUR_TOKEN`

### Production PyPI
- [ ] Created account at https://pypi.org
- [ ] Email verified
- [ ] Generated API token
- [ ] Configured in Poetry: `poetry config pypi-token.pypi pypi-YOUR_TOKEN`

---

## Test PyPI Release

- [ ] Publish to Test PyPI: `poetry publish -r testpypi`
- [ ] Check Test PyPI page: https://test.pypi.org/project/datacheck-cli/
- [ ] Install from Test PyPI: `pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ datacheck-cli`
- [ ] Test CLI: `datacheck version`
- [ ] Test validation: Run an example
- [ ] Uninstall: `pip uninstall datacheck-cli -y`
- [ ] Fix any issues found
- [ ] Repeat if needed

---

## Production PyPI Release

- [ ] Final build: `rm -rf dist/ && poetry build`
- [ ] Publish to PyPI: `poetry publish`
- [ ] Verify on PyPI: https://pypi.org/project/datacheck-cli/
- [ ] Check all metadata displays correctly
- [ ] Install from PyPI: `pip install datacheck-cli`
- [ ] Test CLI: `datacheck version`
- [ ] Test validation: Run an example
- [ ] Celebrate! 🎉

---

## GitHub Release

- [ ] Commit all changes to `main`
- [ ] Push to GitHub: `git push origin main`
- [ ] Create tag: `git tag -a v0.1.0 -m "Release v0.1.0 - Initial public release"`
- [ ] Push tag: `git push origin v0.1.0`
- [ ] Create GitHub release at https://github.com/yash-chauhan-dev/datacheck/releases
  - [ ] Tag: v0.1.0
  - [ ] Title: v0.1.0 - Initial Release
  - [ ] Description: Copy from CHANGELOG.md
  - [ ] Attach: dist/datacheck_cli-0.1.0.tar.gz
  - [ ] Attach: dist/datacheck_cli-0.1.0-py3-none-any.whl
- [ ] Publish release

---

## Post-Release

### Announcement
- [ ] Tweet/X post about the release
- [ ] LinkedIn post
- [ ] Reddit posts:
  - [ ] r/Python
  - [ ] r/datascience
  - [ ] r/dataengineering
- [ ] Dev.to blog post (optional)
- [ ] Hacker News "Show HN" (optional)

### Monitoring
- [ ] Add PyPI badges to README
- [ ] Watch for first GitHub stars ⭐
- [ ] Monitor PyPI downloads: https://pepy.tech/project/datacheck-cli
- [ ] Respond to initial issues/questions
- [ ] Thank early contributors

### Documentation
- [ ] Update main README with PyPI badge
- [ ] Add "Featured on" section if applicable
- [ ] Update any external documentation

---

## Verification

After 24 hours, verify:

- [ ] Package installs correctly: `pip install datacheck-cli`
- [ ] CLI works: `datacheck --help`
- [ ] No critical issues reported
- [ ] Download count increasing
- [ ] GitHub stars increasing (hopefully!)

---

## Known Issues & Fixes

If something goes wrong:

**Issue**: "File already exists" on PyPI
- **Fix**: Can't reupload same version. Bump to 0.1.1, rebuild, republish.

**Issue**: "Invalid credentials"
- **Fix**: Regenerate API token and reconfigure Poetry.

**Issue**: Package name taken
- **Fix**: Use alternative name (e.g., `datacheck-cli`).

**Issue**: Import errors after install
- **Fix**: Check package structure, ensure `__init__.py` exists.

**Issue**: Missing dependencies
- **Fix**: Check `pyproject.toml` dependencies section.

---

## Success Criteria

✅ Your release is successful when:

1. Package is available on PyPI: https://pypi.org/project/datacheck-cli/
2. Users can install: `pip install datacheck-cli`
3. CLI works: `datacheck version` shows v0.1.0
4. Examples run without errors
5. No critical bugs reported in first 48 hours
6. CI is green on all platforms
7. At least 10 downloads in first week (realistic for v0.1.0)

---

## Next Release

After v0.1.0 is stable, plan for v0.2.0:

- Review issues and feature requests
- Implement high-priority features from roadmap
- Update CHANGELOG.md
- Repeat this checklist!

---

**Notes:**
- Check off items as you complete them
- Don't skip steps!
- If in doubt, test on Test PyPI first
- Ask for help in GitHub Discussions if stuck

**Good luck! 🚀**

Date Started: ___________
Date Released: ___________
