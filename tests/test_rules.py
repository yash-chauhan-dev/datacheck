"""Tests for validation rules."""

import pandas as pd
import pytest

from datacheck.config import RuleConfig
from datacheck.exceptions import ColumnNotFoundError, RuleDefinitionError
from datacheck.rules import (
    AllowedValuesRule,
    MinMaxRule,
    NotNullRule,
    RegexRule,
    RuleFactory,
    UniqueRule,
)


class TestNotNullRule:
    """Tests for NotNullRule."""

    def test_all_values_present(self) -> None:
        """Test validation passes when no nulls."""
        df = pd.DataFrame({"col1": [1, 2, 3, 4, 5]})
        rule = NotNullRule("test_rule", "col1")
        result = rule.validate(df)

        assert result.passed is True
        assert result.failed_rows == 0
        assert result.total_rows == 5

    def test_some_nulls(self) -> None:
        """Test validation fails when nulls present."""
        df = pd.DataFrame({"col1": [1, None, 3, None, 5]})
        rule = NotNullRule("test_rule", "col1")
        result = rule.validate(df)

        assert result.passed is False
        assert result.failed_rows == 2
        assert result.total_rows == 5
        assert result.failure_details is not None
        assert result.failure_details.failed_count == 2

    def test_all_nulls(self) -> None:
        """Test validation with all null values."""
        df = pd.DataFrame({"col1": [None, None, None]})
        rule = NotNullRule("test_rule", "col1")
        result = rule.validate(df)

        assert result.passed is False
        assert result.failed_rows == 3
        assert result.total_rows == 3

    def test_column_not_found(self) -> None:
        """Test error when column doesn't exist."""
        df = pd.DataFrame({"col1": [1, 2, 3]})
        rule = NotNullRule("test_rule", "col2")

        with pytest.raises(ColumnNotFoundError) as exc_info:
            rule.validate(df)

        assert "col2" in str(exc_info.value)
        assert "col1" in str(exc_info.value)


class TestMinMaxRule:
    """Tests for MinMaxRule."""

    def test_min_only_all_pass(self) -> None:
        """Test min validation passes."""
        df = pd.DataFrame({"age": [25, 30, 35, 40]})
        rule = MinMaxRule("age_check", "age", min_value=18)
        result = rule.validate(df)

        assert result.passed is True
        assert result.failed_rows == 0

    def test_min_only_some_fail(self) -> None:
        """Test min validation with failures."""
        df = pd.DataFrame({"age": [15, 25, 30, 10]})
        rule = MinMaxRule("age_check", "age", min_value=18)
        result = rule.validate(df)

        assert result.passed is False
        assert result.failed_rows == 2
        assert result.failure_details is not None

    def test_max_only_all_pass(self) -> None:
        """Test max validation passes."""
        df = pd.DataFrame({"age": [25, 30, 35, 40]})
        rule = MinMaxRule("age_check", "age", max_value=50)
        result = rule.validate(df)

        assert result.passed is True
        assert result.failed_rows == 0

    def test_max_only_some_fail(self) -> None:
        """Test max validation with failures."""
        df = pd.DataFrame({"age": [25, 60, 35, 70]})
        rule = MinMaxRule("age_check", "age", max_value=50)
        result = rule.validate(df)

        assert result.passed is False
        assert result.failed_rows == 2

    def test_min_and_max_all_pass(self) -> None:
        """Test min and max validation passes."""
        df = pd.DataFrame({"age": [20, 30, 40, 50]})
        rule = MinMaxRule("age_check", "age", min_value=18, max_value=65)
        result = rule.validate(df)

        assert result.passed is True
        assert result.failed_rows == 0

    def test_min_and_max_some_fail(self) -> None:
        """Test min and max validation with failures."""
        df = pd.DataFrame({"age": [10, 30, 70, 50]})
        rule = MinMaxRule("age_check", "age", min_value=18, max_value=65)
        result = rule.validate(df)

        assert result.passed is False
        assert result.failed_rows == 2

    def test_ignores_null_values(self) -> None:
        """Test that null values are ignored."""
        df = pd.DataFrame({"age": [25, None, 30, None]})
        rule = MinMaxRule("age_check", "age", min_value=18, max_value=65)
        result = rule.validate(df)

        assert result.passed is True

    def test_non_numeric_column(self) -> None:
        """Test error with non-numeric column."""
        df = pd.DataFrame({"name": ["Alice", "Bob", "Charlie"]})
        rule = MinMaxRule("name_check", "name", min_value=0)
        result = rule.validate(df)

        assert result.passed is False
        assert result.has_error is True
        assert result.error is not None
        assert "not numeric" in result.error

    def test_requires_min_or_max(self) -> None:
        """Test that at least min or max must be specified."""
        with pytest.raises(RuleDefinitionError, match="requires at least min or max"):
            MinMaxRule("test", "col", min_value=None, max_value=None)

    def test_column_not_found(self) -> None:
        """Test error when column doesn't exist."""
        df = pd.DataFrame({"col1": [1, 2, 3]})
        rule = MinMaxRule("test", "col2", min_value=0)

        with pytest.raises(ColumnNotFoundError):
            rule.validate(df)


class TestUniqueRule:
    """Tests for UniqueRule."""

    def test_all_unique(self) -> None:
        """Test validation passes with all unique values."""
        df = pd.DataFrame({"id": [1, 2, 3, 4, 5]})
        rule = UniqueRule("id_check", "id")
        result = rule.validate(df)

        assert result.passed is True
        assert result.failed_rows == 0

    def test_some_duplicates(self) -> None:
        """Test validation fails with duplicates."""
        df = pd.DataFrame({"id": [1, 2, 3, 2, 4, 3]})
        rule = UniqueRule("id_check", "id")
        result = rule.validate(df)

        assert result.passed is False
        # Duplicates: indices 1,3 (value 2) and indices 2,5 (value 3) = 4 rows
        assert result.failed_rows == 4
        assert result.failure_details is not None

    def test_ignores_null_values(self) -> None:
        """Test that null values are ignored."""
        df = pd.DataFrame({"id": [1, None, 2, None, 3]})
        rule = UniqueRule("id_check", "id")
        result = rule.validate(df)

        assert result.passed is True

    def test_null_duplicates_ignored(self) -> None:
        """Test that duplicate nulls are ignored."""
        df = pd.DataFrame({"id": [1, 2, None, None, 3]})
        rule = UniqueRule("id_check", "id")
        result = rule.validate(df)

        assert result.passed is True

    def test_column_not_found(self) -> None:
        """Test error when column doesn't exist."""
        df = pd.DataFrame({"col1": [1, 2, 3]})
        rule = UniqueRule("test", "col2")

        with pytest.raises(ColumnNotFoundError):
            rule.validate(df)


class TestRegexRule:
    """Tests for RegexRule."""

    def test_all_match(self) -> None:
        """Test validation passes when all values match."""
        df = pd.DataFrame({"email": ["a@b.com", "c@d.org", "e@f.net"]})
        rule = RegexRule("email_check", "email", pattern=r".+@.+\..+")
        result = rule.validate(df)

        assert result.passed is True
        assert result.failed_rows == 0

    def test_some_fail(self) -> None:
        """Test validation fails with some mismatches."""
        df = pd.DataFrame({"email": ["valid@test.com", "invalid", "another@test.com", "bad"]})
        rule = RegexRule("email_check", "email", pattern=r".+@.+\..+")
        result = rule.validate(df)

        assert result.passed is False
        assert result.failed_rows == 2
        assert result.failure_details is not None

    def test_ignores_null_values(self) -> None:
        """Test that null values are ignored."""
        df = pd.DataFrame({"email": ["a@b.com", None, "c@d.org"]})
        rule = RegexRule("email_check", "email", pattern=r".+@.+\..+")
        result = rule.validate(df)

        assert result.passed is True

    def test_numeric_pattern(self) -> None:
        """Test regex with numeric pattern."""
        df = pd.DataFrame({"code": ["123", "456", "ABC", "789"]})
        rule = RegexRule("code_check", "code", pattern=r"^\d{3}$")
        result = rule.validate(df)

        assert result.passed is False
        assert result.failed_rows == 1  # "ABC" fails

    def test_invalid_regex_pattern(self) -> None:
        """Test error with invalid regex pattern."""
        with pytest.raises(RuleDefinitionError, match="Invalid regex pattern"):
            RegexRule("test", "col", pattern="[invalid(")

    def test_column_not_found(self) -> None:
        """Test error when column doesn't exist."""
        df = pd.DataFrame({"col1": ["a", "b", "c"]})
        rule = RegexRule("test", "col2", pattern=r"\w+")

        with pytest.raises(ColumnNotFoundError):
            rule.validate(df)


class TestAllowedValuesRule:
    """Tests for AllowedValuesRule."""

    def test_all_allowed(self) -> None:
        """Test validation passes when all values allowed."""
        df = pd.DataFrame({"country": ["US", "UK", "CA", "US"]})
        rule = AllowedValuesRule("country_check", "country", allowed_values=["US", "UK", "CA"])
        result = rule.validate(df)

        assert result.passed is True
        assert result.failed_rows == 0

    def test_some_not_allowed(self) -> None:
        """Test validation fails with disallowed values."""
        df = pd.DataFrame({"country": ["US", "FR", "UK", "DE"]})
        rule = AllowedValuesRule("country_check", "country", allowed_values=["US", "UK", "CA"])
        result = rule.validate(df)

        assert result.passed is False
        assert result.failed_rows == 2  # FR and DE
        assert result.failure_details is not None

    def test_ignores_null_values(self) -> None:
        """Test that null values are ignored."""
        df = pd.DataFrame({"country": ["US", None, "UK"]})
        rule = AllowedValuesRule("country_check", "country", allowed_values=["US", "UK", "CA"])
        result = rule.validate(df)

        assert result.passed is True

    def test_numeric_allowed_values(self) -> None:
        """Test with numeric allowed values."""
        df = pd.DataFrame({"rating": [1, 2, 3, 5, 2]})
        rule = AllowedValuesRule("rating_check", "rating", allowed_values=[1, 2, 3, 4, 5])
        result = rule.validate(df)

        assert result.passed is True

    def test_empty_allowed_values(self) -> None:
        """Test error with empty allowed values."""
        with pytest.raises(RuleDefinitionError, match="allowed_values cannot be empty"):
            AllowedValuesRule("test", "col", allowed_values=[])

    def test_column_not_found(self) -> None:
        """Test error when column doesn't exist."""
        df = pd.DataFrame({"col1": ["a", "b", "c"]})
        rule = AllowedValuesRule("test", "col2", allowed_values=["a", "b"])

        with pytest.raises(ColumnNotFoundError):
            rule.validate(df)


class TestRuleFactory:
    """Tests for RuleFactory."""

    def test_create_not_null_rule(self) -> None:
        """Test creating NotNullRule from config."""
        config = RuleConfig(name="test", column="col1", rules={"not_null": True})
        rules = RuleFactory.create_rules(config)

        assert len(rules) == 1
        assert isinstance(rules[0], NotNullRule)
        assert rules[0].name == "test"
        assert rules[0].column == "col1"

    def test_create_min_rule(self) -> None:
        """Test creating MinMaxRule with min from config."""
        config = RuleConfig(name="test", column="age", rules={"min": 18})
        rules = RuleFactory.create_rules(config)

        assert len(rules) == 1
        assert isinstance(rules[0], MinMaxRule)
        assert rules[0].min_value == 18
        assert rules[0].max_value is None

    def test_create_max_rule(self) -> None:
        """Test creating MinMaxRule with max from config."""
        config = RuleConfig(name="test", column="age", rules={"max": 65})
        rules = RuleFactory.create_rules(config)

        assert len(rules) == 1
        assert isinstance(rules[0], MinMaxRule)
        assert rules[0].min_value is None
        assert rules[0].max_value == 65

    def test_create_min_and_max_rules(self) -> None:
        """Test creating separate min and max rules."""
        config = RuleConfig(name="test", column="age", rules={"min": 18, "max": 65})
        rules = RuleFactory.create_rules(config)

        assert len(rules) == 2
        assert all(isinstance(r, MinMaxRule) for r in rules)

    def test_create_unique_rule(self) -> None:
        """Test creating UniqueRule from config."""
        config = RuleConfig(name="test", column="id", rules={"unique": True})
        rules = RuleFactory.create_rules(config)

        assert len(rules) == 1
        assert isinstance(rules[0], UniqueRule)

    def test_create_regex_rule(self) -> None:
        """Test creating RegexRule from config."""
        config = RuleConfig(name="test", column="email", rules={"regex": r".+@.+\..+"})
        rules = RuleFactory.create_rules(config)

        assert len(rules) == 1
        assert isinstance(rules[0], RegexRule)
        assert rules[0].pattern_str == r".+@.+\..+"

    def test_create_allowed_values_rule(self) -> None:
        """Test creating AllowedValuesRule from config."""
        config = RuleConfig(
            name="test", column="country", rules={"allowed_values": ["US", "UK", "CA"]}
        )
        rules = RuleFactory.create_rules(config)

        assert len(rules) == 1
        assert isinstance(rules[0], AllowedValuesRule)
        assert rules[0].allowed_values == {"US", "UK", "CA"}

    def test_create_multiple_rules(self) -> None:
        """Test creating multiple rules from config."""
        config = RuleConfig(
            name="test",
            column="age",
            rules={"not_null": True, "min": 0, "max": 120},
        )
        rules = RuleFactory.create_rules(config)

        assert len(rules) == 3
        assert sum(isinstance(r, NotNullRule) for r in rules) == 1
        assert sum(isinstance(r, MinMaxRule) for r in rules) == 2

    def test_not_null_false_creates_no_rule(self) -> None:
        """Test that not_null: false doesn't create a rule."""
        config = RuleConfig(name="test", column="col", rules={"not_null": False, "min": 0})
        rules = RuleFactory.create_rules(config)

        assert len(rules) == 1
        assert isinstance(rules[0], MinMaxRule)

    def test_unique_false_creates_no_rule(self) -> None:
        """Test that unique: false doesn't create a rule."""
        config = RuleConfig(name="test", column="col", rules={"unique": False, "min": 0})
        rules = RuleFactory.create_rules(config)

        assert len(rules) == 1
        assert isinstance(rules[0], MinMaxRule)

    def test_invalid_regex_pattern(self) -> None:
        """Test error with invalid regex pattern."""
        config = RuleConfig(name="test", column="col", rules={"regex": "[invalid("})

        with pytest.raises(RuleDefinitionError, match="Invalid regex pattern"):
            RuleFactory.create_rules(config)

    def test_empty_allowed_values(self) -> None:
        """Test error with empty allowed values."""
        config = RuleConfig(name="test", column="col", rules={"allowed_values": []})

        with pytest.raises(RuleDefinitionError):
            RuleFactory.create_rules(config)

    def test_no_rules_created(self) -> None:
        """Test error when no rules are created."""
        config = RuleConfig(name="test", column="col", rules={"not_null": False})

        with pytest.raises(RuleDefinitionError, match="No valid rules created"):
            RuleFactory.create_rules(config)
