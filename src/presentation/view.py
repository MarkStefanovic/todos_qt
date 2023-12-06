from __future__ import annotations

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa

from src.presentation.category.widget import CategoryWidget
from src.presentation.shared import fonts
from src.presentation.todo.widget import TodoWidget

__all__ = ("MainView",)


class MainView(qtw.QWidget):
    def __init__(
        self,
        *,
        category_widget: CategoryWidget,
        todo_widget: TodoWidget,
    ):
        super().__init__()

        self._todos = todo_widget
        self._categories = category_widget
        # self.users = UserView()

        self._tabs = qtw.QTabWidget()
        self._tabs.setFont(fonts.BOLD)
        self._tabs.addTab(self._todos, "Todo")
        self._tabs.addTab(self._categories, "Category")
        # self._tabs.addTab(self.users, "Users")
        # noinspection PyUnresolvedReferences

        layout = qtw.QVBoxLayout()
        layout.addWidget(self._tabs)
        self.setLayout(layout)

        # noinspection PyUnresolvedReferences
        self._tabs.currentChanged.connect(self._on_tab_changed)

        self.enter_key_shortcut = qtw.QShortcut(qtg.QKeySequence(qtc.Qt.Key_Return), self)
        # noinspection PyUnresolvedReferences
        self.enter_key_shortcut.activated.connect(self._on_enter_key_pressed)

    def on_load(self) -> None:
        self._todos.refresh_dash()

    def _on_enter_key_pressed(self) -> None:
        if (ix := self._tabs.currentIndex()) == 0:
            if self._todos.current_view() == "dash":
                self._todos.refresh_dash()
            else:
                self._todos.save_form()
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
            if self._todos.current_view() == "dash":
                self._todos.refresh_dash()
        elif ix == 1:
            if self.categories.stacked_layout.currentIndex() == 0:
                self.categories.dash.refresh_btn.click()
        else:
            if self.users.stacked_layout.currentIndex() == 0:
                self.users.dash.refresh_btn.click()
