from __future__ import annotations

import dataclasses
import datetime
import typing

from src import domain
from src.presentation.category.state import CategoryState
from src.presentation.todo.state import TodoState

__all__ = ("MainState",)


@dataclasses.dataclass(frozen=True)
class MainState:
    active_tab: typing.Union[
        typing.Literal["todo"],
        typing.Literal["category"],
        typing.Literal["user"],
    ]
    category_state: CategoryState
    todo_state: TodoState

    @staticmethod
    def initial(
        *,
        todos: list[domain.Todo],
        category_options: list[domain.Category],
        user_options: list[domain.User],
        current_user: domain.User,
    ) -> MainState:
        return MainState(
            active_tab="todo",
            todo_state=TodoState.initial(
                todos=todos,
                category_options=category_options,
                user_options=user_options,
                current_user=current_user,
            ),
            category_state=CategoryState.initial(
                current_user=current_user,
            ),
        )
