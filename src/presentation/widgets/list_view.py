from __future__ import annotations

import typing

from PyQt5 import QtWidgets as qtw, QtCore as qtc
from loguru import logger

from src.presentation.widgets import list_view_model

__all__ = ("ListView",)


class ListView(qtw.QWidget):
    def __init__(self, /, view_model: list_view_model.ListViewModel):
        super().__init__()

        self._view_model = view_model

        self._table = qtw.QTableView()

        self._table.setSortingEnabled(True)
        self._table.setSizeAdjustPolicy(qtw.QAbstractScrollArea.AdjustToContents)
        self._table.setModel(self._view_model)

        self.refresh()

    def refresh(self) -> None:
        logger.debug("Refresh clicked")
        self._view_model.refresh()
        self._table.resizeColumnsToContents()

    def selected_row_id(self) -> typing.Optional[typing.List[typing.Any]]:
        if selected_index := self._table.selectedIndexes():
            first_row_selected = selected_index[0].row()
            first_col_index = self._table.model().index(first_row_selected, 0)
            todo_id = self._table.model().data(first_col_index, qtc.Qt.DisplayRole)
            logger.debug(f"Selected row = {first_row_selected}, todo_id = {todo_id}")
            return todo_id
        else:
            logger.debug("Nothing is selected.")
            return None

    @property
    def view_model(self) -> list_view_model.ListViewModel:
        return self._view_model
