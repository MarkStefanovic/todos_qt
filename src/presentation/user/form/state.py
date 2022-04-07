from __future__ import annotations

import dataclasses
import datetime

from src import domain

__all__ = ("UserFormState",)


@dataclasses.dataclass(frozen=True)
class UserFormState:
    user_id: str
    username: str
    display_name: str
    is_admin: bool
    date_added: datetime.datetime
    date_updated: datetime.datetime | None

    @staticmethod
    def initial() -> UserFormState:
        return UserFormState(
            user_id=domain.create_uuid(),
            username="",
            display_name="",
            is_admin=False,
            date_added=datetime.datetime.now(),
            date_updated=None,
        )

    @staticmethod
    def from_domain(*, user: domain.User) -> UserFormState:
        return UserFormState(
            user_id=user.user_id,
            username=user.username,
            display_name=user.display_name,
            is_admin=user.is_admin,
            date_added=user.date_added,
            date_updated=user.date_updated,
        )

    def to_domain(self) -> domain.User:
        return domain.User(
            user_id=self.user_id,
            username=self.username,
            display_name=self.display_name,
            is_admin=self.is_admin,
            date_added=self.date_added,
            date_updated=self.date_updated,
        )
