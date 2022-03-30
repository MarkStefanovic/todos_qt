import typing

from PyQt5 import QtCore as qtc, QtWidgets as qtw

__all__ = ("MapCBO",)

Value = typing.TypeVar("Value")


class MapCBO(typing.Generic[Value], qtw.QWidget):
    value_changed = qtc.pyqtSignal(object)  # Value

    def __init__(self, *, mapping: dict[Value, str], value: Value):
        super().__init__()

        self._cbo = qtw.QComboBox()

        self._mapping = mapping

        self._index_by_value: dict[Value, int] = {}

        self.set_values(mapping=mapping)

        self.set_value(value=value)

        # noinspection PyUnresolvedReferences
        self._cbo.currentIndexChanged.connect(
            lambda _: self.value_changed.emit(self._cbo.currentData())
        )

        layout = qtw.QVBoxLayout()
        layout.addWidget(self._cbo)
        self.setLayout(layout)

    def set_value(self, *, value: Value) -> None:
        if value in self._index_by_value:
            self._cbo.setCurrentIndex(self._index_by_value[value])
        else:
            raise ValueError(
                f"The value, {value!r}, is not an option.  Available values include the "
                f"following: {', '.join(str(v) for v in self._index_by_value.values())}"
            )

    def get_value(self) -> Value:
        return self._cbo.currentData()

    def get_values(self) -> dict[Value, str]:
        return self._mapping

    def set_values(self, *, mapping: dict[Value, str]) -> None:
        self._mapping = mapping

        self._index_by_value = {
            value: ix
            for ix, value in enumerate(mapping.keys())
        }

        for value, display_value in mapping.items():
            self._cbo.addItem(display_value, userData=value)
