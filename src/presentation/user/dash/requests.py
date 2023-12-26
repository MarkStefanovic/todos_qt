import dataclasses

# noinspection PyPep8Naming
from PyQt6 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa: F401

from src import domain

__all__ = (
    "DeleteRequest",
    "EditRequest",
    "UserDashRequests",
)


@dataclasses.dataclass(frozen=True, kw_only=True)
class DeleteRequest:
    user: domain.User


@dataclasses.dataclass(frozen=True, kw_only=True)
class EditRequest:
    user: domain.User


class UserDashRequests(qtc.QObject):
    add = qtc.pyqtSignal()
    delete = qtc.pyqtSignal(DeleteRequest)
    edit = qtc.pyqtSignal(EditRequest)
    refresh = qtc.pyqtSignal()
