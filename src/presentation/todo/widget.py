import typing

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa

from src import service
from src.presentation.todo.view import TodoView
from src.presentation.todo.controller import TodoController


class TodoWidget(qtw.QWidget):
    def __init__(
        self,
        *,
        category_service: service.CategoryService,
        todo_service: service.TodoService,
        user_service: service.UserService,
        parent: qtw.QWidget | None,
    ):
        super().__init__(parent=parent)

        self._view = TodoView(parent=self)

        self._controller = TodoController(
            category_service=category_service,
            todo_service=todo_service,
            user_service=user_service,
            view=self._view,
        )

        layout = qtw.QStackedLayout()
        layout.addWidget(self._view)
        self.setLayout(layout)

    def current_view(self) -> typing.Literal["dash", "form"]:
        return self._view.current_view()

    def refresh_dash(self) -> None:
        self._view.refresh_dash()

    def save_form(self) -> None:
        self._view.save_form()

    def show_current_user_todos(self) -> None:
        return self._controller.show_current_user_todos()
