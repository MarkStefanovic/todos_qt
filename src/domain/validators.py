from src.domain import validation_result


def value_is_not_blank(value: str, /) -> validation_result.ValidationResult:
    if value:
        return validation_result.ValidationPassed("value_is_not_blank")
    else:
        return validation_result.ValidationFailed(
            rule_description="value_is_not_blank", error_message="value is required"
        )
