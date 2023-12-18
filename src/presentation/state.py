import dataclasses
import typing

from src import domain
from src.presentation.category.state import CategoryState
from src.presentation.todo.state import TodoState

__all__ = ("MainState",)


@dataclasses.dataclass(frozen=True, kw_only=True)
class MainState:
    active_tab: typing.Literal["todo", "category", "user"] | domain.Unspecified = domain.Unspecified()
    category_state: CategoryState | domain.Unspecified = domain.Unspecified()
    todo_state: TodoState | domain.Unspecified = domain.Unspecified()
