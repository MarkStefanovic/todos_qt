import typing

from PyQt5 import QtCore as qtc, QtWidgets as qtw

__all__ = ("MapCBO",)

Display = typing.TypeVar("Display")
Value = typing.TypeVar("Value")


class MapCBO(typing.Generic[Display, Value], qtw.QWidget):
    value_changed = qtc.pyqtSignal(object)  # Value

    def __init__(self, *, mapping: dict[Display, Value], value: Value):
        super().__init__()

        self._cbo = qtw.QComboBox()

        self._index_by_value = {
            value: ix
            for ix, value in enumerate(mapping.values())
        }

        for key, value in mapping.items():
            self._cbo.addItem(key, userData=value)  # type: ignore

        self.set_value(value=value)

        # noinspection PyUnresolvedReferences
        self._cbo.currentIndexChanged.connect(lambda _: self._cbo.currentData())

    def set_value(self, *, value: Value) -> None:
        self._cbo.setCurrentIndex(self._index_by_value[value])

    def get_value(self) -> Value:
        return self._cbo.currentData()
