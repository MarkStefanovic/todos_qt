from __future__ import annotations

import datetime
import typing

import pydantic

from src.presentation.todo.state import TodoState

__all__ = ("MainState",)


class MainState(pydantic.BaseModel):
    today: datetime.date
    active_tab: typing.Literal["todo"] | typing.Literal["completed"]
    todo_state: TodoState

    @staticmethod
    def initial() -> MainState:
        return MainState(
            today=datetime.date.today(),
            active_tab="todo",
            todo_state=TodoState.initial(),
        )
