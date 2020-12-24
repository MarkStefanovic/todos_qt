import pytest

from src.domain.validation_result import *


@pytest.mark.parametrize(
    "result1, result2, should_be_equal, description",
    [
        (
            ValidationPassed("x should be y"),
            ValidationPassed("x should be y"),
            True,
            "Passed rules with the same name should be equal.",
        ),
        (
            ValidationPassed("x should be y"),
            ValidationPassed("x should be z"),
            False,
            "Passed rules with the different names should not be equal.",
        ),
        (
            ValidationFailed("x should be y", error_message="Whoopsy daisy!"),
            ValidationFailed("x should be y", error_message="Whoopsy daisy!"),
            True,
            "Failed validation rules with the same name and same error messages should be equal.",
        ),
        (
            ValidationFailed("x should be y", error_message="Whoopsy daisy!"),
            ValidationFailed("x should be y", error_message="Did I do that?"),
            False,
            "Failed validation rules with the same name but different error messages should not be equal.",
        ),
    ],
)
def test_validation_rule_comparison(
    result1: ValidationResult,
    result2: ValidationResult,
    should_be_equal: bool,
    description: ValidationResult,
) -> None:
    result = result1 == result2
    assert result is should_be_equal, description
