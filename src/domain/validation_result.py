from __future__ import annotations

import dataclasses

__all__ = (
    "ValidationResult",
    "ValidationFailed",
    "ValidationPassed",
)


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

    def __eq__(self, o: object) -> bool:
        assert isinstance(o, ValidationResult)
        if isinstance(o, ValidationFailed):
            return o.error_message == self.error_message
        return False


@dataclasses.dataclass(frozen=True)
class ValidationPassed(ValidationResult):
    rule_description: str
