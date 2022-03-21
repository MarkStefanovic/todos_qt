from __future__ import annotations

import dataclasses

from src import domain

__all__ = ("TodoDashState",)


@dataclasses.dataclass(frozen=True)
class TodoDashState:
    description_filter: str
    selected_todo_id: str | None

    @staticmethod
    def initial() -> TodoDashState:
        return TodoDashState(
            description_filter="",
            selected_todo_id=None,
        )
