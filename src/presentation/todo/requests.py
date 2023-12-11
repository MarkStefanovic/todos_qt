import dataclasses

from src import domain

__all__ = (
    "DeleteTodo",
    "EditTodo",
    "RefreshRequest",
    "ToggleCompleted",
)


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
class SaveRequest:
    todo: domain.Todo


@dataclasses.dataclass(frozen=True, kw_only=True)
class ToggleCompleted:
    todo: domain.Todo
