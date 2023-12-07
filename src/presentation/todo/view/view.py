from __future__ import annotations

import typing

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa


from src.presentation.todo.state import TodoState
from src.presentation.todo.view.dash import TodoDash
from src.presentation.todo.view.form.view import TodoForm


__all__ = ("TodoView",)


class TodoView(qtw.QWidget):
    def __init__(self, *, parent: qtw.QWidget | None = None):
        super().__init__(parent=parent)

        self.dash = TodoDash(parent=self)
        self.form = TodoForm(parent=self)

        self.stacked_layout = qtw.QStackedLayout()
        self.stacked_layout.addWidget(self.dash)
        self.stacked_layout.addWidget(self.form)

        self.setLayout(self.stacked_layout)

    def refresh_dash(self) -> None:
        self.dash.refresh_requests.emit()

    def get_state(self) -> TodoState:
        return TodoState(
            dash_state=self.dash.get_state(),
            form_state=self.form.get_state(),
            dash_active=self.stacked_layout.currentIndex() == 0,
        )

    def save_form(self) -> None:
        self.form.save_btn.click()

    def set_state(self, *, state: TodoState) -> None:
        self.dash.set_state(state=state.dash_state)
        self.form.set_state(state=state.form_state)
        if state.dash_active:
            self.stacked_layout.setCurrentIndex(0)
        else:
            self.stacked_layout.setCurrentIndex(1)

    def current_view(self) -> typing.Literal["dash", "form"]:
        if self.stacked_layout.currentIndex() == 0:
            return "dash"
        return "form"
