from __future__ import annotations

import dataclasses

from src import domain

__all__ = ("UserDashState",)


@dataclasses.dataclass(frozen=True, kw_only=True)
class UserDashState:
    users: list[domain.User] | domain.Unspecified = domain.Unspecified()
    selected_user: domain.User | None | domain.Unspecified = domain.Unspecified()
    status: str | domain.Unspecified = domain.Unspecified()

    @staticmethod
    def initial() -> UserDashState:
        return UserDashState(
            users=[],
            selected_user=None,
            status="",
        )
