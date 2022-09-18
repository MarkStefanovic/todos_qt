from __future__ import annotations

import datetime

import sqlalchemy as sa
import sqlmodel as sm

from src import adapter, domain
from src.domain import Category

__all__ = ("CategoryService",)


class CategoryService(domain.CategoryService):
    def __init__(self, *, engine: sa.engine.Engine):
        self._engine = engine

        self._categories: dict[str, domain.Category] = {}
        self._last_refresh: datetime.datetime | None = None

    def add(self, *, category: Category) -> None:
        self._refresh()

        with sm.Session(self._engine) as session:
            repo = adapter.DbCategoryRepository(session=session)
            repo.add(category=category)
            session.commit()
            self._categories[category.category_id] = category

    def all(self) -> list[Category]:
        self._refresh()

        # noinspection PyTypeChecker
        return sorted(self._categories.values(), key=lambda c: c.name)

    def delete(self, *, category_id: str) -> None:
        self._refresh()

        with sm.Session(self._engine) as session:
            todo_repo = adapter.DbTodoRepository(session=session)
            if matching_todos := todo_repo.where_category(category_id=category_id):
                if category := self._categories[category_id]:
                    raise ValueError(
                        f"Cannot delete the category, {category.name}, as it is used "
                        f"by {len(matching_todos)} todos."
                    )
                else:
                    raise Exception("Category does not exist in the database.")

            category_repo = adapter.DbCategoryRepository(session=session)
            category_repo.delete(category_id=category_id)
            session.commit()
            del self._categories[category_id]

    def get(self, *, category_id: str) -> Category | None:
        self._refresh()

        return self._categories.get(category_id)

    def refresh(self) -> None:
        with sm.Session(self._engine) as session:
            repo = adapter.DbCategoryRepository(session=session)
            self._categories = {
                category.category_id: category
                for category in repo.get_active()
            }
            self._last_refresh = datetime.datetime.now()

    def update(self, *, category: Category) -> None:
        self._refresh()

        with sm.Session(self._engine) as session:
            repo = adapter.DbCategoryRepository(session=session)
            repo.update(category=category)
            session.commit()
            self._categories[category.category_id] = category

    def _refresh(self) -> None:
        if self._last_refresh is None:
            time_to_refresh = True
        else:
            if (datetime.datetime.now() - self._last_refresh).seconds > 300:
                time_to_refresh = True
            else:
                time_to_refresh = False

        if time_to_refresh:
            self.refresh()
