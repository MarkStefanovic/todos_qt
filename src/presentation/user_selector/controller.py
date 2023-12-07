import typing

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa
from loguru import logger

from src import service, domain
from src.presentation.user_selector.view import UserSelectorView

__all__ = ("UserSelectorController",)


class UserSelectorController(qtc.QObject):
    def __init__(
        self,
        *,
        view: UserSelectorView,
        user_service: service.UserService,
        include_all_user: bool,
        parent: qtc.QObject | None,
    ):
        super().__init__(parent=parent)

        self._view: typing.Final[UserSelectorView] = view
        self._user_service: typing.Final[service.UserService] = user_service
        self._include_all_user: typing.Final[bool] = include_all_user

    def refresh(self) -> None | domain.Error:
        logger.debug(f"{self.__class__.__name__}.refresh()")

        try:
            self._user_service.refresh()

            categories = self._user_service.all()

            if self._include_all_user:
                categories.insert(0, domain.ALL_USER)

            self._view.set_items(categories)

            return None
        except Exception as e:
            return domain.Error.new(str(e))
