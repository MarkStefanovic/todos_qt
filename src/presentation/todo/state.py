from __future__ import annotations

import dataclasses

from src import domain
from src.presentation.todo.dash.state import TodoDashState
from src.presentation.todo.form.state import TodoFormState

__all__ = ("TodoState",)


@dataclasses.dataclass(frozen=True)
class TodoState:
    dash_state: TodoDashState
    form_state: TodoFormState
    dash_active: bool

    @staticmethod
    def initial(
        *,
        todos: list[domain.Todo],
        category_options: list[domain.Category],
        user_options: list[domain.User],
        current_user: domain.User,
    ) -> TodoState:
        return TodoState(
            dash_state=TodoDashState.initial(
                todos=todos,
                category_options=category_options,
                user_options=user_options,
                current_user=current_user,
            ),
            form_state=TodoFormState.initial(
                category_options=category_options,
                user_options=user_options,
                current_user=current_user,
            ),
            dash_active=True,
        )
