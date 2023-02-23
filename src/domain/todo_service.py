from __future__ import annotations

import abc
import datetime

from src.domain.user import User
from src.domain.todo import Todo

__all__ = ("TodoService",)


class TodoService(abc.ABC):
    @abc.abstractmethod
    def add(self, *, todo: Todo) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def add_default_holidays_for_all_users(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def cleanup(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, *, todo_id: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, *, todo_id: str) -> Todo | None:
        raise NotImplementedError

    @abc.abstractmethod
    def where(
        self,
        *,
        due_filter: bool,
        description_like: str,
        category_id_filter: str | None,
        user_id_filter: str | None,
    ) -> list[Todo]:
        raise NotImplementedError

    @abc.abstractmethod
    def mark_complete(self, *, todo_id: str, user: User | None) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def mark_incomplete(self, *, todo_id: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def refresh(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, *, todo: Todo) -> None:
        raise NotImplementedError
