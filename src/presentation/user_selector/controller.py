import typing

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa
from loguru import logger

from src import domain, service
from src.presentation.user_selector.state import UserSelectorState

__all__ = ("UserSelectorController",)


class UserSelectorController(qtc.QObject):
    states = qtc.pyqtSignal(UserSelectorState)

    def __init__(
        self,
        *,
        user_service: service.UserService,
        include_all_user: bool,
        parent: qtc.QObject | None,
    ):
        super().__init__(parent=parent)

        self._user_service: typing.Final[service.UserService] = user_service
        self._include_all_user: typing.Final[bool] = include_all_user

    def refresh(self) -> None:
        logger.debug(f"{self.__class__.__name__}.refresh()")

        try:
            users = self._user_service.where(active=True)
            if isinstance(users, domain.Error):
                logger.error(f"{self.__class__.__name__}.refresh() failed: {users!s}")

                self.states.emit(UserSelectorState(error=domain.Error.new(str(users))))

                return None

            if self._include_all_user:
                users.insert(0, domain.ALL_USER)

            self.states.emit(UserSelectorState(users=tuple(users)))
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.refresh() failed: {e!s}")

            self.states.emit(UserSelectorState(error=domain.Error.new(str(e))))
