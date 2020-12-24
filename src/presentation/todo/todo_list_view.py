from __future__ import annotations

import typing

from PyQt5 import QtWidgets as qtw
from loguru import logger

from src import domain
from src.presentation import widgets
from src.presentation.todo import (
    todo_list_view_model,
)
from src.presentation.todo.todo_edit_form import edit_form_base

__all__ = ("TodoListView",)


class TodoListView(widgets.ListView):
    def __init__(self, /, view_model: todo_list_view_model.TodoListViewModel):
        super().__init__(view_model)

        self._mark_complete_button = qtw.QPushButton("Mark Complete")
        self._mark_complete_button.clicked.connect(self.mark_complete)
        self._mark_complete_button.setMinimumWidth(100)
        self._mark_complete_button.setDisabled(True)

        self._refresh_button = qtw.QPushButton("Refresh")
        self._refresh_button.clicked.connect(self.refresh)
        self._refresh_button.setMinimumWidth(100)

        self._add_button = qtw.QPushButton("Add")
        self._add_button.clicked.connect(self.open_add_form)
        self._add_button.setMinimumWidth(100)

        self._edit_button = qtw.QPushButton("Edit")
        self._edit_button.clicked.connect(self.open_edit_form)
        self._edit_button.setMinimumWidth(100)
        self._edit_button.setDisabled(True)

        self._delete_button = qtw.QPushButton("Delete")
        self._delete_button.clicked.connect(self.delete)
        self._delete_button.setMinimumWidth(100)
        self._delete_button.setDisabled(True)

        spacer = qtw.QSpacerItem(20, 40, qtw.QSizePolicy.Expanding)

        button_layout = qtw.QHBoxLayout()
        button_layout.addItem(spacer)
        button_layout.addWidget(self._mark_complete_button)
        button_layout.addWidget(self._refresh_button)
        button_layout.addWidget(self._add_button)
        button_layout.addWidget(self._edit_button)
        button_layout.addWidget(self._delete_button)

        layout = qtw.QVBoxLayout()
        layout.addWidget(self._table)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self._table.selectionModel().selectionChanged.connect(self.on_selection_changed)

        self._popup: typing.Optional[qtw.QDialog] = None

    def delete(self) -> None:
        logger.debug("delete_button clicked.")
        if todo_id := self.selected_row_id:
            row = self.view_model.get_row(todo_id)
            assert row is not None
            assert len(row) >= 1
            description = row[1]
            confirmation = qtw.QMessageBox.question(
                self,
                "Confirm Delete",
                f"Are you sure you want to delete {description!r}?",
                qtw.QMessageBox.Yes | qtw.QMessageBox.No,
                qtw.QMessageBox.No,
            )
            if confirmation == qtw.QMessageBox.Yes:
                self.view_model.delete(todo_id)
            else:
                logger.debug(
                    f"User did not confirm they wanted to delete {description}."
                )
        else:
            logger.debug("Nothing is selected.")

    def mark_complete(self) -> None:
        logger.debug("mark_complete_button clicked.")
        if todo_id := self.selected_row_id:
            self.view_model.mark_complete(todo_id)
        else:
            logger.debug("Nothing is selected.")

    def on_selection_changed(self) -> None:
        if todo := self.selected_todo():
            if todo.display():
                self._mark_complete_button.setText("Mark Complete")
            else:
                self._mark_complete_button.setText("Mark Incomplete")
            self._mark_complete_button.setDisabled(False)
            self._edit_button.setDisabled(False)
            self._delete_button.setDisabled(False)
        else:
            self._mark_complete_button.setDisabled(True)
            self._edit_button.setDisabled(True)
            self._delete_button.setDisabled(True)

    def open_add_form(self) -> None:
        logger.debug(f"opening add form")
        model = self.view_model.create_add_todo_form_model()
        self._popup = edit_form_base.EditFormBase(model)
        self._popup.exec()

    def open_edit_form(self) -> None:
        if todo_id := self.selected_row_id:
            logger.debug(f"opening edit form for todo id {todo_id}")
            model = self.view_model.create_edit_todo_form_model(todo_id)
            self._popup = edit_form_base.EditFormBase(model)
            self._popup.exec()
        else:
            logger.debug("Nothing is selected.")

    def selected_todo(self) -> typing.Optional[domain.Todo]:
        if todo_id := self.selected_row_id:
            return self.view_model.get_todo(todo_id)
        return None
