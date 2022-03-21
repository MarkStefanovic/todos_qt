from __future__ import annotations

import dataclasses

from src.presentation.todo.dash.state import TodoDashState
from src.presentation.todo.form.state import TodoFormState

__all__ = ("TodoState",)


@dataclasses.dataclass(frozen=True)
class TodoState:
    dash_state: TodoDashState
    form_state: TodoFormState
    dash_active: bool

    @staticmethod
    def initial() -> TodoState:
        return TodoState(
            dash_state=TodoDashState.initial(),
            form_state=TodoFormState.initial(),
            dash_active=True,
        )
