import datetime

from src import domain
from src.adapter import db
from src.domain import Category

import sqlalchemy as sa

__all__ = ("DbCategoryRepository",)



class DbCategoryRepository(domain.CategoryRepository):
    def __init__(self, *, engine: sa.engine.Engine):
        self._engine = engine

    def add(self, *, category: Category) -> None:
        with self._engine.begin() as con:
            con.execute(
                sa.insert(db.category)
                .values(
                    category_id=category.category_id,
                    name=category.name,
                    note=category.note,
                    date_added=category.date_added,
                    date_updated=category.date_updated,
                    date_deleted=None,
                )
            )

    def delete(self, *, category_id: str) -> None:
        with self._engine.begin() as con:
            con.execute(
                sa.update(db.category)
                .where(db.category.c.category_id == category_id)
                .values(date_deleted=datetime.datetime.now())
            )

    def get(self, *, category_id: str) -> Category | None:
        with self._engine.begin() as con:
            result = con.execute(
                sa.select(db.category)
                .where(db.category.c.category_id == category_id)
            )
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

    def get_active(self) -> list[Category]:
        with self._engine.begin() as con:
            result = con.execute(
                sa.select(db.category)
                .where(db.category.c.date_deleted == None)  # noqa
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

    def update(self, *, category: Category) -> None:
        with self._engine.begin() as con:
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


if __name__ == '__main__':
    eng = db.create_engine()
    repo = DbCategoryRepository(engine=eng)
    for r in repo.get_active():
        print(r)

    print(f"{repo.get(category_id='29b91b51b5b64a4590e25b610b91b84f')}")