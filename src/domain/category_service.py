import abc

from src.domain.category import Category
from src.domain.error import Error

__all__ = ("CategoryService",)


class CategoryService(abc.ABC):
    @abc.abstractmethod
    def add(self, /, category: Category) -> None | Error:
        raise NotImplementedError

    @abc.abstractmethod
    def all(self) -> list[Category] | Error:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, *, category_id: str) -> None | Error:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, *, category_id: str) -> Category | None | Error:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, *, category: Category) -> None | Error:
        raise NotImplementedError
