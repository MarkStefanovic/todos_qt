import dataclasses

# noinspection PyPep8Naming
from PyQt5 import QtCore as qtc

from src import domain

__all__ = (
    "CategoryFormRequests",
    "Save",
)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Save:
    category: domain.Category


@dataclasses.dataclass(frozen=True, kw_only=True)
class CategoryFormRequests:
    back: qtc.pyqtBoundSignal = qtc.pyqtSignal()
    save: qtc.pyqtBoundSignal = qtc.pyqtSignal(Save)
