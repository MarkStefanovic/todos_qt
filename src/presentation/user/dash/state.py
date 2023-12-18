from __future__ import annotations

import dataclasses

from src import domain

__all__ = ("UserDashState",)


@dataclasses.dataclass(frozen=True, kw_only=True)
class UserDashState:
    users: list[domain.User] | domain.Unspecified = domain.Unspecified()
    selected_user: domain.User | None | domain.Unspecified = domain.Unspecified()
    status: str | domain.Unspecified = domain.Unspecified()
    user_added: domain.User | None = None
    user_deleted: domain.User | None = None
    user_updated: domain.User | None = None

    @staticmethod
    def initial() -> UserDashState:
        return UserDashState(
            users=[],
            selected_user=None,
            status="",
            user_added=None,
            user_deleted=None,
            user_updated=None,
        )
