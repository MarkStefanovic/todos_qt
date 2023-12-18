from __future__ import annotations

import dataclasses

from src import domain

__all__ = ("UserDashState",)


@dataclasses.dataclass(frozen=True, kw_only=True)
class UserDashState:
    users: list[domain.User] | domain.Unspecified = domain.Unspecified()
    current_user: domain.User | domain.Unspecified = domain.Unspecified()
    selected_user: domain.User | None | domain.Unspecified = domain.Unspecified()
    status: str | domain.Unspecified = domain.Unspecified()

    @staticmethod
    def initial() -> UserDashState:
        return UserDashState(
            users=[],
            current_user=domain.DEFAULT_USER,
            selected_user=None,
            status="",
        )
