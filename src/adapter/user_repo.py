import datetime

import sqlalchemy as sa

from src import domain
from src.adapter import db
from src.domain import User

__all__ = ("add",)


# noinspection DuplicatedCode
def add(*, con: sa.Connection, user: User) -> None | domain.Error:
    try:
        con.execute(
            sa.insert(db.user).values(
                user_id=user.user_id,
                display_name=user.display_name,
                username=user.username,
                is_admin=user.is_admin,
                date_added=datetime.datetime.now(),
                date_updated=None,
                date_deleted=None,
            )
        )
    except Exception as e:
        return domain.Error.new(str(e), user=user)


def where(*, con: sa.Connection, active: bool) -> list[User] | domain.Error:
    try:
        qry = sa.select(db.user)

        if active:
            qry = qry.where(db.user.c.date_deleted == None)  # noqa

        result = con.execute(qry.order_by(db.user.c.display_name))

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
    except Exception as e:
        return domain.Error.new(str(e))


def delete_user(
    *,
    con: sa.Connection,
    user_id: str,
) -> None | domain.Error:
    try:
        con.execute(sa.update(db.todo).where(db.todo.c.user_id == user_id).values(date_deleted=datetime.datetime.now()))

        con.execute(sa.update(db.user).where(db.user.c.user_id == user_id).values(date_deleted=datetime.datetime.now()))
    except Exception as e:
        return domain.Error.new(str(e), user_id=user_id)


def get(
    *,
    con: sa.Connection,
    user_id: str,
) -> domain.User | None | domain.Error:
    try:
        result = con.execute(sa.select(db.user).where(db.user.c.user_id == user_id))

        if row := result.one_or_none():
            return domain.User(
                user_id=row.user_id,
                username=row.username,
                display_name=row.display_name,
                is_admin=row.is_admin,
                date_added=row.date_added,
                date_updated=row.date_updated,
            )
    except Exception as e:
        return domain.Error.new(str(e))

    return None


def update(
    *,
    con: sa.Connection,
    user: User,
) -> None | domain.Error:
    try:
        con.execute(
            sa.update(db.user)
            .where(db.user.c.user_id == user.user_id)
            .values(
                username=user.username,
                display_name=user.display_name,
                date_updated=datetime.datetime.now(),
                date_deleted=None,
                is_admin=user.is_admin,
            )
        )
    except Exception as e:
        return domain.Error.new(str(e), user=user)
