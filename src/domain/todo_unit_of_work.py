from __future__ import annotations
import abc
import types
import typing

import src.domain

__all__ = ("TodoUnitOfWork",)


class TodoUnitOfWork(abc.ABC):
    @abc.abstractmethod
    def __enter__(self) -> TodoUnitOfWork:
        raise NotImplementedError

    @abc.abstractmethod
    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_val: typing.Optional[BaseException],
        exc_tb: typing.Optional[types.TracebackType],
    ) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def save(self) -> None:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def todo_repository(self) -> src.domain.todo_repository.TodoRepository:
        raise NotImplementedError
