import datetime

from src import domain
from src.adapter import db
from src.domain import User

import sqlalchemy as sa

__all__ = ("DbUserRepository",)


# noinspection DuplicatedCode
class DbUserRepository(domain.UserRepository):
    def __init__(self, engine: sa.engine.Engine):
        self._engine = engine

    def add(self, *, user: User) -> None:
        with self._engine.begin() as con:
            con.execute(
                sa.insert(db.user)
                .values(
                    user_id=user.user_id,
                    display_name=user.display_name,
                    username=user.username,
                    is_admin=user.is_admin,
                    date_added=datetime.datetime.now(),
                    date_updated=None,
                    date_deleted=None,
                )
            )

    def all(self) -> list[User]:
        with self._engine.begin() as con:
            # noinspection PyComparisonWithNone
            result = con.execute(
                sa.select(db.user)
                .where(db.user.c.date_deleted == None)
            )

            return [
                domain.User(
                    user_id=row.user_id,
                    username=row.username,
                    display_name=row.display_name,
                    is_admin=row.is_admin,
                    date_added=row.date_added,
                    date_updated=row.date_updated,
                )
                for row in result.fetchall()
            ]

    def delete(self, *, user_id: str) -> None:
        with self._engine.begin() as con:
            result = con.execute(
                sa.select(db.todo)
                .where(db.todo.c.date_deleted == None)  # noqa
                .where(db.todo.c.user_id == user_id)
            )
            if rows := result.fetchall():
                for row in rows:
                    con.execute(
                        sa.update(db.todo)
                        .where(db.todo.c.todo_id == row.todo_id)
                        .values(date_deleted=datetime.datetime.now())
                    )

            con.execute(
                sa.update(db.user)
                .values(date_deleted=datetime.datetime.now())
            )

    def get(self, *, user_id: str) -> domain.User | None:
        with self._engine.begin() as con:
            result = con.execute(
                sa.select(db.user)
                .where(db.user.c.user_id == user_id)
            )

            if row := result.one_or_none():
                return domain.User(
                    user_id=row.user_id,
                    username=row.username,
                    display_name=row.display_name,
                    is_admin=row.is_admin,
                    date_added=row.date_added,
                    date_updated=row.date_updated,
                )

        return None

    def update(self, *, user: User) -> None:
        with self._engine.begin() as con:
            con.execute(
                sa.update(db.user)
                .where(db.user.c.user_id == user.user_id)
                .values(
                    username=user.username,
                    display_name=user.display_name,
                    date_updated=datetime.datetime.now(),
                    is_admin=user.is_admin,
                )
            )
