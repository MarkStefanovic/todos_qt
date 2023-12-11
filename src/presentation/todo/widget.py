import typing

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa

from src import service, domain
from src.presentation.todo.view.view import TodoView
from src.presentation.todo.controller import TodoController


class TodoWidget(qtw.QWidget):
    def __init__(
        self,
        *,
        todo_service: service.TodoService,
        current_user: domain.User,
        parent: qtw.QWidget | None,
    ):
        super().__init__(parent=parent)

        self._view = TodoView(parent=self)

        self._controller = TodoController(
            todo_service=todo_service,
            current_user=current_user,
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
