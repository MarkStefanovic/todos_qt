import dataclasses

from src import domain

__all__ = ("TodoDashState",)


@dataclasses.dataclass(frozen=True, kw_only=True)
class TodoDashState:
    added_todo: domain.Todo | None = None
    category_filter: domain.Category | domain.Unspecified = domain.Unspecified()
    categories_stale: bool | domain.Unspecified = domain.Unspecified()
    deleted_todo: domain.Todo | None = None
    description_filter: str | domain.Unspecified = domain.Unspecified()
    due_filter: bool | domain.Unspecified = domain.Unspecified()
    selected_todo: domain.Todo | domain.Unspecified = domain.Unspecified()
    todos: tuple[domain.Todo, ...] | domain.Unspecified = domain.Unspecified()
    updated_todo: domain.Todo | None = None
    user_filter: domain.User | domain.Unspecified = domain.Unspecified()
    users_stale: bool | domain.Unspecified = domain.Unspecified()
    status: str | domain.Unspecified = domain.Unspecified()
