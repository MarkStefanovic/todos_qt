from __future__ import annotations

import typing

# noinspection PyPep8Naming
from PyQt5 import QtCore as qtc, QtWidgets as qtw
from loguru import logger

from src import domain
from src.presentation.category import dash, form
from src.presentation.category.state import CategoryState

__all__ = ("CategoryView",)


class CategoryView(qtw.QWidget):
    def __init__(
        self,
        *,
        user_is_admin: bool,
        dash_requests: dash.requests.CategoryDashRequests,
        form_requests: form.requests.CategoryFormRequests,
        states: qtc.pyqtBoundSignal,
        parent: qtw.QWidget | None = None,
    ):
        super().__init__(parent=parent)

        self._dash_requests: typing.Final[dash.requests.CategoryDashRequests] = dash_requests
        self._form_requests: typing.Final[form.requests.CategoryFormRequests] = form_requests

        self._dash = dash.CategoryDash(
            parent=self,
            user_is_admin=user_is_admin,
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

    def get_state(self) -> CategoryState | domain.Error:
        try:
            dash_state = self._dash.get_state()
            if isinstance(dash_state, domain.Error):
                return dash_state

            form_state = self._form.get_state()
            if isinstance(form_state, domain.Error):
                return form_state

            return CategoryState(
                dash_state=dash_state,
                form_state=form_state,
                dash_active=self.stacked_layout.currentIndex() == 0,
            )
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.get_state() failed: {e!s}")
            return domain.Error.new(str(e))

    def refresh_dash(self) -> None:
        self._dash.refresh()

    def save_form(self) -> None:
        self._form.save()

    def set_state(self, /, state: CategoryState) -> None | domain.Error:
        try:
            if isinstance(state.dash_state, dash.CategoryDashState):
                self._dash.set_state(state.dash_state)

            if isinstance(state.form_state, form.CategoryFormState):
                self._form.set_state(state.form_state)

            if isinstance(state.dash_active, bool):
                if state.dash_active:
                    self.stacked_layout.setCurrentIndex(0)
                else:
                    self.stacked_layout.setCurrentIndex(1)

            return None
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.set_state({state=!r}) failed: {e!s}")
            return domain.Error.new(str(e), state=state)
