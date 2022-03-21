from __future__ import annotations

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw

from src.presentation.main.state import MainState
from src.presentation.todo.view import TodoView

__all__ = ("MainView",)


class MainView(qtw.QDialog):
    def __init__(self, *, window_icon: qtg.QIcon):
        super().__init__()

        state = MainState.initial()

        self.setWindowTitle("Todos")

        self.setWindowIcon(window_icon)

        # noinspection PyTypeChecker
        self.setWindowFlags(
            self.windowFlags()
            | qtc.Qt.WindowMinimizeButtonHint
            | qtc.Qt.WindowMaximizeButtonHint
            | qtc.Qt.WindowSystemMenuHint
        )

        todo_view = TodoView(state=state.todo_state)

        # self._tabs = qtw.QTabWidget()
        # self._tabs.addTab(self._todo_view, "Todos")
        # self._tabs.addTab(self._reminder_view, "Reminders")

        layout = qtw.QHBoxLayout()
        layout.addWidget(todo_view)

        self.setLayout(layout)

        # self.setCentralWidget(self._tabs)

        # menu = self.menuBar()
        # file_menu = menu.addMenu("File")
        # file_menu.addAction("Open", self.select_file)
        # file_menu.addAction("Save", self.save)
        # edit_menu = menu.addMenu("Edit")
        # edit_menu.addAction("Insert Above", self.insert_above)
        # edit_menu.addAction("Insert Below", self.insert_below)
        # edit_menu.addAction("Remove Row(s)", self.remove_rows)
