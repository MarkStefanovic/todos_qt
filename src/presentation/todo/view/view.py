from __future__ import annotations

import typing

from PyQt6 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa

from src import domain
from src.presentation.category_selector.widget import CategorySelectorWidget
from src.presentation.todo.state import TodoState
from src.presentation.todo.view import dash, form
from src.presentation.user_selector.widget import UserSelectorWidget

__all__ = ("TodoView",)


class TodoView(qtw.QWidget):
    def __init__(
        self,
        *,
        states: qtc.pyqtBoundSignal,
        dash_requests: dash.requests.TodoDashRequests,
        form_requests: form.requests.TodoFormRequests,
        dash_category_selector: CategorySelectorWidget,
        form_category_selector: CategorySelectorWidget,
        dash_user_selector: UserSelectorWidget,
        form_user_selector: UserSelectorWidget,
        current_user: domain.User,
        parent: qtw.QWidget | None,
    ):
        super().__init__(parent=parent)

        self._states: typing.Final[qtc.pyqtBoundSignal] = states
        self._dash_requests: typing.Final[dash.requests.TodoDashRequests] = dash_requests
        self._form_requests: typing.Final[form.requests.TodoFormRequests] = form_requests

        self.dash = dash.TodoDashView(
            parent=self,
            current_user=current_user,
            todo_dash_requests=dash_requests,
            category_selector=dash_category_selector,
            user_selector=dash_user_selector,
        )

        self.form = form.TodoFormView(
            parent=self,
            form_requests=self._form_requests,
            category_selector=form_category_selector,
            user_selector=form_user_selector,
        )

        self.stacked_layout = qtw.QStackedLayout()
        self.stacked_layout.addWidget(self.dash)
        self.stacked_layout.addWidget(self.form)
        self.setLayout(self.stacked_layout)

        self._states.connect(self.set_state)

    def refresh_dash(self) -> None:
        self.dash.refresh()

    def get_state(self) -> TodoState | domain.Error:
        try:
            dash_state = self.dash.get_state()
            if isinstance(dash_state, domain.Error):
                return dash_state

            form_state = self.form.get_state()
            if isinstance(form_state, domain.Error):
                return form_state

            return TodoState(
                dash_state=dash_state,
                form_state=form_state,
                dash_active=self.stacked_layout.currentIndex() == 0,
            )
        except Exception as e:
            return domain.Error.new(str(e))

    def save_form(self) -> None:
        self.form.save_btn.click()

    def set_state(self, /, state: TodoState) -> None | domain.Error:
        try:
            if not isinstance(state.dash_state, domain.Unspecified):
                self.dash.set_state(state.dash_state)

            if not isinstance(state.form_state, domain.Unspecified):
                self.form.set_state(state.form_state)

            if not isinstance(state.dash_active, domain.Unspecified):
                if state.dash_active:
                    self.stacked_layout.setCurrentIndex(0)
                else:
                    self.stacked_layout.setCurrentIndex(1)

            return None
        except Exception as e:
            return domain.Error.new(str(e))

    def current_view(self) -> typing.Literal["dash", "form"]:
        if self.stacked_layout.currentIndex() == 0:
            return "dash"
        return "form"
