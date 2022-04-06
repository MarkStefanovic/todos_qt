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
        return domain.DEFAULT_USER
