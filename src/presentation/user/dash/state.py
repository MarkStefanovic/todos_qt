from __future__ import annotations

import dataclasses

from src import domain

__all__ = ("UserDashState",)


@dataclasses.dataclass(frozen=True)
class UserDashState:
    users: list[domain.User]
    current_user: domain.User
    status: str

    @staticmethod
    def initial() -> UserDashState:
        return UserDashState(
            users=[],
            current_user=domain.DEFAULT_USER,
            status="",
        )
