from __future__ import annotations

import dataclasses
import datetime

from src import domain

__all__ = ("ALL_CATEGORY", "TodoDashState")


ALL_CATEGORY = domain.Category(
    category_id="",
    name="All",
    note="",
    date_added=datetime.datetime(1900, 1, 1),
    date_updated=None,
    date_deleted=None,
)


@dataclasses.dataclass(frozen=True)
class TodoDashState:
    date_filter: datetime.date
    due_filter: bool
    description_filter: str
    category_filter: domain.Category
    selected_todo: domain.Todo | None
    todos: list[domain.Todo]
    category_options: list[domain.Category]
    status: str

    @staticmethod
    def initial(*, todos: list[domain.Todo], category_options: list[domain.Category]) -> TodoDashState:
        return TodoDashState(
            date_filter=datetime.date.today(),
            due_filter=True,
            description_filter="",
            category_filter=ALL_CATEGORY,
            selected_todo=None,
            todos=todos,
            category_options=category_options,
            status="",
        )
