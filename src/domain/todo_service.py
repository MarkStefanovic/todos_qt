import abc
import datetime

from src.domain.todo import Todo

__all__ = ("TodoService",)


class TodoService(abc.ABC):
    @abc.abstractmethod
    def delete(self, *, todo_id: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def where(
        self,
        *,
        date_filter: datetime.date,
        due_filter: bool,
        description_like: str,
        category_id_filter: str | None,
        user_id_filter: str | None,
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
