import typing

from PyQt6 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa

from src import domain
from src.presentation.category import form, dash
from src.presentation.category.controller import CategoryController
from src.presentation.category.view import CategoryView

__all__ = ("CategoryWidget",)


class CategoryWidget(qtw.QWidget):
    categories_updated = qtc.pyqtSignal()

    def __init__(
        self,
        *,
        user_is_admin: bool,
        category_service: domain.CategoryService,
        parent: qtw.QWidget | None,
    ):
        super().__init__(parent=parent)

        self._dash_requests: typing.Final[dash.requests.CategoryDashRequests] = dash.requests.CategoryDashRequests(
            parent=self
        )

        self._form_requests: typing.Final[form.requests.CategoryFormRequests] = form.requests.CategoryFormRequests(
            parent=self
        )

        self._controller = CategoryController(
            category_service=category_service,
            dash_requests=self._dash_requests,
            form_requests=self._form_requests,
        )
        self._controller_thread = qtc.QThread(parent=self)
        self._controller.moveToThread(self._controller_thread)

        self._view = CategoryView(
            user_is_admin=user_is_admin,
            dash_requests=self._dash_requests,
            form_requests=self._form_requests,
            states=self._controller.states,
            parent=self,
        )

        layout = qtw.QStackedLayout()
        layout.addWidget(self._view)
        self.setLayout(layout)

        self._controller.categories_updated.connect(self.categories_updated.emit)

    def current_view(self) -> typing.Literal["dash", "form"]:
        return self._view.current_view()

    def refresh_dash(self) -> None:
        return self._view.refresh_dash()

    def save_form(self) -> None:
        return self._view.save_form()
