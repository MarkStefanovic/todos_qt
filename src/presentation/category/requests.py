import dataclasses

from src import domain

__all__ = (
    "DeleteCategory",
    "EditCategory",
    "ToggleCompleted",
)


@dataclasses.dataclass(frozen=True, kw_only=True)
class DeleteCategory:
    category: domain.Category


@dataclasses.dataclass(frozen=True, kw_only=True)
class EditCategory:
    category: domain.Category


@dataclasses.dataclass(frozen=True, kw_only=True)
class ToggleCompleted:
    category: domain.Category
