from __future__ import annotations

import dataclasses

__all__ = ("UserState",)


@dataclasses.dataclass(frozen=True)
class UserState:
    dash_state: UserDashState
    form_state: UserFormState
    dash_active: bool

    @staticmethod
    def initial() -> UserState:
        return UserState(
            dash_state=UserDashState.initial(),
            form_state=UserFormState.initial(),
            dash_active=True,
        )
