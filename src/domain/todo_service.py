import abc

from src import domain

__all__ = ("TodoService",)


class TodoService(abc.ABC):
    @abc.abstractmethod
    def add(self, *, todo: domain.Todo) -> None | domain.Error:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, *, todo_id: str) -> None | domain.Error:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, *, todo_id: str) -> domain.Todo | None | domain.Error:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_template_id_and_user_id(
        self,
        *,
        template_todo_id: str,
        user_id: str,
    ) -> domain.Todo | None | domain.Error:
        raise NotImplementedError

    @abc.abstractmethod
    def mark_complete(
        self,
        *,
        todo_id: str,
        user: domain.User | None,
    ) -> None | domain.Error:
        raise NotImplementedError

    @abc.abstractmethod
    def where(
        self,
        *,
        due_filter: bool | domain.Unspecified,
        description_like: str | domain.Unspecified,
        category_id_filter: str | domain.Unspecified,
        user_id_filter: str | domain.Unspecified,
    ) -> list[domain.Todo] | domain.Error:
        raise NotImplementedError

    @abc.abstractmethod
    def mark_incomplete(self, *, todo_id: str) -> None | domain.Error:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, *, todo: domain.Todo) -> None | domain.Error:
        raise NotImplementedError
