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

        self._selected_row_id: typing.Optional[int] = None

        # noinspection PyUnresolvedReferences
        self._table.selectionModel().selectionChanged.connect(self._set_selected_row_id)

        self.refresh()

    def refresh(self) -> None:
        logger.debug("Refresh clicked")
        self._view_model.refresh()
        self._table.resizeColumnsToContents()

    @property
    def selected_row_id(self) -> typing.Optional[int]:
        return self._selected_row_id

    def _set_selected_row_id(self, selection: qtc.QItemSelection) -> None:
        if ixs := selection.indexes():
            first_row_selected = ixs[0].row()
            first_col_index = self._table.model().index(first_row_selected, 0)
            self._selected_row_id = self._table.model().data(
                first_col_index, qtc.Qt.DisplayRole
            )
            logger.debug(
                f"Selected row {first_row_selected}, id = {self._selected_row_id}"
            )
        else:
            logger.debug("Selection cleared.")
            self._selected_row_id = None

    @property
    def view_model(self) -> list_view_model.ListViewModel:
        return self._view_model
