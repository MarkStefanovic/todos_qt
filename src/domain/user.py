import dataclasses
import datetime

__all__ = ("DEFAULT_USER", "User")


@dataclasses.dataclass(frozen=True)
class User:
    user_id: str
    username: str
    display_name: str
    is_admin: bool
    date_added: datetime.datetime
    date_updated: datetime.datetime | None


DEFAULT_USER = User(
    user_id="",
    username="",
    display_name="",
    is_admin=False,
    date_added=datetime.datetime(1900, 1, 1),
    date_updated=None,
)
