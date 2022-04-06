import typing
import warnings

from PyQt5 import QtCore as qtc, QtWidgets as qtw

__all__ = ("MapCBO",)

Value = typing.TypeVar("Value")


class MapCBO(typing.Generic[Value], qtw.QWidget):
    value_changed = qtc.pyqtSignal(object)  # Value

    def __init__(self, *, mapping: dict[Value, str] | None = None, value: Value | None = None):
        super().__init__()

        self._cbo = qtw.QComboBox()

        self._mapping: dict[Value, str] = {}

        self._index_by_value: dict[Value, int] = {}

        if mapping is not None:
            self.set_values(mapping=mapping)

        if value is not None:
            self.set_value(value=value)

        self._cbo.currentIndexChanged.connect(self._on_current_index_changed)

        layout = qtw.QVBoxLayout()
        layout.addWidget(self._cbo)
        self.setLayout(layout)

    def get_value(self) -> Value:
        return self._cbo.currentData()

    def get_values(self) -> list[Value]:
        return list(self._mapping.keys())

    def set_value(self, *, value: Value) -> None:
        if value in self._index_by_value:
            if self._cbo.currentIndex() != self._index_by_value[value]:
                self._cbo.setCurrentIndex(self._index_by_value[value])
        else:
            warnings.warn(
                f"The value, {value!r}, is not an option.  Available values include the "
                f"following: {', '.join(str(v) for v in self._index_by_value.keys())}"
            )
            self._cbo.setCurrentIndex(0)

    def set_values(self, *, mapping: dict[Value, str]) -> None:
        if mapping != self._mapping:
            self.blockSignals(True)

            self._mapping = mapping

            self._index_by_value = {
                value: ix
                for ix, value in enumerate(mapping.keys())
            }

            self._cbo.clear()
            for value, display_value in mapping.items():
                self._cbo.addItem(display_value, userData=value)

            self.blockSignals(False)

    def _on_current_index_changed(self, index: int) -> None:
        self.value_changed.emit(self._cbo.currentData())
