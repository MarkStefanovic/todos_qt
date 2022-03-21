import enum
import typing

from PyQt5 import QtCore as qtc, QtWidgets as qtw

__all__ = ("EnumCBO",)

T = typing.TypeVar("T", enum.Enum, str)


class EnumCBO(typing.Generic[T], qtw.QWidget):
    value_changed = qtc.pyqtSignal(object)  # T

    def __init__(self, *, cls: typing.Type[T], value: T):
        super().__init__()

        self._cbo = qtw.QComboBox()

        self._index_by_value = {data.value: ix for ix, data in enumerate(cls)}  # type: ignore

        for data in cls:  # type: ignore
            self._cbo.addItem(data.value, userData=data)

        self.set_value(value=value)

        # noinspection PyUnresolvedReferences
        self._cbo.currentIndexChanged.connect(lambda _: self.value_changed.emit(self._cbo.currentData()))

    def set_value(self, *, value: T) -> None:
        self._cbo.setCurrentIndex(self._index_by_value[value.value])  # type: ignore

    def get_value(self) -> T:
        return self._cbo.currentData()
