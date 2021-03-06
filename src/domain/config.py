from __future__ import annotations

import pydantic

__all__ = ("Config",)


class Config(pydantic.BaseModel):
    sqlalchemy_url: str
    schema_name: str | None
    add_holidays: bool
    admin_usernames: list[str]

    class Config:
        extra = pydantic.Extra.ignore
        frozen = True
