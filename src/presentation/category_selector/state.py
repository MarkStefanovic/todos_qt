import dataclasses

from src import domain

__all__ = ("CategorySelectorState",)


@dataclasses.dataclass(frozen=True, kw_only=True)
class CategorySelectorState:
    selected_category: domain.Category | domain.Unspecified = domain.Unspecified()
    category_options: tuple[domain.Category, ...] | domain.Unspecified = domain.Unspecified()
