from __future__ import annotations

import dataclasses


@dataclasses.dataclass(frozen=True)
class ValidationResult:
    rule_description: str

    @staticmethod
    def passed(rule_name: str, /) -> ValidationPassed:
        return ValidationPassed(rule_name)

    @staticmethod
    def failed(rule_name: str, /, error_message: str) -> ValidationFailed:
        return ValidationFailed(rule_name, error_message=error_message)


@dataclasses.dataclass(frozen=True)
class ValidationFailed(ValidationResult):
    error_message: str


@dataclasses.dataclass(frozen=True)
class ValidationPassed(ValidationResult):
    rule_description: str
