import typing

import sqlalchemy as sa

from src import adapter, domain

__all__ = ("CategoryService",)


class CategoryService(domain.CategoryService):
    def __init__(self, *, engine: sa.engine.Engine):
        self._engine: typing.Final[sa.engine.Engine] = engine

    def add(self, /, category: domain.Category) -> None | domain.Error:
        try:
            with self._engine.begin() as con:
                add_result = adapter.category_repo.add(con=con, category=category)
                if isinstance(add_result, domain.Error):
                    return add_result

            return None
        except Exception as e:
            return domain.Error.new(str(e), category=category)

    def add_default_categories(self) -> None | domain.Error:
        with self._engine.begin() as con:
            categories = adapter.category_repo.where(con=con, active=False)
            if isinstance(categories, domain.Error):
                return categories

            for category in (domain.TODO_CATEGORY,):
                if category not in categories:
                    add_result = adapter.category_repo.add(con=con, category=category)
                    if isinstance(add_result, domain.Error):
                        return add_result

        return None

    def all(self) -> list[domain.Category] | domain.Error:
        try:
            with self._engine.begin() as con:
                return adapter.category_repo.where(con=con, active=True)
        except Exception as e:
            return domain.Error.new(str(e))

    def delete(self, *, category_id: str) -> None | domain.Error:
        try:
            with self._engine.begin() as con:
                category = adapter.category_repo.get(con=con, category_id=category_id)
                if isinstance(category, domain.Error):
                    return category

                if category is None:
                    return None

                matching_todos = adapter.todo_repo.where(
                    con=con,
                    category_id=category_id,
                    user_id=domain.Unspecified(),
                    description_starts_with=domain.Unspecified(),
                    template_todo_id=domain.Unspecified(),
                )
                if isinstance(matching_todos, domain.Error):
                    return matching_todos

                if matching_todos:
                    raise ValueError(
                        f"Cannot delete the category, {category.name}, as it is used "
                        f"by {len(matching_todos)} todos."
                    )

                delete_result = adapter.category_repo.delete(con=con, category_id=category_id)
                if isinstance(delete_result, domain.Error):
                    return delete_result

                return None
        except Exception as e:
            return domain.Error.new(str(e), category_id=category_id)

    def get(self, *, category_id: str) -> domain.Category | None | domain.Error:
        try:
            with self._engine.begin() as con:
                return adapter.category_repo.get(con=con, category_id=category_id)
        except Exception as e:
            return domain.Error.new(str(e), category_id=category_id)

    def update(self, *, category: domain.Category) -> None | domain.Error:
        try:
            with self._engine.begin() as con:
                update_result = adapter.category_repo.update(con=con, category=category)
                if isinstance(update_result, domain.Error):
                    return update_result

            return None
        except Exception as e:
            return domain.Error.new(str(e), category=category)


if __name__ == "__main__":
    eng = adapter.db.create_engine()
    assert not isinstance(eng, domain.Error)
    svc = CategoryService(engine=eng)
    rs = svc.all()
    assert not isinstance(rs, domain.Error)
    for r in rs:
        print(r)
