from __future__ import annotations

import abc

from src.domain.user import User

__all__ = ("UserService",)


class UserService(abc.ABC):
    @abc.abstractmethod
    def add(self, *, user: User) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def all(self) -> list[User]:
        raise NotImplementedError

    @abc.abstractmethod
    def current_user(self) -> User | None:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, *, user_id: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, *, user_id: str) -> User | None:
        raise NotImplementedError

    @abc.abstractmethod
    def refresh(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, *, user: User) -> None:
        raise NotImplementedError
