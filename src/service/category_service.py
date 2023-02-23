import datetime

import sqlalchemy as sa

from src import adapter, domain

__all__ = ("CategoryService",)


class CategoryService(domain.CategoryService):
    def __init__(self, *, engine: sa.engine.Engine):
        self._engine = engine

        self._categories: dict[str, domain.Category] = {}
        self._last_refresh: datetime.datetime | None = None

    def add(self, *, category: domain.Category) -> None:
        self._refresh()

        repo = adapter.DbCategoryRepository(engine=self._engine)
        repo.add(category=category)
        self._categories[category.category_id] = category

    def all(self) -> list[domain.Category]:
        self._refresh()

        # noinspection PyTypeChecker
        return sorted(self._categories.values(), key=lambda c: c.name)

    def delete(self, *, category_id: str) -> None:
        self._refresh()

        todo_repo = adapter.DbTodoRepository(engine=self._engine)
        if matching_todos := todo_repo.where_category(category_id=category_id):
            if category := self._categories[category_id]:
                raise ValueError(
                    f"Cannot delete the category, {category.name}, as it is used "
                    f"by {len(matching_todos)} todos."
                )
            else:
                raise Exception("Category does not exist in the database.")

        category_repo = adapter.DbCategoryRepository(engine=self._engine)
        category_repo.delete(category_id=category_id)
        del self._categories[category_id]

    def get(self, *, category_id: str) -> domain.Category | None:
        self._refresh()

        return self._categories.get(category_id)

    def refresh(self) -> None:
        repo = adapter.DbCategoryRepository(engine=self._engine)
        self._categories = {
            category.category_id: category
            for category in repo.get_active()
        }
        self._last_refresh = datetime.datetime.now()

    def update(self, *, category: domain.Category) -> None:
        self._refresh()

        repo = adapter.DbCategoryRepository(engine=self._engine)
        repo.update(category=category)
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


if __name__ == '__main__':
    eng = adapter.db.create_engine()
    svc = CategoryService(engine=eng)
    for r in svc.all():
        print(r)
