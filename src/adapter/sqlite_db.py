from __future__ import annotations

import pathlib
import sqlite3
import types
import typing

from loguru import logger

from src import domain

__all__ = ("SqliteDb",)


class SqliteDb(domain.Db):
    def __init__(self, /, fp: pathlib.Path):
        super().__init__()

        self._fp = fp

        self._con: typing.Optional[sqlite3.Connection] = None
        self._cur: typing.Optional[sqlite3.Cursor] = None

    def execute(self, sql: str, /, **params: typing.Any) -> domain.Rows:
        if self._con is None:
            raise domain.exceptions.ConnectionClosed()
        else:
            logger.debug(f"Executing sql:\n\t{sql}\n\tparams={params}")
            if self._cur is None:
                logger.debug("Opened cursor.")
                self._cur = self._con.cursor()

            if len(params) == 0:
                result = self._cur.execute(sql)
            else:
                result = self._cur.execute(sql, params)

            if rows := result.fetchall():
                column_names = [description[0] for description in self._cur.description]
                return domain.Rows(
                    column_names=column_names, rows=[tuple(row) for row in rows]
                )
            else:
                return domain.Rows(column_names=[], rows=[])

    def executemany(self, sql: str, /, *params: dict[str, typing.Any]) -> None:
        if self._con is None:
            raise domain.exceptions.ConnectionClosed()
        else:
            logger.debug(f"Executing sql:\n\t{sql}\n\tparams={params}")
            if self._cur is None:
                logger.debug("Opened cursor.")
                self._cur = self._con.cursor()

            if len(params) == 0:
                self._cur.execute(sql)
            else:
                self._cur.executemany(sql, params)

    def commit(self) -> None:
        if self._con is None:
            raise domain.exceptions.ConnectionClosed()
        else:
            self._con.commit()

    def rollback(self) -> None:
        if self._con is None:
            raise domain.exceptions.ConnectionClosed()
        else:
            self._con.rollback()

    def __enter__(self) -> SqliteDb:
        if self._con is None:
            self._con = sqlite3.connect(self._fp)
            logger.debug(f"Opened connection to to {self._fp}.")
        return self

    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_val: typing.Optional[BaseException],
        exc_tb: typing.Optional[types.TracebackType],
    ) -> None:
        if self._cur is not None:
            self._cur.close()
            self._cur = None
            logger.debug("Closed cursor.")

        if self._con is not None:
            self._con.close()
            self._con = None
            logger.debug(f"Closed connection to {self._fp}.")
