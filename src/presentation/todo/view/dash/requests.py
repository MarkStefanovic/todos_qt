import dataclasses

# noinspection PyPep8Naming
from PyQt5 import QtCore as qtc

from src import domain

__all__ = (
    "AddTodo",
    "DeleteTodo",
    "EditTodo",
    "RefreshRequest",
    "ToggleCompleted",
    "TodoDashRequests",
)


@dataclasses.dataclass(frozen=True, kw_only=True)
class AddTodo:
    todo: domain.Todo


@dataclasses.dataclass(frozen=True, kw_only=True)
class DeleteTodo:
    todo: domain.Todo


@dataclasses.dataclass(frozen=True, kw_only=True)
class EditTodo:
    todo: domain.Todo


@dataclasses.dataclass(frozen=True, kw_only=True)
class RefreshRequest:
    is_due: bool
    description: str
    category: domain.Category
    user: domain.User


@dataclasses.dataclass(frozen=True, kw_only=True)
class ToggleCompleted:
    todo: domain.Todo


class TodoDashRequests(qtc.QObject):
    add = qtc.pyqtSignal()
    delete = qtc.pyqtSignal(DeleteTodo)
    edit = qtc.pyqtSignal(EditTodo)
    refresh = qtc.pyqtSignal(RefreshRequest)
    toggle_completed = qtc.pyqtSignal(ToggleCompleted)
