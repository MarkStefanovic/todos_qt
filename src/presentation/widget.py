from __future__ import annotations

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa

from src import service
from src.presentation.todo.widget import TodoWidget
from src.presentation.view import MainView

__all__ = ("MainWidget",)


class MainWidget(qtw.QMainWindow):
    def __init__(
        self,
        *,
        window_icon: qtg.QIcon,
        username: str,
        category_service: service.CategoryService,
        todo_service: service.TodoService,
        user_service: service.UserService,
    ):
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

        # self.setWindowTitle(f"Todos - {username}")
        #
        # self.setWindowIcon(window_icon)
        #
        # # noinspection PyTypeChecker
        # self.setWindowFlags(
        #     self.windowFlags()
        #     | qtc.Qt.WindowMinimizeButtonHint
        #     | qtc.Qt.WindowMaximizeButtonHint
        #     | qtc.Qt.WindowSystemMenuHint
        # )

        todo_widget = TodoWidget(
            category_service=category_service,
            todo_service=todo_service,
            user_service=user_service,
            parent=self,
        )

        self._view = MainView(todo_widget=todo_widget)

        self.setCentralWidget(self._view)

        self._view.on_load()