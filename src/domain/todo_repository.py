import abc
import datetime
import typing

from src.domain import todo


__all__ = ("TodoRepository",)


class TodoRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, /, item: todo.Todo) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def all(self) -> typing.List[todo.Todo]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_id(self, /, todo_id: int) -> todo.Todo:
        raise NotImplementedError

    @abc.abstractmethod
    def mark_completed(
        self, item_id: int, today: datetime.date = datetime.date.today()
    ) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, /, item_id: int) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, /, item: todo.Todo) -> None:
        raise NotImplementedError
