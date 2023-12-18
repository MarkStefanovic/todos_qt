from __future__ import annotations

import dataclasses
import datetime

from src import domain

__all__ = ("UserFormState",)


@dataclasses.dataclass(frozen=True)
class UserFormState:
    user_id: str | domain.Unspecified = domain.Unspecified()
    username: str | domain.Unspecified = domain.Unspecified()
    display_name: str | domain.Unspecified = domain.Unspecified()
    is_admin: bool | domain.Unspecified = domain.Unspecified()
    date_added: datetime.datetime | domain.Unspecified = domain.Unspecified()
    date_updated: datetime.datetime | None | domain.Unspecified = domain.Unspecified()

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

    def to_domain(self) -> domain.User | domain.Error:
        if isinstance(self.user_id, domain.Unspecified):
            return domain.Error.new("user_id is unspecified.")

        if isinstance(self.username, domain.Unspecified):
            return domain.Error.new("username is unspecified.")

        if isinstance(self.display_name, domain.Unspecified):
            return domain.Error.new("display_name is unspecified.")

        if isinstance(self.is_admin, domain.Unspecified):
            return domain.Error.new("is_admin is unspecified.")

        if isinstance(self.date_added, domain.Unspecified):
            return domain.Error.new("date_added is unspecified.")

        if isinstance(self.date_updated, domain.Unspecified):
            return domain.Error.new("date_updated is unspecified.")

        return domain.User(
            user_id=self.user_id,
            username=self.username,
            display_name=self.display_name,
            is_admin=self.is_admin,
            date_added=self.date_added,
            date_updated=self.date_updated,
        )
