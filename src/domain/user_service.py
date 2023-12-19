import abc

from src.domain.error import Error
from src.domain.user import User

__all__ = ("UserService",)


class UserService:
    @abc.abstractmethod
    def add(self, *, user: User) -> None | Error:
        raise NotImplementedError

    @abc.abstractmethod
    def get_current_user(self) -> User | Error:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, *, user_id: str) -> None | Error:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, *, user_id: str) -> User | None | Error:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, *, user: User) -> None | Error:
        raise NotImplementedError

    @abc.abstractmethod
    def where(self, *, active: bool) -> list[User] | Error:
        raise NotImplementedError
