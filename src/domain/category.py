from __future__ import annotations

import dataclasses
import typing
import datetime

__all__ = (
    "Category",
    "ALL_CATEGORY",
    "TODO_CATEGORY",
)


@dataclasses.dataclass(frozen=True, order=True)
class Category:
    category_id: str
    name: str
    note: str
    date_added: datetime.datetime
    date_updated: datetime.datetime | None
    date_deleted: datetime.datetime | None


ALL_CATEGORY: typing.Final[Category] = Category(
    category_id="",
    name="All",
    note="",
    date_added=datetime.datetime(1900, 1, 1),
    date_updated=None,
    date_deleted=None,
)

TODO_CATEGORY: typing.Final[Category] = Category(
    category_id="29b91b51b5b64a4590e25b610b91b84f",
    name="Todo",
    note="",
    date_added=datetime.datetime(1900, 1, 1),
    date_updated=None,
    date_deleted=None,
)
