import dataclasses
import datetime

__all__ = ("Category", "TODO_CATEGORY")


@dataclasses.dataclass(frozen=True, order=True)
class Category:
    category_id: str
    name: str
    note: str
    date_added: datetime.datetime
    date_updated: datetime.datetime | None
    date_deleted: datetime.datetime | None


TODO_CATEGORY = Category(
    category_id="29b91b51b5b64a4590e25b610b91b84f",
    name="Todo",
    note="",
    date_added=datetime.datetime(1900, 1, 1),
    date_updated=None,
    date_deleted=None,
)
