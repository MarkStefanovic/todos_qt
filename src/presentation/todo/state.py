from __future__ import annotations

import dataclasses

from src import domain
from src.presentation.todo.view.dash.state import TodoDashState
from src.presentation.todo.view.form.state import TodoFormState

__all__ = ("TodoState",)


@dataclasses.dataclass(frozen=True)
class TodoState:
    dash_state: TodoDashState | domain.Unspecified = domain.Unspecified()
    form_state: TodoFormState | domain.Unspecified = domain.Unspecified()
    dash_active: bool | domain.Unspecified = domain.Unspecified()

    @staticmethod
    def set_status(status: str, /) -> TodoState:
        return TodoState(dash_state=TodoDashState(status=status))
