from PyQt5 import QtWidgets as qtw

from src.presentation.todo.state import TodoState
from src.presentation.todo.dash.view import TodoDash
from src.presentation.todo.form.view import TodoForm

__all__ = ("TodoView",)


class TodoView(qtw.QWidget):
    def __init__(self, *, state: TodoState):
        super().__init__()

        self._dash = TodoDash(state=state.dash_state)
        self._form = TodoForm(state=state.form_state)

        self._stacked_layout = qtw.QStackedLayout()
        self._stacked_layout.addWidget(self._dash)
        self._stacked_layout.addWidget(self._form)

        self.setLayout(self._stacked_layout)

    def get_state(self) -> TodoState:
        return TodoState(
            dash_state=self._dash.get_state(),
            form_state=self._form.get_state(),
            dash_active=self._stacked_layout.currentIndex() == 0,
        )

    def set_state(self, *, state: TodoState) -> None:
        self._dash.set_state(state=state.dash_state)
        self._form.set_state(state=state.form_state)
        if state.dash_active:
            self._stacked_layout.setCurrentIndex(0)
        else:
            self._stacked_layout.setCurrentIndex(1)
