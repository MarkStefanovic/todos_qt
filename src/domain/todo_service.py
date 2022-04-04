import abc
import datetime

from src.domain.todo import Todo
from src.domain.category import Category

__all__ = ("TodoService",)


class TodoService(abc.ABC):
    @abc.abstractmethod
    def delete(self, *, todo_id: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> list[Todo]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_where(
        self,
        *,
        date_filter: datetime.date,
        due_filter: bool,
        description_like: str,
        category_filter: Category | None,
    ) -> list[Todo]:
        raise NotImplementedError

    @abc.abstractmethod
    def mark_complete(self, *, todo_id: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def mark_incomplete(self, *, todo_id: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def refresh(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def upsert(self, *, todo: Todo) -> None:
        raise NotImplementedError
