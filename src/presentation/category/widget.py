import typing

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa

from src import service, domain
from src.presentation.category import form, dash
from src.presentation.category.controller import CategoryController
from src.presentation.category.view import CategoryView


__all__ = ("CategoryWidget",)


class CategoryWidget(qtw.QWidget):
    def __init__(
        self,
        *,
        category_service: service.CategoryService,
        current_user: domain.User,
        parent: qtw.QWidget | None,
    ):
        super().__init__(parent=parent)

        self._dash_requests: typing.Final[dash.requests.CategoryDashRequests] = dash.requests.CategoryDashRequests()

        self._form_requests: typing.Final[form.requests.CategoryFormRequests] = form.requests.CategoryFormRequests()

        self._controller = CategoryController(
            category_service=category_service,
            dash_requests=self._dash_requests,
            form_requests=self._form_requests,
            parent=self,
        )

        self._view = CategoryView(
            current_user=current_user,
            dash_requests=self._dash_requests,
            form_requests=self._form_requests,
            states=self._controller.states,
            parent=self,
        )

        layout = qtw.QStackedLayout()
        layout.addWidget(self._view)
        self.setLayout(layout)

    def current_view(self) -> typing.Literal["dash", "form"]:
        return self._view.current_view()

    def refresh_dash(self) -> None:
        return self._controller.refresh()

    def save_form(self) -> None:
        return self._view.save_form()
