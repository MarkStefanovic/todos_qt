import typing

from PyQt6 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa

from src import domain
from src.presentation.user_selector.controller import UserSelectorController
from src.presentation.user_selector.view import UserSelectorView

__all__ = ("UserSelectorWidget",)


class UserSelectorWidget(qtw.QWidget):
    item_selected = qtc.pyqtSignal(domain.User)

    def __init__(
        self,
        *,
        user_service: domain.UserService,
        include_all_user: bool,
        parent: qtw.QWidget | None,
    ):
        super().__init__(parent=parent)

        self._controller = UserSelectorController(
            user_service=user_service,
            include_all_user=include_all_user,
            parent=self,
        )

        self._view = UserSelectorView(
            item_selected_requests=self.item_selected,
            states=self._controller.states,
            parent=self,
        )

        layout = qtw.QStackedLayout()
        layout.addWidget(self._view)
        self.setLayout(layout)

        self.setFixedSize(self._view.size())

    def get_selected_item(self) -> domain.User:
        return self._view.get_selected_item()

    def refresh(self) -> None:
        self._controller.refresh()

    def select_item(self, /, item: domain.User) -> None:
        return self._view.select_item(item)

    def set_items(self, /, items: typing.Iterable[domain.User]) -> None:
        self._view.set_items(items)
