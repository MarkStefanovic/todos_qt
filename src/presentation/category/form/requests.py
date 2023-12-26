import dataclasses

# noinspection PyPep8Naming
from PyQt6 import QtCore as qtc

from src import domain

__all__ = (
    "CategoryFormRequests",
    "Save",
)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Save:
    category: domain.Category


@dataclasses.dataclass(frozen=True, kw_only=True)
class CategoryFormRequests(qtc.QObject):
    back = qtc.pyqtSignal()
    save = qtc.pyqtSignal(Save)

    def __init__(self, *, parent: qtc.QObject | None):
        super().__init__(parent=parent)
