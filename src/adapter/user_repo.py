import datetime
import typing

import sqlalchemy as sa
from loguru import logger

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

        return None
    except Exception as e:
        logger.error(f"{__file__}.add({user=!r}) failed: {e}")

        return domain.Error.new(str(e), user=user)


def delete_user(
    *,
    con: sa.Connection,
    user_id: str,
) -> None | domain.Error:
    try:
        # noinspection PyComparisonWithNone,PyTypeChecker
        todos_for_user = con.execute(
            sa.select(sa.func.count(db.todo.c.todo_id)).where(
                (db.todo.c.user_id == user_id) & (db.todo.c.date_deleted == None)  # noqa: E711
            )
        ).scalar_one()

        if todos_for_user is not None and todos_for_user > 0:
            return domain.Error.new(
                f"Cannot delete user, as there are {todos_for_user} Todos associated with them.  "
                f"Please reassign or delete those first."
            )

        con.execute(sa.update(db.user).where(db.user.c.user_id == user_id).values(date_deleted=datetime.datetime.now()))

        return None
    except Exception as e:
        logger.error(f"{__file__}.delete({user_id=!r}) failed: {e}")

        return domain.Error.new(str(e), user_id=user_id)


def get(
    *,
    con: sa.Connection,
    user_id: str,
) -> domain.User | None | domain.Error:
    try:
        result = con.execute(sa.select(db.user).where(db.user.c.user_id == user_id))

        if row := result.one_or_none():
            return _row_to_domain(row)

        return None
    except Exception as e:
        logger.error(f"{__file__}.get({user_id=!r}) failed: {e}")

        return domain.Error.new(str(e))


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

        return None
    except Exception as e:
        logger.error(f"{__file__}.get({user=!r}) failed: {e}")

        return domain.Error.new(str(e), user=user)


def where(*, con: sa.Connection, active: bool) -> list[User] | domain.Error:
    try:
        qry = sa.select(db.user)

        if active:
            qry = qry.where(db.user.c.date_deleted == None)  # noqa

        result = con.execute(qry.order_by(db.user.c.display_name))

        users: list[domain.User] = []
        for row in result.fetchall():
            user = _row_to_domain(row)
            if isinstance(user, domain.Error):
                return user

            users.append(user)

        return users
    except Exception as e:
        logger.error(f"{__file__}.where({active=!r}) failed: {e}")

        return domain.Error.new(str(e))


def _row_to_domain(row: sa.Row[typing.Any], /) -> domain.User | domain.Error:
    try:
        errors: list[str] = []
        values: dict[str, typing.Any] = {}

        if row.user_id is None:
            errors.append("user_id is None.")
        else:
            if isinstance(row.user_id, str):
                values["user_id"] = row.user_id
            else:
                errors.append(f"user_id, {row.user_id!r}, is not a string.")

        if row.username is None:
            errors.append("username is None.")
        else:
            if isinstance(row.username, str):
                values["username"] = row.username
            else:
                errors.append(f"username, {row.username!r}, is not a string.")

        if row.display_name is None:
            errors.append("display_name is None.")
        else:
            if isinstance(row.display_name, str):
                values["display_name"] = row.display_name
            else:
                errors.append(f"display_name, {row.display_name!r}, is not a string.")

        if row.date_added is None:
            values["date_added"] = None
        else:
            if isinstance(row.date_added, datetime.datetime):
                values["date_added"] = row.date_added
            else:
                errors.append(f"date_added, {row.date_added!r}, is not a string.")

        if row.date_updated is None:
            values["date_updated"] = None
        else:
            if isinstance(row.date_updated, datetime.datetime):
                values["date_updated"] = row.date_updated
            else:
                errors.append(f"date_updated, {row.date_updated!r}, is not a datetime.")

        if row.is_admin is None:
            errors.append("is_admin is None.")
        else:
            if isinstance(row.is_admin, bool):
                values["is_admin"] = row.is_admin
            else:
                errors.append(f"is_admin, {row.is_admin!r}, is not a bool.")

        if errors:
            error_csv = ", ".join(errors)
            return domain.Error.new(f"Invalid User row, {row!r}: {error_csv}")

        return domain.User(**values)
    except Exception as e:
        logger.error(f"{__file__}._row_to_domain({row=!r}) failed: {e!s}")

        return domain.Error.new(str(e), row=row)


if __name__ == "__main__":
    eng = db.create_engine()
    if isinstance(eng, domain.Error):
        raise Exception(str(eng))

    with eng.begin() as cn:
        cs = where(con=cn, active=True)
        if isinstance(cs, domain.Error):
            raise Exception(str(cs))

        for c in cs:
            print(c)
