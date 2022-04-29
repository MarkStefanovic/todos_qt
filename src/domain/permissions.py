from __future__ import annotations

from src.domain.category import Category, TODO_CATEGORY
from src.domain.holidays import HOLIDAY_CATEGORY
from src.domain.frequency_type import FrequencyType
from src.domain.todo import Todo
from src.domain.user import User

__all__ = (
    "user_can_edit_category",
    "user_can_edit_todo",
    "user_can_edit_user",
)


def user_can_edit_category(*, user: User | None, category: Category | None) -> bool:
    if user is None:
        return False

    if category is None:
        return False

    if category in (HOLIDAY_CATEGORY, TODO_CATEGORY):
        return False

    if user.is_admin:
        return True

    return False


def user_can_edit_todo(*, user: User | None, todo: Todo | None) -> bool:
    if user is None:
        return False

    if todo is None:
        return False

    if todo.frequency.name in {FrequencyType.Easter, FrequencyType.MemorialDay}:
        return False

    if user.is_admin:
        return True

    return False


def user_can_edit_user(*, current_user: User | None, user: User | None) -> bool:
    if current_user is None:
        return False

    if user is None:
        return False

    if current_user.is_admin:
        if user.is_admin:
            if current_user == user:
                return True
            return False
        return True

    return False
