from __future__ import annotations

import abc

from src.domain.todo import Todo

__all__ = ("TodoRepository",)


class TodoRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, *, todo: Todo) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def all(self) -> list[Todo]:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, *, todo_id: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, *, todo_id: str) -> Todo | None:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, *, todo: Todo) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def where_category(self, *, category_id: str) -> list[Todo]:
        raise NotImplementedError
