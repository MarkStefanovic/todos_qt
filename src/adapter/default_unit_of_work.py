from __future__ import annotations

import types
import typing

from src import domain
from src.adapter import sqlite_db, sqlite_todo_repository

__all__ = ("DefaultTodoUnitOfWork",)


class DefaultTodoUnitOfWork(domain.TodoUnitOfWork):
    def __init__(self, sqlite_db: sqlite_db.SqliteDb):
        self._db = sqlite_db
        self._todo_repository = sqlite_todo_repository.SqliteTodoRepository(self._db)

        self._todo_repository.create_if_not_exists()

    def __enter__(self) -> DefaultTodoUnitOfWork:
        self._todo_repository = sqlite_todo_repository.SqliteTodoRepository(self._db)
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
    def todo_repository(self) -> sqlite_todo_repository.SqliteTodoRepository:
        if self._todo_repository is None:
            raise domain.exceptions.OutsideTransaction
        return self._todo_repository
