from __future__ import annotations

import dataclasses
import datetime
import typing

__all__ = (
    "ALL_USER",
    "DEFAULT_USER",
    "User",
)


@dataclasses.dataclass(frozen=True)
class User:
    user_id: str
    username: str
    display_name: str
    is_admin: bool
    date_added: datetime.datetime
    date_updated: datetime.datetime | None


DEFAULT_USER: typing.Final[User] = User(
    user_id="",
    username="",
    display_name="",
    is_admin=False,
    date_added=datetime.datetime(1900, 1, 1),
    date_updated=None,
)

ALL_USER: typing.Final[User] = User(
    user_id="",
    username="all",
    display_name="All",
    is_admin=False,
    date_added=datetime.datetime(1900, 1, 1),
    date_updated=None,
)
