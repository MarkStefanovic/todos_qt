import typing

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa

from src import service
from src.presentation.category.controller import CategoryController
from src.presentation.category.view import CategoryView


__all__ = ("CategoryWidget",)


class CategoryWidget(qtw.QWidget):
    def __init__(
        self,
        *,
        category_service: service.CategoryService,
        user_service: service.UserService,
        parent: qtw.QWidget | None,
    ):
        super().__init__(parent=parent)

        self._view = CategoryView(parent=self)

        self._controller = CategoryController(
            category_service=category_service,
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
        return self._view.save_form()