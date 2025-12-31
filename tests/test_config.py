"""Tests for configuration parsing and validation."""

from pathlib import Path
from typing import Any

import pytest

from datacheck.config import ConfigLoader, RuleConfig, ValidationConfig
from datacheck.exceptions import ConfigurationError


class TestRuleConfig:
    """Tests for RuleConfig dataclass."""

    def test_valid_rule_config(self) -> None:
        """Test creating a valid rule configuration."""
        rule = RuleConfig(
            name="test_rule",
            column="test_column",
            rules={"not_null": True, "min": 0, "max": 100},
        )
        assert rule.name == "test_rule"
        assert rule.column == "test_column"
        assert rule.rules == {"not_null": True, "min": 0, "max": 100}

    def test_empty_name(self) -> None:
        """Test that empty name raises error."""
        with pytest.raises(ConfigurationError, match="Rule name cannot be empty"):
            RuleConfig(name="", column="test", rules={"not_null": True})

    def test_empty_column(self) -> None:
        """Test that empty column raises error."""
        with pytest.raises(ConfigurationError, match="Column name cannot be empty"):
            RuleConfig(name="test", column="", rules={"not_null": True})

    def test_empty_rules(self) -> None:
        """Test that empty rules dict raises error."""
        with pytest.raises(ConfigurationError, match="Rules cannot be empty"):
            RuleConfig(name="test", column="test_col", rules={})

    def test_invalid_rule_type(self) -> None:
        """Test that invalid rule type raises error."""
        with pytest.raises(ConfigurationError, match="Invalid rule types"):
            RuleConfig(
                name="test",
                column="test_col",
                rules={"not_null": True, "invalid_rule": True},
            )

    def test_all_valid_rule_types(self) -> None:
        """Test all valid rule types."""
        rule = RuleConfig(
            name="test",
            column="test_col",
            rules={
                "not_null": True,
                "min": 0,
                "max": 100,
                "unique": True,
                "regex": r"\d+",
                "allowed_values": ["a", "b", "c"],
            },
        )
        assert len(rule.rules) == 6


class TestValidationConfig:
    """Tests for ValidationConfig dataclass."""

    def test_valid_config(self) -> None:
        """Test creating valid validation configuration."""
        checks = [
            RuleConfig(name="rule1", column="col1", rules={"not_null": True}),
            RuleConfig(name="rule2", column="col2", rules={"min": 0}),
        ]
        config = ValidationConfig(checks=checks)
        assert len(config.checks) == 2

    def test_empty_checks(self) -> None:
        """Test that empty checks list raises error."""
        with pytest.raises(ConfigurationError, match="must contain at least one check"):
            ValidationConfig(checks=[])

    def test_duplicate_rule_names(self) -> None:
        """Test that duplicate rule names raise error."""
        checks = [
            RuleConfig(name="rule1", column="col1", rules={"not_null": True}),
            RuleConfig(name="rule1", column="col2", rules={"min": 0}),
        ]
        with pytest.raises(ConfigurationError, match="Duplicate rule names"):
            ValidationConfig(checks=checks)


class TestConfigLoader:
    """Tests for ConfigLoader."""

    def test_load_valid_config(self, tmp_path: Path) -> None:
        """Test loading a valid configuration file."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            """
checks:
  - name: age_validation
    column: age
    rules:
      not_null: true
      min: 0
      max: 120

  - name: email_validation
    column: email
    rules:
      not_null: true
      regex: ".+@.+\\\\..+"
"""
        )

        config = ConfigLoader.load(config_file)
        assert len(config.checks) == 2
        assert config.checks[0].name == "age_validation"
        assert config.checks[0].column == "age"
        assert config.checks[0].rules == {"not_null": True, "min": 0, "max": 120}
        assert config.checks[1].name == "email_validation"

    def test_load_file_not_found(self) -> None:
        """Test loading non-existent file raises error."""
        with pytest.raises(ConfigurationError, match="Configuration file not found"):
            ConfigLoader.load("nonexistent.yaml")

    def test_load_directory_instead_of_file(self, tmp_path: Path) -> None:
        """Test loading a directory raises error."""
        with pytest.raises(ConfigurationError, match="not a file"):
            ConfigLoader.load(tmp_path)

    def test_load_invalid_yaml(self, tmp_path: Path) -> None:
        """Test loading invalid YAML raises error."""
        config_file = tmp_path / "invalid.yaml"
        config_file.write_text("invalid: yaml: content: [")

        with pytest.raises(ConfigurationError, match="Invalid YAML"):
            ConfigLoader.load(config_file)

    def test_load_empty_file(self, tmp_path: Path) -> None:
        """Test loading empty file raises error."""
        config_file = tmp_path / "empty.yaml"
        config_file.write_text("")

        with pytest.raises(ConfigurationError, match="Configuration file is empty"):
            ConfigLoader.load(config_file)

    def test_load_non_dict_yaml(self, tmp_path: Path) -> None:
        """Test loading YAML that's not a dict raises error."""
        config_file = tmp_path / "list.yaml"
        config_file.write_text("- item1\n- item2")

        with pytest.raises(ConfigurationError, match="must be a dictionary"):
            ConfigLoader.load(config_file)

    def test_load_missing_checks_key(self, tmp_path: Path) -> None:
        """Test loading config without 'checks' key raises error."""
        config_file = tmp_path / "no_checks.yaml"
        config_file.write_text("other_key: value")

        with pytest.raises(ConfigurationError, match="must contain 'checks' key"):
            ConfigLoader.load(config_file)

    def test_load_checks_not_list(self, tmp_path: Path) -> None:
        """Test loading config with non-list checks raises error."""
        config_file = tmp_path / "bad_checks.yaml"
        config_file.write_text("checks: not_a_list")

        with pytest.raises(ConfigurationError, match="'checks' must be a list"):
            ConfigLoader.load(config_file)

    def test_load_check_not_dict(self, tmp_path: Path) -> None:
        """Test loading config with non-dict check raises error."""
        config_file = tmp_path / "bad_check.yaml"
        config_file.write_text("checks:\n  - just_a_string")

        with pytest.raises(ConfigurationError, match="must be a dictionary"):
            ConfigLoader.load(config_file)

    def test_load_check_missing_name(self, tmp_path: Path) -> None:
        """Test loading check without name raises error."""
        config_file = tmp_path / "no_name.yaml"
        config_file.write_text(
            """
checks:
  - column: test
    rules:
      not_null: true
"""
        )

        with pytest.raises(ConfigurationError, match="missing 'name' field"):
            ConfigLoader.load(config_file)

    def test_load_check_missing_column(self, tmp_path: Path) -> None:
        """Test loading check without column raises error."""
        config_file = tmp_path / "no_column.yaml"
        config_file.write_text(
            """
checks:
  - name: test
    rules:
      not_null: true
"""
        )

        with pytest.raises(ConfigurationError, match="missing 'column' field"):
            ConfigLoader.load(config_file)

    def test_load_check_missing_rules(self, tmp_path: Path) -> None:
        """Test loading check without rules raises error."""
        config_file = tmp_path / "no_rules.yaml"
        config_file.write_text(
            """
checks:
  - name: test
    column: test_col
"""
        )

        with pytest.raises(ConfigurationError, match="missing 'rules' field"):
            ConfigLoader.load(config_file)

    def test_load_with_invalid_rule_type(self, tmp_path: Path) -> None:
        """Test loading config with invalid rule type raises error."""
        config_file = tmp_path / "invalid_rule.yaml"
        config_file.write_text(
            """
checks:
  - name: test
    column: test_col
    rules:
      invalid_rule: true
"""
        )

        with pytest.raises(ConfigurationError, match="Invalid rule types"):
            ConfigLoader.load(config_file)

    def test_find_config_yaml(self, tmp_path: Path, monkeypatch: Any) -> None:
        """Test finding .datacheck.yaml file."""
        monkeypatch.chdir(tmp_path)
        config_file = tmp_path / ".datacheck.yaml"
        config_file.write_text("checks: []")

        found = ConfigLoader.find_config()
        assert found is not None
        assert found.name == ".datacheck.yaml"

    def test_find_config_yml(self, tmp_path: Path, monkeypatch: Any) -> None:
        """Test finding .datacheck.yml file."""
        monkeypatch.chdir(tmp_path)
        config_file = tmp_path / ".datacheck.yml"
        config_file.write_text("checks: []")

        found = ConfigLoader.find_config()
        assert found is not None
        assert found.name == ".datacheck.yml"

    def test_find_config_priority(self, tmp_path: Path, monkeypatch: Any) -> None:
        """Test that .datacheck.yaml has priority over other names."""
        monkeypatch.chdir(tmp_path)
        (tmp_path / ".datacheck.yaml").write_text("checks: []")
        (tmp_path / "datacheck.yaml").write_text("checks: []")

        found = ConfigLoader.find_config()
        assert found is not None
        assert found.name == ".datacheck.yaml"

    def test_find_config_not_found(self, tmp_path: Path, monkeypatch: Any) -> None:
        """Test finding config when no file exists."""
        monkeypatch.chdir(tmp_path)

        found = ConfigLoader.find_config()
        assert found is None

    def test_load_with_string_path(self, tmp_path: Path) -> None:
        """Test loading config with string path."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            """
checks:
  - name: test
    column: test_col
    rules:
      not_null: true
"""
        )

        config = ConfigLoader.load(str(config_file))
        assert len(config.checks) == 1
