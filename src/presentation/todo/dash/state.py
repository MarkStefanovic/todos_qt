from __future__ import annotations

import dataclasses
import datetime

from src import domain

__all__ = ("ALL_CATEGORY", "ALL_USER", "TodoDashState")


ALL_CATEGORY = domain.Category(
    category_id="",
    name="All",
    note="",
    date_added=datetime.datetime(1900, 1, 1),
    date_updated=None,
    date_deleted=None,
)

ALL_USER = domain.User(
    user_id="",
    username="all",
    display_name="All",
    is_admin=False,
    date_added=datetime.datetime(1900, 1, 1),
    date_updated=None,
)


@dataclasses.dataclass(frozen=True)
class TodoDashState:
    due_filter: bool
    description_filter: str
    category_filter: domain.Category
    user_filter: domain.User
    selected_todo: domain.Todo | None
    todos: list[domain.Todo]
    category_options: list[domain.Category]
    user_options: list[domain.User]
    status: str
    current_user: domain.User

    @staticmethod
    def initial(
        *,
        todos: list[domain.Todo],
        category_options: list[domain.Category],
        user_options: list[domain.User],
        current_user: domain.User,
    ) -> TodoDashState:
        return TodoDashState(
            due_filter=True,
            description_filter="",
            category_filter=ALL_CATEGORY,
            user_filter=ALL_USER,
            selected_todo=None,
            todos=todos,
            category_options=category_options,
            user_options=user_options,
            status="",
            current_user=current_user,
        )
