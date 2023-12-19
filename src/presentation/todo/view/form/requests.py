import dataclasses

# noinspection PyPep8Naming
from PyQt5 import QtCore as qtc

from src import domain

__all__ = (
    "SaveRequest",
    "TodoFormRequests",
)


@dataclasses.dataclass(frozen=True, kw_only=True)
class SaveRequest:
    todo: domain.Todo


class TodoFormRequests(qtc.QObject):
    back = qtc.pyqtSignal()
    save = qtc.pyqtSignal(SaveRequest)
    error = qtc.pyqtSignal(domain.Error)
