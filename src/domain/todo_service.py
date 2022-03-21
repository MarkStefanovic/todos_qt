import abc

from src.domain.todo import Todo

__all__ = ("TodoService",)


class TodoService(abc.ABC):
    @abc.abstractmethod
    def delete(self, *, todo_id: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> list[Todo]:
        raise NotImplementedError

    @abc.abstractmethod
    def refresh(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def upsert(self, *, todo: Todo) -> None:
        raise NotImplementedError
