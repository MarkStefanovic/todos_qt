import typing

# noinspection PyPep8Naming
from PyQt6 import QtCore as qtc

from src.presentation.shared.widgets.table_view.model import TableViewModel

__all__ = ("BoundButtonEnabledSelector",)


class BoundButtonEnabledSelector:
    def __init__(self, *, model: TableViewModel) -> None:
        self._model: typing.Final[TableViewModel] = model

    def is_enabled(self, /, index: qtc.QModelIndex) -> bool:
        if self._model.items:
            item = self._model.items[index.row()]

            attr = self._model.get_attr_for_column_number(index.column())
            selector = attr.enabled_selector
            if selector is None:
                raise Exception(f"enabled_selector for attr, {attr.name}, is None.")

            return selector(item)

        return False
