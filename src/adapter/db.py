import datetime
import functools

import sqlalchemy as sa
import sqlmodel as sm

from src.adapter.json_config import config

__all__ = ("get_engine", "Todo")


class Todo(sm.SQLModel, table=True):
    __table_args__ = {"schema": config().schema_name}

    todo_id: str = sm.Field(primary_key=True)
    description: str
    note: str
    user_id: str
    category_id: str
    advance_days: int
    expire_days: int
    start_date: datetime.date
    last_completed: datetime.date | None
    prior_completed: datetime.date | None

    date_added: datetime.datetime
    date_updated: datetime.datetime | None
    date_deleted: datetime.datetime | None

    # frequency fields
    frequency: str
    month: int | None
    week_day: int | None
    week_number: int | None
    month_day: int | None
    days: int | None
    due_date: datetime.date | None 


class Category(sm.SQLModel, table=True):
    __table_args__ = {"schema": config().schema_name}

    category_id: str = sm.Field(primary_key=True)
    name: str
    note: str
    date_added: datetime.datetime
    date_updated: datetime.datetime | None
    date_deleted: datetime.datetime | None


class User(sm.SQLModel, table=True):
    __table_args__ = {"schema": config().schema_name}

    user_id: str = sm.Field(primary_key=True)
    display_name: str
    username: str
    is_admin: bool
    date_added: datetime.datetime
    date_updated: datetime.datetime | None
    date_deleted: datetime.datetime | None


@functools.lru_cache(1)
def get_engine(*, url: str, echo: bool = False) -> sa.engine.Engine:
    engine = sm.create_engine(url, echo=echo)
    sm.SQLModel.metadata.create_all(engine)
    return engine
