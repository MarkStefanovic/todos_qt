import dataclasses

__all__ = ("Config",)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Config:
    sqlalchemy_url: str
    schema_name: str | None
    add_holidays: bool
    admin_usernames: list[str]
