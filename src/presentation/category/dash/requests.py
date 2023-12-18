import dataclasses

# noinspection PyPep8Naming
from PyQt5 import QtCore as qtc

from src import domain

__all__ = (
    "CategoryDashRequests",
    "Delete",
    "Edit",
)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Delete:
    category: domain.Category


@dataclasses.dataclass(frozen=True, kw_only=True)
class Edit:
    category: domain.Category


@dataclasses.dataclass(frozen=True, kw_only=True)
class CategoryDashRequests(qtc.QObject):
    add = qtc.pyqtSignal()
    delete = qtc.pyqtSignal(Delete)
    edit = qtc.pyqtSignal(Edit)
    refresh = qtc.pyqtSignal()
