import typing

# noinspection PyPep8Naming
from PyQt5 import QtWidgets as qtw

from src import domain, service
from src.presentation.user.controller import UserController
from src.presentation.user.dash.requests import UserDashRequests
from src.presentation.user.form.requests import UserFormRequests
from src.presentation.user.view import UserView

__all__ = ("UserWidget",)


class UserWidget(qtw.QWidget):
    def __init__(
        self,
        *,
        current_user: domain.User,
        user_service: service.UserService,
        parent: qtw.QWidget | None,
    ):
        super().__init__(parent=parent)

        dash_requests: typing.Final[UserDashRequests] = UserDashRequests()

        form_requests: typing.Final[UserFormRequests] = UserFormRequests()

        self._controller = UserController(
            dash_requests=dash_requests,
            form_requests=form_requests,
            current_user=current_user,
            user_service=user_service,
            parent=self,
        )

        self._view = UserView(
            states=self._controller.states,
            current_user=current_user,
            parent=self,
        )

        layout = qtw.QStackedLayout()
        layout.addWidget(self._view)
        self.setLayout(layout)

    def current_view(self) -> typing.Literal["dash", "form"]:
        return self._view.current_view()

    def refresh_dash(self) -> None:
        self._view.dash.refresh()

    def save_form(self) -> None:
        self._view.form.save()
