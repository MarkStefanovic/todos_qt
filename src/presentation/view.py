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

        self._tabs_loaded: set[int] = set()

    def on_load(self) -> None:
        self._todos.dash.refresh()
        self._tabs_loaded.add(0)

    def _on_enter_key_pressed(self) -> None:
        if (ix := self._tabs.currentIndex()) == 0:
            if self._todos.current_view() == "dash":
                self._todos.refresh_dash()
            else:
                self._todos.save_form()
        elif ix == 1:
            if self._categories.current_view() == "dash":
                self._categories.refresh_dash()
            else:
                self._categories.save_form()
        elif ix == 2:
            if self._users.current_view == "dash":
                self._users.refresh_dash()
            else:
                self._users.save_form()
        else:
            raise Exception(f"Unrecognized tab index: {ix}.")

    def _on_tab_changed(self) -> None:
        current_tab = self._tabs.currentIndex()
        if current_tab in self._tabs_loaded:
            return None

        if current_tab == 0:
            if self._todos.current_view() == "dash":
                self._todos.refresh_dash()
        elif current_tab == 1:
            if self._categories.current_view() == "dash":
                self._categories.refresh_dash()
        else:
            if self._users.current_view() == "dash":
                self._users._dash._refresh_btn.click()
