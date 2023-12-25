from src import domain
from src.domain import Error

__all__ = ("CategoryService",)


class CategoryService(domain.CategoryService):
    def __init__(self):  # type: ignore
        self.add_result: None | domain.Error = None
        self.all_result: list[domain.Category] | domain.Error = []
        self.delete_result: None | domain.Error = None
        self.get_result: domain.Category | None | domain.Error = None
        self.update_result: None | domain.Error = None

    def add(self, /, category: domain.Category) -> None | domain.Error:
        return self.add_result

    def add_default_categories(self) -> None | Error:
        return None

    def all(self) -> list[domain.Category] | domain.Error:
        return self.all_result

    def delete(self, *, category_id: str) -> None | domain.Error:
        return self.delete_result

    def get(self, *, category_id: str) -> domain.Category | None | domain.Error:
        return self.get_result

    def update(self, *, category: domain.Category) -> None | domain.Error:
        return self.update_result
