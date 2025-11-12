"""
Rule Validation - Validation rules for data
FROZEN MODULE - Pure stdlib
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional


@dataclass
class ValidationResult:
    """Result of validation."""
    valid: bool
    errors: List[str]
    warnings: List[str] = None

    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []


@dataclass
class ValidationRule:
    """Validation rule definition."""
    name: str
    check: Callable[[Any], ValidationResult]
    description: str = ""
    severity: str = "error"  # error, warning


class RuleRegistry:
    """Registry for validation rules."""

    def __init__(self):
        self._rules: Dict[str, ValidationRule] = {}

    def register(self, rule: ValidationRule) -> None:
        """Register a validation rule."""
        self._rules[rule.name] = rule

    def get(self, name: str) -> Optional[ValidationRule]:
        """Get rule by name."""
        return self._rules.get(name)

    def list(self) -> List[str]:
        """List all rule names."""
        return list(self._rules.keys())

    def validate(self, data: Any, rule_names: List[str]) -> ValidationResult:
        """
        Validate data against multiple rules.
        Aggregates results from all rules.
        """
        all_errors = []
        all_warnings = []

        for rule_name in rule_names:
            rule = self.get(rule_name)
            if not rule:
                all_errors.append(f"Rule '{rule_name}' not found")
                continue

            result = rule.check(data)
            if rule.severity == "error":
                all_errors.extend(result.errors)
            else:
                all_warnings.extend(result.errors)

            all_warnings.extend(result.warnings)

        return ValidationResult(
            valid=len(all_errors) == 0,
            errors=all_errors,
            warnings=all_warnings
        )


# Global registry
_registry = RuleRegistry()


def define_rule(
    name: str,
    check: Callable[[Any], ValidationResult],
    description: str = "",
    severity: str = "error"
) -> ValidationRule:
    """
    Define a new validation rule.

    Args:
        name: Rule name
        check: Validation function that returns ValidationResult
        description: Rule description
        severity: 'error' or 'warning'
    """
    rule = ValidationRule(
        name=name,
        check=check,
        description=description,
        severity=severity
    )
    _registry.register(rule)
    return rule


def validate_asset(data: Any, rule_names: List[str]) -> ValidationResult:
    """Validate data against rules."""
    return _registry.validate(data, rule_names)


def get_rule(name: str) -> Optional[ValidationRule]:
    """Get rule by name."""
    return _registry.get(name)


def list_rules() -> List[str]:
    """List all registered rule names."""
    return _registry.list()
