from __future__ import annotations

import typing

from PyQt5 import QtWidgets as qtw, QtCore as qtc
from loguru import logger

from src import domain, service
from src.presentation.todo import (
    todo_list_view_model,
)
from src.presentation.todo.todo_edit_form import edit_form_model, edit_form_base

__all__ = ("TodoListView",)


class TodoListView(qtw.QWidget):
    def __init__(
        self, *, todo_service: service.TodoService, category: domain.TodoCategory
    ):
        super().__init__()

        self._todo_service = todo_service

        self._model = todo_list_view_model.TableListViewModel(
            todo_service=todo_service, category=category
        )

        self._table = qtw.QTableView()
        self._table.setSortingEnabled(True)
        self._table.setSizeAdjustPolicy(qtw.QAbstractScrollArea.AdjustToContents)
        self._table.setModel(self._model)
        self._table.resizeColumnsToContents()

        button_layout = qtw.QHBoxLayout()
        # button_group = qtw.QGroupBox(alignment=qtc.Qt.AlignRight)
        # button_group.setAlignment(qtc.Qt.AlignHCenter)

        mark_complete_button = qtw.QPushButton("Mark Complete", clicked=self.mark_complete)  # type: ignore
        mark_complete_button.setMinimumWidth(100)
        refresh_button = qtw.QPushButton("Refresh", clicked=self.refresh)  # type: ignore
        refresh_button.setMinimumWidth(100)
        add_button = qtw.QPushButton("Add", clicked=self.open_add_form)  # type: ignore
        add_button.setMinimumWidth(100)
        edit_button = qtw.QPushButton("Edit", clicked=self.open_edit_form)  # type: ignore
        edit_button.setMinimumWidth(100)
        delete_button = qtw.QPushButton("Delete", clicked=self.delete)  # type: ignore
        delete_button.setMinimumWidth(100)

        spacer = qtw.QSpacerItem(20, 40, qtw.QSizePolicy.Expanding)
        button_layout.addItem(spacer)
        button_layout.addWidget(mark_complete_button)
        button_layout.addWidget(refresh_button)
        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        # button_group.setLayout(button_layout)

        layout = qtw.QVBoxLayout()
        layout.addWidget(self._table)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self._popup: typing.Optional[qtw.QDialog] = None

        self._selection_model = self._table.selectionModel()
        # self._selection_model.selectionChanged.connect(self.show_selected_id)

    def delete(self) -> None:
        logger.debug("delete_button clicked.")
        if todo_id := self.selected_id:
            description = self._model.get_row_by_id(todo_id)[1]
            confirmation = qtw.QMessageBox.question(
                self,
                "Confirm Delete",
                f"Are you sure you want to delete {description!r}?",
                qtw.QMessageBox.Yes | qtw.QMessageBox.No,  # type: ignore
                qtw.QMessageBox.No,
            )
            if confirmation == qtw.QMessageBox.Yes:
                self._model.delete(todo_id)
            else:
                logger.debug(
                    f"User did not confirm they wanted to delete {description}."
                )
        else:
            logger.debug("Nothing is selected.")

    def mark_complete(self) -> None:
        logger.debug("mark_complete_button clicked.")
        if self.selected_id:
            self._model.mark_complete(self.selected_id)
        else:
            logger.debug("Nothing is selected.")

    def open_add_form(self) -> None:
        print(f"opening add form")
        item_model = edit_form_model.TodoEditFormModel(
            edit_mode=domain.EditMode.ADD, todo_service=self._todo_service
        )
        self._popup = edit_form_base.EditFormBase(item_model)
        self._popup.exec()

    def open_edit_form(self) -> None:
        if self.selected_id:
            logger.debug(f"opening edit form: {self.selected_id=}")
            item_model = edit_form_model.TodoEditFormModel(
                edit_mode=domain.EditMode.EDIT,
                todo_service=self._todo_service,
                todo_id=self.selected_id,
            )
            self._popup = edit_form_base.EditFormBase(item_model)
            self._popup.exec()
        else:
            logger.debug("Nothing is selected.")

    def refresh(self) -> None:
        logger.debug("Refresh clicked")
        self._model.refresh()
        self._table.setModel(self._model)

    @property
    def selected_id(self) -> typing.Optional[int]:
        if selected_index := self._table.selectedIndexes():
            first_row_selected = selected_index[0].row()
            first_col_index = self._table.model().index(first_row_selected, 0)
            todo_id = self._table.model().data(first_col_index, qtc.Qt.DisplayRole)
            logger.debug(f"Selection: {first_row_selected=}, {todo_id=}")
            return todo_id
        else:
            logger.debug("Nothing is selected.")
            return None

    # def show_selected_id(self) -> None:
    #     selected_index = self._table.selectedIndexes()
    #     first_row_selected = selected_index[0].row()
    #     first_col_index = self._table.model().index(first_row_selected, 0)
    #     todo_id = self._table.model().data(first_col_index, qtc.Qt.DisplayRole)
    #     logger.debug(f"{first_row_selected=}, {todo_id=}")
