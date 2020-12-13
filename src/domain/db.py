from __future__ import annotations

import abc
import types
import typing

from src.domain import rows

__all__ = ("Db",)


class Db(abc.ABC):
    @abc.abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def execute(
        self,
        *,
        sql: str,
        params: typing.Optional[typing.List[typing.Dict[str, typing.Any]]] = None,
    ) -> typing.Optional[rows.Rows]:
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def __enter__(self) -> Db:
        raise NotImplementedError

    @abc.abstractmethod
    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_val: typing.Optional[BaseException],
        exc_tb: typing.Optional[types.TracebackType],
    ) -> None:
        raise NotImplementedError
