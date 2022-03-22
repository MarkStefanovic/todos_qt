from __future__ import annotations

import enum

__all__ = ("TodoCategory",)


class TodoCategory(enum.Enum):
    Birthday = "birthday"
    Holiday = "holiday"
    Reminder = "reminder"
    Todo = "todo"
