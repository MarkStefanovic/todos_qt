from __future__ import annotations

import typing

# noinspection PyPep8Naming
from PyQt5 import QtCore as qtc, QtWidgets as qtw


from src import domain
from src.presentation.category import dash, form
from src.presentation.category.state import CategoryState

__all__ = ("CategoryView",)


class CategoryView(qtw.QWidget, domain.View[CategoryState]):
    def __init__(
        self,
        *,
        current_user: domain.User,
        dash_requests: dash.requests.CategoryDashRequests,
        form_requests: form.requests.CategoryFormRequests,
        states: qtc.pyqtBoundSignal,
        parent: qtw.QWidget | None = None,
    ):
        super().__init__(parent=parent)

        self._current_user: typing.Final[domain.User] = current_user
        self._dash_requests: typing.Final[dash.requests.CategoryDashRequests] = dash_requests
        self._form_requests: typing.Final[form.requests.CategoryFormRequests] = form_requests

        self._dash = dash.CategoryDash(
            parent=self,
            current_user=current_user,
            dash_requests=dash_requests,
        )

        self._form = form.CategoryForm(
            parent=self,
            form_requests=form_requests,
        )

        self.stacked_layout = qtw.QStackedLayout()
        self.stacked_layout.addWidget(self._dash)
        self.stacked_layout.addWidget(self._form)

        self.setLayout(self.stacked_layout)

        states.connect(self.set_state)

    def current_view(self) -> typing.Literal["dash", "form"]:
        if self.stacked_layout.currentIndex() == 0:
            return "dash"
        return "form"

    def get_state(self) -> CategoryState:
        return CategoryState(
            dash_state=self._dash.get_state(),
            form_state=self._form.get_state(),
            dash_active=self.stacked_layout.currentIndex() == 0,
        )

    def refresh_dash(self) -> None:
        self._dash.refresh()

    def save_form(self) -> None:
        self._form.save()

    def set_state(self, /, state: CategoryState) -> None:
        if isinstance(state.dash_state, dash.CategoryDashState):
            self._dash.set_state(state.dash_state)

        if isinstance(state.form_state, form.CategoryFormState):
            self._form.set_state(state.form_state)

        if isinstance(state.dash_active, bool):
            if state.dash_active:
                self.stacked_layout.setCurrentIndex(0)
            else:
                self.stacked_layout.setCurrentIndex(1)
