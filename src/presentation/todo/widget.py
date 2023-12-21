import typing

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa

from src import domain
from src.presentation.category_selector import CategorySelectorWidget
from src.presentation.todo.controller import TodoController
from src.presentation.todo.view.dash.requests import TodoDashRequests
from src.presentation.todo.view.form.requests import TodoFormRequests
from src.presentation.todo.view.view import TodoView
from src.presentation.user_selector import UserSelectorWidget

__all__ = ("TodoWidget",)


class TodoWidget(qtw.QWidget):
    def __init__(
        self,
        *,
        category_service: domain.CategoryService,
        todo_service: domain.TodoService,
        user_service: domain.UserService,
        current_user: domain.User,
        parent: qtw.QWidget | None,
    ):
        super().__init__(parent=parent)

        self._controller_thread = qtc.QThread(parent=self)

        dash_requests = TodoDashRequests(parent=self)

        form_requests = TodoFormRequests(parent=self)

        self._controller: typing.Final[TodoController] = TodoController(
            todo_service=todo_service,
            current_user=current_user,
            dash_requests=dash_requests,
            form_requests=form_requests,
            parent=self,
        )

        self._controller.moveToThread(self._controller_thread)

        self._dash_category_selector = CategorySelectorWidget(
            category_service=category_service,
            include_all_category=True,
            parent=self,
        )

        self._form_category_selector = CategorySelectorWidget(
            category_service=category_service,
            include_all_category=False,
            parent=self,
        )

        self._dash_user_selector = UserSelectorWidget(
            user_service=user_service,
            include_all_user=True,
            parent=self,
        )

        self._form_user_selector = UserSelectorWidget(
            user_service=user_service,
            include_all_user=False,
            parent=self,
        )

        self._view: typing.Final[TodoView] = TodoView(
            states=self._controller.states,
            dash_requests=dash_requests,
            form_requests=form_requests,
            current_user=current_user,
            dash_category_selector=self._dash_category_selector,
            form_category_selector=self._form_category_selector,
            dash_user_selector=self._dash_user_selector,
            form_user_selector=self._form_user_selector,
            parent=self,
        )

        layout = qtw.QStackedLayout()
        layout.addWidget(self._view)
        self.setLayout(layout)

    def current_view(self) -> typing.Literal["dash", "form"]:
        return self._view.current_view()

    def refresh_categories(self) -> None:
        self._dash_category_selector.refresh()
        self._form_category_selector.refresh()

    def refresh_dash(self) -> None:
        self._view.refresh_dash()

    def refresh_users(self) -> None:
        self._dash_user_selector.refresh()
        self._form_user_selector.refresh()

    def save_form(self) -> None:
        self._view.save_form()
