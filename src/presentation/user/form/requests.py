import dataclasses

from src import domain

# noinspection PyPep8Naming
from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa: F401

__all__ = (
    "SaveRequest",
    "UserFormRequests",
)


@dataclasses.dataclass(frozen=True, kw_only=True)
class SaveRequest:
    user: domain.User


class UserFormRequests(qtc.QObject):
    back = qtc.pyqtSignal()
    save = qtc.pyqtSignal(SaveRequest)
