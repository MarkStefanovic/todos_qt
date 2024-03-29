import datetime
import typing

import sqlalchemy as sa
from loguru import logger

from src import domain
from src.adapter import db

__all__ = (
    "add",
    "delete",
    "get",
    "update",
    "where",
)


def add(
    *,
    schema: str | None,
    con: sa.Connection,
    category: domain.Category,
) -> None | domain.Error:
    try:
        con.execute(
            sa.insert(db.category(schema=schema)).values(
                category_id=category.category_id,
                name=category.name,
                note=category.note,
                date_added=category.date_added,
                date_updated=category.date_updated,
                date_deleted=category.date_deleted,
            )
        )

        return None
    except Exception as e:
        logger.error(f"{__file__}.add({category=!r}) failed: {e!s}")

        return domain.Error.new(str(e), category=category)


def delete(
    *,
    schema: str | None,
    con: sa.Connection,
    category_id: str,
) -> None | domain.Error:
    try:
        # noinspection PyComparisonWithNone
        categories_for_user = con.execute(
            sa.select(sa.func.count(db.todo(schema=schema).c.todo_id)).where(
                (db.todo(schema=schema).c.category_id == category_id) & (db.todo(schema=schema).c.date_deleted == None)  # noqa: E711
            )
        ).scalar_one()
        if categories_for_user is not None and categories_for_user > 0:
            return domain.Error.new(
                f"Cannot delete category, as there are {categories_for_user} Todos associated with it.  "
                f"Please reassign or delete those first."
            )

        con.execute(
            sa.update(db.category(schema=schema))
            .where(db.category(schema=schema).c.category_id == category_id)
            .values(date_deleted=datetime.datetime.now())
        )

        return None
    except Exception as e:
        logger.error(f"{__file__}.delete({category_id=!r}) failed: {e!s}")

        return domain.Error.new(str(e), category_id=category_id)


def get(
    *,
    schema: str | None,
    con: sa.Connection,
    category_id: str,
) -> domain.Category | None | domain.Error:
    try:
        result = con.execute(
            sa.select(db.category(schema=schema)).where(db.category(schema=schema).c.category_id == category_id)
        )

        if row := result.one_or_none():
            errors: list[str] = []
            if row.category_id is None:
                errors.append("category is None.")
            if row.name is None:
                errors.append("name is None.")
            if row.note is None:
                errors.append("note is None.")
            if row.date_added is None:
                errors.append("date_added is None.")
            if errors:
                errors_str = "\n- ".join(errors)
                return domain.Error.new(f"invalid Category row, {row!r}:\n- {errors_str}")

            return _row_to_domain(row)

        return None
    except Exception as e:
        logger.error(f"{__file__}.get({category_id=!r}) failed: {e!s}")

        return domain.Error.new(str(e), category_id=category_id)


def where(
    *,
    schema: str | None,
    con: sa.Connection,
    active: bool,
) -> list[domain.Category] | domain.Error:
    try:
        qry = sa.select(db.category(schema=schema))

        if active:
            # noinspection PyComparisonWithNone,PyTypeChecker
            qry = qry.where(db.category(schema=schema).c.date_deleted == None)  # noqa: E711

        result = con.execute(qry.order_by(db.category(schema=schema).c.name))

        categories: list[domain.Category] = []
        for row in result.fetchall():
            category = _row_to_domain(row)
            if isinstance(category, domain.Error):
                return category

            categories.append(category)

        return categories
    except Exception as e:
        logger.error(f"{__file__}.where({active=!r}) failed: {e!s}")

        return domain.Error.new(str(e), active=active)


def update(
    *,
    schema: str | None,
    con: sa.Connection,
    category: domain.Category,
) -> None | domain.Error:
    try:
        con.execute(
            sa.update(db.category(schema=schema))
            .where(db.category(schema=schema).c.category_id == category.category_id)
            .values(
                name=category.name,
                note=category.note,
                date_updated=category.date_updated,
                date_deleted=None,
            )
        )

        return None
    except Exception as e:
        logger.error(f"{__file__}.update({category=!r}) failed: {e}")

        return domain.Error.new(str(e), category=category)


def _row_to_domain(row: sa.Row[typing.Any], /) -> domain.Category | domain.Error:
    try:
        values: dict[str, typing.Any] = {}
        errors: list[str] = []

        if row.category_id is None:
            errors.append("category is None.")
        else:
            if isinstance(row.category_id, str):
                values["category_id"] = row.category_id
            else:
                errors.append(f"category_id, {row.category_id!r}, is not a string.")

        if row.name is None:
            errors.append("name is None.")
        else:
            if isinstance(row.name, str):
                values["name"] = row.name
            else:
                errors.append(f"name, {row.name!r}, is not a string.")

        if row.note is None:
            errors.append("note is None.")
        else:
            if isinstance(row.note, str):
                values["note"] = row.note
            else:
                errors.append(f"note, {row.note!r}, is not a string.")

        if row.date_added is None:
            errors.append("date_added is None.")
        else:
            if isinstance(row.date_added, datetime.datetime):
                values["date_added"] = row.date_added
            else:
                errors.append(f"date_added, {row.date_added!r}, is not a datetime.")

        if row.date_updated is None:
            values["date_updated"] = None
        else:
            if isinstance(row.date_added, datetime.datetime):
                values["date_updated"] = row.date_updated
            else:
                errors.append(f"date_updated, {row.date_updated!r}, is not a datetime.")

        if row.date_deleted is None:
            values["date_deleted"] = None
        else:
            if isinstance(row.date_added, datetime.datetime):
                values["date_deleted"] = row.date_deleted
            else:
                errors.append(f"date_deleted, {row.date_deleted!r}, is not a datetime.")

        if errors:
            errors_csv = ", ".join(errors)
            return domain.Error.new(f"invalid Category row: {errors_csv}", row=row)

        return domain.Category(**values)
    except Exception as e:
        logger.error(f"{__file__}._row_to_domain({row=!r}) failed: {e!s}")

        return domain.Error.new(str(e), row=row)
