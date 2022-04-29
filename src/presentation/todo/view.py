from __future__ import annotations

from PyQt5 import QtWidgets as qtw

from src.presentation.todo.state import TodoState
from src.presentation.todo.dash.view import TodoDash
from src.presentation.todo.form.view import TodoForm

__all__ = ("TodoView",)


class TodoView(qtw.QWidget):
    def __init__(self, *, parent: qtw.QWidget | None = None):
        super().__init__(parent=parent)

        self.dash = TodoDash()
        self.form = TodoForm()

        self.stacked_layout = qtw.QStackedLayout()
        self.stacked_layout.addWidget(self.dash)
        self.stacked_layout.addWidget(self.form)

        self.setLayout(self.stacked_layout)

    def get_state(self) -> TodoState:
        return TodoState(
            dash_state=self.dash.get_state(),
            form_state=self.form.get_state(),
            dash_active=self.stacked_layout.currentIndex() == 0,
        )

    def set_state(self, *, state: TodoState) -> None:
        self.dash.set_state(state=state.dash_state)
        self.form.set_state(state=state.form_state)
        if state.dash_active:
            self.stacked_layout.setCurrentIndex(0)
        else:
            self.stacked_layout.setCurrentIndex(1)
