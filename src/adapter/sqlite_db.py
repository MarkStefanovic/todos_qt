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

    def create_if_not_exists(self) -> None:
        if self._con is None:
            raise domain.exceptions.ConnectionClosed()
        else:
            # fmt: off
            self._con.executescript(
                """CREATE TABLE IF NOT EXISTS todo (
                        id INTEGER PRIMARY KEY,
                        description VARCHAR(100) NOT NULL,
                        frequency VARCHAR(20) NOT NULL,
                        month INT NULL,
                        week_day INT NULL,
                        month_day INT NULL,
                        year INT NULL,
                        week_number INT NULL,
                        date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                        date_completed TIMESTAMP NULL,
                        advance_days INT NULL,
                        start_date DATE NULL,
                        days INT NULL,
                        note TEXT NULL,
                        category TEXT NULL
                    );
                    CREATE INDEX IF NOT EXISTS ix_todo_category ON todo (category, description);
                """
            )
            # fmt: on

    def execute(
        self,
        sql: str,
        params: typing.Optional[typing.List[typing.Dict[str, typing.Any]]] = None,
    ) -> domain.Rows:
        if self._con is None:
            raise domain.exceptions.ConnectionClosed()
        else:
            logger.debug(f"Executing sql:\n\t{sql}\n\tparams={params}")
            if self._cur is None:
                self._cur = self._con.cursor()
                logger.debug("Opened cursor.")

            if params is None:
                result = self._cur.execute(sql)
            elif len(params) > 1:
                result = self._cur.executemany(sql, params)
            else:
                result = self._cur.execute(sql, params[0])

            if rows := result.fetchall():
                column_names = [description[0] for description in self._cur.description]
                return domain.Rows(
                    column_names=column_names, rows=[tuple(row) for row in rows]
                )
            else:
                return domain.Rows(column_names=[], rows=[])

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
