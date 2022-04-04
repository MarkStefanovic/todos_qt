from __future__ import annotations

import dataclasses
import datetime

from src import domain

__all__ = ("CategoryFormState",)


@dataclasses.dataclass(frozen=True)
class CategoryFormState:
    category_id: str
    name: str
    note: str
    date_added: datetime.datetime
    date_updated: datetime.datetime | None

    @staticmethod
    def initial() -> CategoryFormState:
        return CategoryFormState(
            category_id=domain.create_uuid(),
            name="",
            note="",
            date_added=datetime.datetime.now(),
            date_updated=None,
        )

    @staticmethod
    def from_domain(*, category: domain.Category) -> CategoryFormState:
        return CategoryFormState(
            category_id=category.category_id,
            name=category.name,
            note=category.note,
            date_added=category.date_added,
            date_updated=category.date_updated,
        )

    def to_domain(self) -> domain.Category:
        return domain.Category(
            category_id=self.category_id,
            name=self.name,
            note=self.note,
            date_added=self.date_added,
            date_updated=self.date_updated,
            date_deleted=None,
        )

