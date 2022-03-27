from __future__ import annotations

import enum

__all__ = ("TodoCategory",)


class TodoCategory(str, enum.Enum):
    Birthday = "Birthday"
    Holiday = "Holiday"
    Reminder = "Reminder"
    Todo = "Todo"

    def __str__(self) -> str:
        return str.__str__(self)
