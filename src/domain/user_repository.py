from __future__ import annotations

import abc

from src.domain.user import User

__all__ = ("UserRepository",)


class UserRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, *, user: User) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def all(self) -> list[User]:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, *, user_id: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, *, user_id: str) -> User | None:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, *, user: User) -> None:
        raise NotImplementedError
