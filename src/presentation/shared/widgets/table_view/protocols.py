import typing

# noinspection PyPep8Naming
from PyQt6 import QtCore as qtc, QtGui as qtg

from src.presentation.shared.widgets.table_view.item import Item
from src.presentation.shared.widgets.table_view.value import Value

__all__ = (
    "EnabledSelector",
    "TextColorSelector",
    "ValueSelector",
)


class EnabledSelector(typing.Protocol[Item]):
    def __call__(self, /, item: Item) -> bool:
        raise NotImplementedError


class TextColorSelector(typing.Protocol[Item]):
    def __call__(self, /, item: Item) -> qtg.QColor | qtc.Qt.GlobalColor | None:
        raise NotImplementedError


class ValueSelector(typing.Protocol[Item, Value]):
    def __call__(self, /, item: Item) -> Value:
        raise NotImplementedError
