from __future__ import annotations

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw

from src.presentation.main.state import MainState
from src.presentation.todo.view import TodoView

__all__ = ("MainView",)


class MainView(qtw.QDialog):
    def __init__(self, *, window_icon: qtg.QIcon):
        super().__init__()

        state = MainState.initial()

        self.setWindowTitle("ToDo")

        self.setWindowIcon(window_icon)

        # noinspection PyTypeChecker
        self.setWindowFlags(
            self.windowFlags()  # type: ignore
            | qtc.Qt.WindowMinimizeButtonHint
            | qtc.Qt.WindowMaximizeButtonHint
            | qtc.Qt.WindowSystemMenuHint
        )

        self.todos = TodoView(state=state.todo_state)

        layout = qtw.QHBoxLayout()
        layout.addWidget(self.todos)

        self.setLayout(layout)

        self.enter_key_shortcut = qtw.QShortcut(qtg.QKeySequence(qtc.Qt.Key_Return), self)
        self.enter_key_shortcut.activated.connect(self.todos.dash.refresh_btn.click)
