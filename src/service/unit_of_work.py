from __future__ import annotations

import abc
import types
import typing

import src.adapter.sqlite_db
import src.domain.todo_repository
from src import adapter, domain


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


class DefaultTodoUnitOfWork(TodoUnitOfWork):
    def __init__(self, sqlite_db: src.adapter.sqlite_db.SqliteDb):
        self._db = sqlite_db
        self._todo_repository: typing.Optional[adapter.SqliteTodoRepository] = None

    def __enter__(self) -> DefaultTodoUnitOfWork:
        self._todo_repository = adapter.SqliteTodoRepository(self._db)
        return self

    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_val: typing.Optional[BaseException],
        exc_tb: typing.Optional[types.TracebackType],
    ) -> None:
        pass

    def rollback(self) -> None:
        self._db.rollback()

    def save(self) -> None:
        self._db.commit()

    @property
    def todo_repository(self) -> adapter.SqliteTodoRepository:
        if self._todo_repository is None:
            raise domain.exceptions.OutsideTransaction
        return self._todo_repository
