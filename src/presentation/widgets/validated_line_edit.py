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

        self.setText(initial_value)
        self.textChanged.connect(self.validate)
        self.validate(initial_value)

    def validate(self, text: str) -> None:
        validation_errors = [
            result for validator in self._validators if (result := validator(text))
        ]
        if validation_errors:
            self.setStyleSheet("border: 1px solid red;")
            # self.setStyleSheet("QLineEdit { color : red; }")
            # self.setStyleSheet("QLineEdit { background : red; }")
            self.validation_error_occurred.emit(validation_errors)
        else:
            self.setStyleSheet("")


class ValidatedTextWidget(ValidatedLineEdit):
    def __init__(
        self,
        *,
        field_name: str,
        initial_value: str,
        min_length: typing.Optional[int] = None,
        max_length: typing.Optional[int] = None,
        additional_rules: typing.Optional[
            typing.List[typing.Callable[[str], typing.Optional[str]]]
        ] = None,
    ) -> None:
        validators: typing.List[typing.Callable[[str], typing.Optional[str]]] = []
        if min_length:
            validator = (
                lambda txt: f"{field_name.capitalize()} must be at least {min_length} characters."
                if len(txt) < min_length
                else None
            )
            validators.append(validator)
        if max_length:
            validator = (
                lambda txt: f"{field_name.capitalize()} must be at most {max_length} characters."
                if len(txt) > typing.cast(int, max_length)
                else None
            )
            validators.append(validator)
        if additional_rules:
            validators += additional_rules

        super().__init__(initial_value=initial_value, validators=validators)
