# Release Checklist

> **📝 Note: This is for project maintainers only.**
>
> Contributors: See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.
> You only need to bump the version and update CHANGELOG.md for user-facing changes.

This checklist helps maintainers track release progress and ensure nothing is missed.

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

## GitHub Setup (One-Time)

### PyPI Credentials
- [ ] Created PyPI account at https://pypi.org
- [ ] Generated API token
- [ ] Added token to GitHub secrets as `PYPI_API_TOKEN`
- [ ] OR configured Trusted Publishing (recommended)

### GitHub Actions
- [ ] Verified CI workflow passes
- [ ] Verified auto-release workflow is enabled
- [ ] Verified PR version check workflow is enabled

---

## Release Process (Automated)

The release is fully automated when a PR with version bump is merged to `main`:

### Before Merge
- [ ] PR has version bumped (e.g., `poetry version minor`)
- [ ] CHANGELOG.md updated with new version
- [ ] PR checks passing (CI, version check)
- [ ] Code reviewed and approved

### Merge PR
- [ ] Merge PR to `main`
- [ ] Wait for CI to pass on `main` (~5 min)
- [ ] Auto-release workflow triggers automatically
- [ ] Watch Actions tab for release progress (~10-15 min total)

### Verify Release
- [ ] Check PyPI: https://pypi.org/project/datacheck-cli/
- [ ] Check GitHub Release: https://github.com/yash-chauhan-dev/datacheck/releases
- [ ] Install and test: `pip install datacheck-cli`
- [ ] Test CLI: `datacheck version`
- [ ] Celebrate! 🎉

**Note**: If using tag-based release instead:
- [ ] Create tag: `git tag -a v0.X.Y -m "Release v0.X.Y"`
- [ ] Push tag: `git push origin v0.X.Y`
- [ ] Watch Actions tab for automated release

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

## Troubleshooting

If something goes wrong during automated release:

**Issue**: CI workflow failed, release blocked
- **Fix**: Check CI logs in Actions tab. Fix errors and push fix to `main`. CI will re-run.

**Issue**: Auto-release workflow failed
- **Fix**: Check workflow logs in Actions tab. Common causes:
  - PyPI credentials incorrect (check GitHub secrets)
  - Version already exists on PyPI (bump version)
  - Tests failed (fix and push to `main`)

**Issue**: Release succeeded but package doesn't work
- **Fix**: Create hotfix PR with version bump (e.g., 0.1.0 → 0.1.1). Merge to trigger new release.

**Issue**: GitHub Actions not triggering
- **Fix**: Verify workflow files exist in `.github/workflows/` and are enabled in Actions tab.

---

## Success Criteria

✅ Your automated release is successful when:

1. ✅ Auto-release workflow completed successfully (check Actions tab)
2. ✅ Package is live on PyPI: https://pypi.org/project/datacheck-cli/
3. ✅ GitHub Release created: https://github.com/yash-chauhan-dev/datacheck/releases
4. ✅ Users can install: `pip install datacheck-cli`
5. ✅ CLI works: `datacheck version` shows correct version
6. ✅ Examples run without errors
7. ✅ No critical bugs reported in first 48 hours
8. ✅ CI remains green on all platforms

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
