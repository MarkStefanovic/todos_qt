import datetime

import sqlmodel as sm

from src import adapter, domain
from src.domain import Category

__all__ = ("DbCategoryService",)


class DbCategoryService(domain.CategoryService):
    def __init__(self, *, session: sm.Session):
        self._session = session

        self._categories: dict[str, domain.Category] = {}
        self._last_refresh: datetime.datetime | None = None

    def add(self, *, category: Category) -> None:
        self._refresh()

        self._repo.add(category=category)
        self._session.commit()
        self._categories[category.category_id] = category

    def all(self) -> list[Category]:
        self._refresh()

        # noinspection PyTypeChecker
        return sorted(self._categories.values())

    def delete(self, *, category_id: str) -> None:
        self._refresh()

        todo_repo = adapter.DbTodoRepository(session=self._session)
        if matching_todos := todo_repo.where_category(category_id=category_id):
            if category := self._categories[category_id]:
                raise ValueError(
                    f"Cannot delete the category, {category.name}, as it is used "
                    f"by {len(matching_todos)} todos."
                )
            else:
                raise Exception("Category does not exist in the database.")

        self._repo.delete(category_id=category_id)
        self._session.commit()
        del self._categories[category_id]

    def get(self, *, category_id: str) -> Category | None:
        self._refresh()

        return self._categories.get(category_id)

    def update(self, *, category: Category) -> None:
        self._refresh()

        self._repo.update(category=category)
        self._session.commit()
        self._categories[category.category_id] = category

    def _refresh(self) -> None:
        if self._last_refresh is None:
            time_to_refresh = True
        else:
            if (datetime.datetime.now() - self._last_refresh).seconds > 300:
                time_to_refresh = False
            else:
                time_to_refresh = True

        if time_to_refresh:
            self._categories = {
                category.category_id: category
                for category in self._repo.get_active()
            }
            self._last_refresh = datetime.datetime.now()

    @property
    def _repo(self) -> domain.CategoryRepository:
        return adapter.DbCategoryRepository(session=self._session)
