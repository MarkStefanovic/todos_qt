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
class CategoryDashRequests:
    add: qtc.pyqtBoundSignal = qtc.pyqtSignal()
    delete: qtc.pyqtBoundSignal = qtc.pyqtSignal(Delete)
    edit: qtc.pyqtBoundSignal = qtc.pyqtSignal(Edit)
    refresh: qtc.pyqtBoundSignal = qtc.pyqtSignal()
