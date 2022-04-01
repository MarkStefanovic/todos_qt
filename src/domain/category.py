import dataclasses
import datetime

__all__ = ("Category",)


@dataclasses.dataclass(frozen=True, order=True)
class Category:
    category_id: str
    name: str
    note: str
    date_added: datetime.datetime
    date_updated: datetime.datetime | None
    date_deleted: datetime.datetime | None
