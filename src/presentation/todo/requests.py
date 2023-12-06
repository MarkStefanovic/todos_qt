import dataclasses

from src import domain

__all__ = (
    "DeleteTodo",
    "EditTodo",
    "ToggleCompleted",
)


@dataclasses.dataclass(frozen=True, kw_only=True)
class DeleteTodo:
    todo: domain.Todo


@dataclasses.dataclass(frozen=True, kw_only=True)
class EditTodo:
    todo: domain.Todo


@dataclasses.dataclass(frozen=True, kw_only=True)
class ToggleCompleted:
    todo: domain.Todo
