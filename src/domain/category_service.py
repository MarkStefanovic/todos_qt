from __future__ import annotations

import abc

from src.domain.category import Category

__all__ = ("CategoryService",)


class CategoryService(abc.ABC):
    @abc.abstractmethod
    def add(self, *, category: Category) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def all(self) -> list[Category]:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, *, category_id: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, *, category_id: str) -> Category | None:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, *, category: Category) -> None:
        raise NotImplementedError
