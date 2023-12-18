import dataclasses

from src import domain

__all__ = ("CategoryDashState",)


@dataclasses.dataclass(frozen=True)
class CategoryDashState:
    categories: list[domain.Category] | domain.Unspecified = domain.Unspecified()
    selected_category: domain.Category | domain.Unspecified = domain.Unspecified()
    status: str | domain.Unspecified = domain.Unspecified()
    category_added: domain.Category | domain.Unspecified = domain.Unspecified()
    category_deleted: domain.Category | domain.Unspecified = domain.Unspecified()
    category_edited: domain.Category | domain.Unspecified = domain.Unspecified()
