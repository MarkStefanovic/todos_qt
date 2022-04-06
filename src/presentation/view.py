from __future__ import annotations

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw

from src.presentation.category.view import CategoryView
from src.presentation.todo.view import TodoView
from src.presentation.user.view import UserView

__all__ = ("MainView",)


class MainView(qtw.QDialog):
    def __init__(self, *, window_icon: qtg.QIcon):
        super().__init__()

        self.setWindowTitle("Todos")

        self.setWindowIcon(window_icon)

        # noinspection PyTypeChecker
        self.setWindowFlags(
            self.windowFlags()  # type: ignore
            | qtc.Qt.WindowMinimizeButtonHint
            | qtc.Qt.WindowMaximizeButtonHint
            | qtc.Qt.WindowSystemMenuHint
        )

        self.todos = TodoView()
        self.categories = CategoryView()
        self.users = UserView()

        self._tabs = qtw.QTabWidget()
        self._tabs.addTab(self.todos, "Todo")
        self._tabs.addTab(self.categories, "Category")
        self._tabs.addTab(self.users, "Users")
        self._tabs.currentChanged.connect(self._on_tab_changed)

        layout = qtw.QVBoxLayout()
        layout.addWidget(self._tabs)

        self.setLayout(layout)

        self.enter_key_shortcut = qtw.QShortcut(qtg.QKeySequence(qtc.Qt.Key_Return), self)
        self.enter_key_shortcut.activated.connect(self.todos.dash.refresh_btn.click)

    def _on_tab_changed(self) -> None:
        if (ix := self._tabs.currentIndex()) == 0:
            if self.todos.stacked_layout.currentIndex() == 0:
                self.todos.dash.refresh_btn.click()
        elif ix == 1:
            if self.categories.stacked_layout.currentIndex() == 0:
                self.categories.dash.refresh_btn.click()
        else:
            if self.users.stacked_layout.currentIndex() == 0:
                self.users.dash.refresh_btn.click()

