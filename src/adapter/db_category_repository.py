from __future__ import annotations

import datetime

import sqlmodel as sm

from src import domain
from src.adapter import db
from src.domain import Category

__all__ = ("DbCategoryRepository",)


# noinspection PyComparisonWithNone
class DbCategoryRepository(domain.CategoryRepository):
    def __init__(self, *, session: sm.Session):
        self._session = session

    def add(self, *, category: Category) -> None:
        category_orm = db.Category(
            category_id=category.category_id,
            name=category.name,
            note=category.note,
            date_added=category.date_added,
            date_updated=category.date_updated,
            date_deleted=category.date_deleted,
        )
        self._session.add(category_orm)

    def delete(self, *, category_id: str) -> None:
        if todo_orm := self._session.exec(
            sm.select(db.Todo)
            .where(db.Todo.date_deleted == None)
            .where(db.Todo.category_id == category_id)
            .limit(1)
        ).one_or_none():
            raise Exception(
                f"Cannot delete category, as the todo, {todo_orm.description!r}, uses it."
            )

        if category_orm := self._session.exec(
            sm.select(db.Category)
            .where(db.Category.category_id == category_id)
        ).one_or_none():
            category_orm.date_deleted = datetime.datetime.now()
            self._session.add(category_orm)

    def get(self, *, category_id: str) -> Category | None:
        if category_orm := self._session.exec(
            sm.select(db.Category)
            .where(db.Category.category_id == category_id)
        ).one_or_none():
            return _orm_to_domain(orm=category_orm)
        return None

    def get_active(self) -> list[Category]:
        return [
            _orm_to_domain(orm=orm)
            for orm in self._session.exec(
                sm.select(db.Category)
                .where(db.Category.date_deleted == None)
            ).all()
        ]

    def update(self, *, category: Category) -> None:
        if category_orm := self._session.exec(
            sm.select(db.Category)
            .where(db.Category.category_id == category.category_id)
        ).one_or_none():
            category_orm.name = category.name
            category_orm.note = category.note
            category_orm.date_updated = category.date_updated
            category_orm.date_deleted = category.date_deleted
            self._session.add(category_orm)
        else:
            raise ValueError(
                f"Attempted to update a Category that does not exist in the database.  "
                f"[category_id] {category.category_id} not found."
            )


def _orm_to_domain(*, orm: db.Category) -> domain.Category:
    return Category(
        category_id=orm.category_id,
        name=orm.name,
        note=orm.note,
        date_added=orm.date_added,
        date_updated=orm.date_updated,
        date_deleted=orm.date_deleted,
    )

