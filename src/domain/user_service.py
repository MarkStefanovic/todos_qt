import abc

from src import domain

__all__ = ("UserService",)


class UserService:
    @abc.abstractmethod
    def add(self, *, user: domain.User) -> None | domain.Error:
        raise NotImplementedError

    @abc.abstractmethod
    def get_current_user(self) -> domain.User | domain.Error:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, *, user_id: str) -> None | domain.Error:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, *, user_id: str) -> domain.User | None | domain.Error:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, *, user: domain.User) -> None | domain.Error:
        raise NotImplementedError

    @abc.abstractmethod
    def where(self, *, active: bool) -> list[domain.User] | domain.Error:
        raise NotImplementedError
