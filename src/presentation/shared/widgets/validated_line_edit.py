import functools
import typing

from PyQt5 import QtCore as qtc, QtWidgets as qtw

__all__ = (
    "ValidatedLineEdit",
    "ValidatedTextWidget",
)


class ValidatedLineEdit(qtw.QLineEdit):
    validation_error_occurred = qtc.pyqtSignal(list)

    def __init__(
        self,
        *,
        validators: typing.List[typing.Callable[[str], typing.Optional[str]]],
        initial_value: str,
    ) -> None:
        super().__init__()

        self._validators = validators

        self._original_stylesheet = self.styleSheet()

        self.setText(initial_value)
        # noinspection PyUnresolvedReferences
        self.textChanged.connect(self.validate)
        self.validate(initial_value)

    def validate(self, text: str) -> None:
        validation_errors = [
            result for validator in self._validators if (result := validator(text))
        ]
        if validation_errors:
            self.setStyleSheet("border: 1px solid red;")

            self.validation_error_occurred.emit(validation_errors)  # noqa
        else:
            self.setStyleSheet(self._original_stylesheet)


class ValidatedTextWidget(ValidatedLineEdit):
    def __init__(
        self,
        *,
        field_name: str,
        initial_value: str,
        min_length: int | None = None,
        max_length: int | None = None,
        additional_rules: list[typing.Callable[[str], str | None]] | None = None,
    ) -> None:
        validators: list[typing.Callable[[str], str | None]] = []
        if min_length:
            validator = functools.partial(
                _validate_min_length,
                field_name=field_name,
                min_length=min_length,
            )
            validators.append(validator)
        if max_length:
            validator = functools.partial(
                _validate_max_length,
                field_name=field_name,
                max_length=max_length,
            )
            validators.append(validator)
        if additional_rules:
            validators += additional_rules

        super().__init__(initial_value=initial_value, validators=validators)


def _validate_max_length(field_name: str, max_length: int, txt: str) -> str | None:
    if len(txt) > max_length:
        return f"{field_name.capitalize()} must be at most {max_length} characters."
    return None


def _validate_min_length(field_name: str, min_length: int, txt: str) -> str | None:
    if len(txt) < min_length:
        return f"{field_name.capitalize()} must be at least {min_length} characters."
    return None
