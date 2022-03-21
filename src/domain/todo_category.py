from __future__ import annotations

import enum

__all__ = ("TodoCategory",)


class TodoCategory(enum.Enum):
    Birthday = "birthday"
    Holiday = "holiday"
    Reminder = "reminder"
    Todo = "todo"

    @property
    def db_name(self) -> str:
        return self.value

    @staticmethod
    def from_str(category: str) -> TodoCategory:
        if category == "holiday":
            return TodoCategory.Holiday
        elif category == "todo":
            return TodoCategory.Todo
        elif category == "reminder":
            return TodoCategory.Reminder
        else:
            raise ValueError(f"Unrecognized category: {category!r}")

    def to_str(self) -> str:
        return self.value

if __name__ == '__main__':
    for data in TodoCategory:
        data.value
