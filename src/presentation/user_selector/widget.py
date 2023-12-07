from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa

from src import service, domain
from src.presentation.user_selector.controller import UserSelectorController
from src.presentation.user_selector.view import UserSelectorView

__all__ = ("UserSelectorWidget",)


class UserSelectorWidget(qtw.QWidget):
    item_selected = qtc.pyqtSignal(domain.User)

    def __init__(
        self,
        *,
        user_service: service.UserService,
        include_all_user: bool,
        parent: qtw.QWidget | None,
    ):
        super().__init__(parent=parent)

        self._view = UserSelectorView(parent=self)

        self._controller = UserSelectorController(
            view=self._view,
            user_service=user_service,
            include_all_user=include_all_user,
            parent=self,
        )

        self._view.item_selected.connect(self.item_selected)

    def get_selected_item(self) -> domain.User:
        return self._view.get_selected_item()

    def refresh(self) -> None | domain.Error:
        return self._controller.refresh()
