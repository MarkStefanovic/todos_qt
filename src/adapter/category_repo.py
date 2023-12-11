import datetime

from src import domain
from src.adapter import db
from src.domain import Category

import sqlalchemy as sa

__all__ = (
    "add",
    "delete",
    "get",
    "get_active",
    "update",
)


def add(
    *,
    con: sa.Connection,
    category: Category,
) -> None | domain.Error:
    try:
        con.execute(
            sa.insert(db.category).values(
                category_id=category.category_id,
                name=category.name,
                note=category.note,
                date_added=category.date_added,
                date_updated=category.date_updated,
                date_deleted=None,
            )
        )

        return None
    except Exception as e:
        return domain.Error.new(str(e), category=category)


def delete(
    *,
    con: sa.Connection,
    category_id: str,
) -> None | domain.Error:
    try:
        con.execute(
            sa.update(db.category)
            .where(db.category.c.category_id == category_id)
            .values(date_deleted=datetime.datetime.now())
        )

        return None
    except Exception as e:
        return domain.Error.new(str(e), category_id=category_id)


def get(
    *,
    con: sa.Connection,
    category_id: str,
) -> Category | None | domain.Error:
    try:
        result = con.execute(sa.select(db.category).where(db.category.c.category_id == category_id))

        if row := result.one_or_none():
            return domain.Category(
                category_id=row.category_id,
                name=row.name,
                note=row.note,
                date_added=row.date_added,
                date_updated=row.date_updated,
                date_deleted=row.date_deleted,
            )

        return None
    except Exception as e:
        return domain.Error.new(str(e), category_id=category_id)


def get_active(*, con: sa.Connection) -> list[Category] | domain.Error:
    try:
        result = con.execute(
            sa.select(db.category)
            .where(db.category.c.date_deleted == None)  # noqa
            .order_by(db.category.c.name)
        )
        return [
            domain.Category(
                category_id=row.category_id,
                name=row.name,
                note=row.note,
                date_added=row.date_added,
                date_updated=row.date_updated,
                date_deleted=row.date_deleted,
            )
            for row in result.fetchall()
        ]
    except Exception as e:
        return domain.Error.new(str(e))


def update(*, con: sa.Connection, category: Category) -> None | domain.Error:
    try:
        con.execute(
            sa.update(db.category)
            .where(db.category.c.category_id == category.category_id)
            .values(
                name=category.name,
                note=category.note,
                date_updated=category.date_updated,
                date_deleted=None,
            )
        )

        return None
    except Exception as e:
        return domain.Error.new(str(e), category=category)


if __name__ == "__main__":
    eng = db.create_engine()
    with eng.begin() as cn:
        for r in get_active(con=cn):
            print(r)

        print(f"get: {get(con=cn, category_id='29b91b51b5b64a4590e25b610b91b84f')}")
