from __future__ import annotations

import dataclasses
import datetime

from src import domain

__all__ = ("TodoDashState",)


@dataclasses.dataclass(frozen=True)
class TodoDashState:
    date_filter: datetime.date
    due_filter: bool
    description_filter: str
    category_filter: domain.TodoCategory
    selected_todo: domain.Todo | None
    todos: list[domain.Todo]

    @staticmethod
    def initial() -> TodoDashState:
        return TodoDashState(
            date_filter=datetime.date.today(),
            due_filter=True,
            description_filter="",
            category_filter=domain.TodoCategory.All,
            selected_todo=None,
            todos=[],
        )
