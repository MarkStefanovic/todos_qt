from __future__ import annotations

import typing

from PyQt6 import QtCore as qtc, QtWidgets as qtw  # noqa

__all__ = ("MapCBO",)


Value = typing.TypeVar("Value")


class MapCBO(typing.Generic[Value], qtw.QComboBox):
    value_changed = qtc.pyqtSignal(object)  # Value

    def __init__(self, *, parent: qtw.QWidget | None = None):
        super().__init__(parent=parent)

        self.setFocusPolicy(qtc.Qt.FocusPolicy.StrongFocus)
        self.setMouseTracking(False)
        self.setStyleSheet("combobox-popup: 0;")

        # noinspection PyUnresolvedReferences
        self.currentIndexChanged.connect(self._on_current_index_changed)

    def get_value(self) -> Value | None:
        return self.currentData()

    def get_values(self) -> list[Value]:
        values: list[Value] = []
        for index in range(self.count()):
            if value := self.itemData(index):
                values.append(value)
        return values

    def set_value(self, /, value: Value | None) -> None:
        for i in range(self.count()):
            data = self.itemData(i)
            if data is not None:
                if data == value:
                    self.setCurrentIndex(i)
                    return None

        # warnings.warn(f"The value, {value!r}, is not an option.")

    def set_values(self, /, values: dict[Value, str]) -> None:
        self.blockSignals(True)

        previous_selection = self.currentData()

        self.clear()
        for value, display_value in values.items():
            self.addItem(display_value, userData=value)

        if previous_selection:
            self.set_value(previous_selection)

        self.blockSignals(False)

    def _on_current_index_changed(self, /, _: int) -> None:
        self.value_changed.emit(self.currentData())  # noqa
