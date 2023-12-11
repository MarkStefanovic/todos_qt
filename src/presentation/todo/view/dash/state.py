import dataclasses

from src import domain

__all__ = ("TodoDashState",)


@dataclasses.dataclass(frozen=True, kw_only=True)
class TodoDashState:
    added_todo: domain.Todo | None
    category_filter: domain.Category
    categories_stale: bool
    deleted_todo: domain.Todo | None
    description_filter: str
    due_filter: bool
    selected_todo: domain.Todo
    todos: tuple[domain.Todo, ...]
    updated_todo: domain.Todo | None
    user_filter: domain.User
    users_stale: bool
    status: str
