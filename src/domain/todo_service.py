import abc

from src.domain.error import Error
from src.domain.todo import Todo
from src.domain.unspecified import Unspecified
from src.domain.user import User

__all__ = ("TodoService",)


class TodoService(abc.ABC):
    @abc.abstractmethod
    def add(self, *, todo: Todo) -> None | Error:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, *, todo_id: str) -> None | Error:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, *, todo_id: str) -> Todo | None | Error:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_template_id_and_user_id(
        self,
        *,
        template_todo_id: str,
        user_id: str,
    ) -> Todo | None | Error:
        raise NotImplementedError

    @abc.abstractmethod
    def mark_complete(
        self,
        *,
        todo_id: str,
        user: User | None,
    ) -> None | Error:
        raise NotImplementedError

    @abc.abstractmethod
    def where(
        self,
        *,
        due_filter: bool | Unspecified,
        description_like: str | Unspecified,
        category_id_filter: str | Unspecified,
        user_id_filter: str | Unspecified,
    ) -> list[Todo] | Error:
        raise NotImplementedError

    @abc.abstractmethod
    def mark_incomplete(self, *, todo_id: str) -> None | Error:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, *, todo: Todo) -> None | Error:
        raise NotImplementedError
