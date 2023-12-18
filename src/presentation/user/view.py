import typing

# noinspection PyPep8Naming
from PyQt5 import QtCore as qtc, QtWidgets as qtw

from src import domain
from src.presentation.user import dash, form
from src.presentation.user.dash.view import UserDash
from src.presentation.user.form.view import UserForm
from src.presentation.user.state import UserState

__all__ = ("UserView",)


class UserView(qtw.QWidget):
    def __init__(
        self,
        *,
        states: qtc.pyqtBoundSignal,
        current_user: domain.User,
        parent: qtw.QWidget | None,
    ):
        super().__init__(parent=parent)

        self._states: typing.Final[qtc.pyqtBoundSignal] = states
        self._current_user: typing.Final[domain.User] = current_user

        dash_requests = dash.requests.UserDashRequests()

        form_requests = form.requests.UserFormRequests()

        self._dash = UserDash(
            parent=self,
            current_user=current_user,
            user_requests=dash_requests,
        )
        self._form = UserForm(
            parent=self,
            form_requests=form_requests,
        )

        self._stacked_layout = qtw.QStackedLayout()
        self._stacked_layout.addWidget(self._dash)
        self._stacked_layout.addWidget(self._form)
        self.setLayout(self._stacked_layout)

        self._states.connect(self.set_state)

    @property
    def dash(self) -> UserDash:
        return self._dash

    @property
    def form(self) -> UserForm:
        return self._form

    def current_view(self) -> typing.Literal["dash", "form"]:
        if self._stacked_layout.currentIndex() == 0:
            return "dash"
        return "form"

    def get_state(self) -> UserState:
        return UserState(
            dash_state=self._dash.get_state(),
            form_state=self._form.get_state(),
            dash_active=self._stacked_layout.currentIndex() == 0,
        )

    def set_state(self, /, state: UserState) -> None:
        if not isinstance(state.dash_state, domain.Unspecified):
            self._dash.set_state(state=state.dash_state)

        if not isinstance(state.form_state, domain.Unspecified):
            self._form.set_state(state=state.form_state)

        if not isinstance(state.dash_active, domain.Unspecified):
            if state.dash_active:
                self._stacked_layout.setCurrentIndex(0)
            else:
                self._stacked_layout.setCurrentIndex(1)
