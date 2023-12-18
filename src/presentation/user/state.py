from __future__ import annotations

import dataclasses

from src import domain
from src.presentation.user.dash.state import UserDashState
from src.presentation.user.form.state import UserFormState

__all__ = ("UserState",)


@dataclasses.dataclass(frozen=True)
class UserState:
    dash_state: UserDashState | domain.Unspecified = domain.Unspecified()
    form_state: UserFormState | domain.Unspecified = domain.Unspecified()
    dash_active: bool | domain.Unspecified = domain.Unspecified()

    @staticmethod
    def initial() -> UserState:
        return UserState(
            dash_state=UserDashState.initial(),
            form_state=UserFormState.initial(),
            dash_active=True,
        )
