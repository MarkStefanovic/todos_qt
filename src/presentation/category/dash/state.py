from __future__ import annotations

import dataclasses

from src import domain

__all__ = ("CategoryDashState",)


@dataclasses.dataclass(frozen=True)
class CategoryDashState:
    categories: list[domain.Category]
    selected_category: domain.Category | None
    status: str

    @staticmethod
    def initial() -> CategoryDashState:
        return CategoryDashState(
            categories=[],
            selected_category=None,
            status="",
        )
