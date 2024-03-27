import typing

# noinspection PyPep8Naming
from PyQt6 import QtCore as qtc, QtGui as qtg

from src.presentation.shared.widgets.table_view.model import TableViewModel

__all__ = ("BoundButtonTextColorSelector",)


class BoundButtonTextColorSelector:
    def __init__(self, *, model: TableViewModel) -> None:
        self._model: typing.Final[TableViewModel] = model

    def get_text_color(self, /, index: qtc.QModelIndex) -> qtg.QColor | qtc.Qt.GlobalColor | None:
        if self._model.items:
            item = self._model.items[index.row()]

            attr = self._model.get_attr_for_column_number(index.column())
            selector = attr.color_selector
            if selector is None:
                raise Exception(f"color_selector for attr, {attr.name}, is None.")

            return selector(item)

        return qtg.QColor()
