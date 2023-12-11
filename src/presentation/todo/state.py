from __future__ import annotations

import dataclasses

from src.presentation.todo.view.dash.state import TodoDashState
from src.presentation.todo.view.form.state import TodoFormState

__all__ = ("TodoState",)


@dataclasses.dataclass(frozen=True)
class TodoState:
    dash_state: TodoDashState
    form_state: TodoFormState
    dash_active: bool
