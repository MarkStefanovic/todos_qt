from __future__ import annotations

import dataclasses

from src import domain

__all__ = ("CategoryDashState",)


@dataclasses.dataclass(frozen=True)
class CategoryDashState:
    categories: list[domain.Category]
    selected_category: domain.Category | None
    status: str
    current_user: domain.User

    @staticmethod
    def initial(*, current_user: domain.User) -> CategoryDashState:
        return CategoryDashState(
            categories=[],
            selected_category=None,
            status="",
            current_user=current_user,
        )
