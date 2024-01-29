import typing

from PyQt6 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa
from loguru import logger

from src import domain
from src.presentation.user_selector.state import UserSelectorState

__all__ = ("UserSelectorController",)


class UserSelectorController(qtc.QObject):
    states = qtc.pyqtSignal(UserSelectorState)

    def __init__(
        self,
        *,
        user_service: domain.UserService,
        include_all_user: bool,
        refresh_request: qtc.pyqtBoundSignal,
        parent: qtc.QObject | None,
    ):
        super().__init__(parent=parent)

        self._user_service: typing.Final[domain.UserService] = user_service
        self._include_all_user: typing.Final[bool] = include_all_user

        refresh_request.connect(self._on_refresh_request)

    def _on_refresh_request(self) -> None:
        logger.debug(f"{self.__class__.__name__}._on_refresh_request()")

        try:
            users = self._user_service.where(active=True)
            if isinstance(users, domain.Error):
                logger.error(f"{self.__class__.__name__}.refresh() failed: {users!s}")

                self.states.emit(UserSelectorState(error=users))

                return None

            if self._include_all_user:
                users.insert(0, domain.ALL_USER)

            self.states.emit(UserSelectorState(users=tuple(users)))
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.refresh() failed: {e!s}")

            self.states.emit(UserSelectorState(error=domain.Error.new(str(e))))
