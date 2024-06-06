import dataclasses

from src import domain
from src.domain import Error

__all__ = ("CategoryService",)


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class CategoryService(domain.CategoryService):
    add_result: None | domain.Error = None
    all_result: tuple[domain.Category, ...] | domain.Error = (domain.TODO_CATEGORY,)
    delete_result: None | domain.Error = None
    get_result: domain.Category | None | domain.Error = domain.TODO_CATEGORY
    update_result: None | domain.Error = None

    def add(self, /, category: domain.Category) -> None | domain.Error:
        return self.add_result

    def add_default_categories(self) -> None | Error:
        return None

    def all(self) -> list[domain.Category] | domain.Error:
        if isinstance(self.all_result, domain.Error):
            return self.all_result

        return list(self.all_result)

    def delete(self, *, category_id: str) -> None | domain.Error:
        return self.delete_result

    def get(self, *, category_id: str) -> domain.Category | None | domain.Error:
        return self.get_result

    def update(self, *, category: domain.Category) -> None | domain.Error:
        return self.update_result
