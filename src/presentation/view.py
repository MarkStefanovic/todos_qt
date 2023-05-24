from __future__ import annotations

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw

from src.presentation.category.view import CategoryView
from src.presentation.shared import fonts
from src.presentation.todo.view import TodoView
from src.presentation.user.view import UserView

__all__ = ("MainView",)


class MainView(qtw.QMainWindow):
    def __init__(self, *, window_icon: qtg.QIcon, username: str):
        super().__init__()

        self.setWindowTitle(f"Todos - {username}")

        self.setWindowIcon(window_icon)

        # noinspection PyTypeChecker
        self.setWindowFlags(
            self.windowFlags()
            | qtc.Qt.WindowMinimizeButtonHint
            | qtc.Qt.WindowMaximizeButtonHint
            | qtc.Qt.WindowSystemMenuHint
        )

        self.todos = TodoView()
        self.categories = CategoryView()
        self.users = UserView()

        self._tabs = qtw.QTabWidget()
        self._tabs.setFont(fonts.bold)
        self._tabs.addTab(self.todos, "Todo")
        self._tabs.addTab(self.categories, "Category")
        self._tabs.addTab(self.users, "Users")
        self._tabs.currentChanged.connect(self._on_tab_changed)

        self.setCentralWidget(self._tabs)

        self.enter_key_shortcut = qtw.QShortcut(qtg.QKeySequence(qtc.Qt.Key_Return), self)
        self.enter_key_shortcut.activated.connect(self._on_enter_key_pressed)

    def _on_enter_key_pressed(self) -> None:
        if (ix := self._tabs.currentIndex()) == 0:
            if (todo_ix := self.todos.stacked_layout.currentIndex()) == 0:
                self.todos.dash.refresh_btn.click()
            elif todo_ix == 1:
                self.todos.form.save_btn.click()
            else:
                raise Exception(f"Unrecognized todo stacked_layout index: {todo_ix}.")
        elif ix == 1:
            if (category_ix := self.categories.stacked_layout.currentIndex()) == 0:
                self.categories.dash.refresh_btn.click()
            elif category_ix == 1:
                self.categories.form.save_btn.click()
            else:
                raise Exception(f"Unrecognized category stacked_layout index: {category_ix}.")
        elif ix == 2:
            if (user_ix := self.todos.stacked_layout.currentIndex()) == 0:
                self.users.dash.refresh_btn.click()
            elif user_ix == 1:
                self.users.form.save_btn.click()
            else:
                raise Exception(f"Unrecognized user stacked_layout index: {user_ix}.")
        else:
            raise Exception(f"Unrecognized tab index: {ix}.")

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

