import datetime
import functools

import sqlalchemy as sa
import sqlmodel as sm

__all__ = ("get_engine", "Schedule", "Todo")


class Todo(sm.SQLModel, table=True):
    todo_id: str = sm.Field(primary_key=True)
    description: str
    note: str
    category: str
    advance_days: int
    expire_days: int
    start_date: datetime.date
    date_added: datetime.datetime
    date_updated: datetime.datetime | None
    date_deleted: datetime.datetime | None

    # frequncy fields
    frequency: str
    month: int | None
    week_day: int | None
    week_number: int | None
    month_day: int | None
    days: int | None
    due_date: datetime.date | None 


class Schedule(sm.SQLModel, table=True):
    schedule_id: str = sm.Field(primary_key=True)
    todo_id: str = sm.Field(foreign_key="todo.todo_id")
    due_date: datetime.date
    start_display: datetime.date
    end_display: datetime.date
    note: str
    date_completed: datetime.date | None
    date_added: datetime.datetime = sm.Field(default_factory=datetime.datetime.now)
    date_updated: datetime.datetime | None
    date_deleted: datetime.datetime | None


@functools.lru_cache(1)
def get_engine(*, url: str, echo: bool = False) -> sa.engine.Engine:
    engine = sm.create_engine(url, echo=echo)
    sm.SQLModel.metadata.create_all(engine)
    return engine
