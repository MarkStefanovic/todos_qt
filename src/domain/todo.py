from __future__ import annotations

import dataclasses
import datetime

from src.domain.frequency import Frequency
from src.domain.month import Month
from src.domain.todo_category import TodoCategory
from src.domain.weekday import Weekday

__all__ = ("Todo", "DEFAULT_TODO",)


@dataclasses.dataclass(frozen=True)
class Todo:
    todo_id: str
    advance_days: int
    expire_days: int
    category: TodoCategory
    description: str
    frequency: Frequency
    note: str
    start_date: datetime.date | None
    date_added: datetime.datetime
    date_updated: datetime.datetime | None
    date_deleted: datetime.datetime | None

    @staticmethod
    def daily(
        *,
        category: TodoCategory,
        date_added: datetime.datetime,
        date_deleted: datetime.datetime | None,
        date_updated: datetime.datetime | None,
        description: str,
        note: str,
        start_date: datetime.date | None,
        todo_id: str,
    ) -> Todo:
        return Todo(
            todo_id=todo_id,
            advance_days=0,
            expire_days=0,
            category=category,
            description=description,
            frequency=Frequency.daily(),
            note=note,
            start_date=start_date,
            date_added=date_added,
            date_updated=date_updated,
            date_deleted=date_deleted,
        )

    @staticmethod
    def easter(*, todo_id: str) -> Todo:
        return Todo(
            todo_id=todo_id,
            advance_days=0,
            expire_days=0,
            category=TodoCategory.Holiday,
            description="Easter",
            frequency=Frequency.easter(),
            note="",
            start_date=datetime.date(1900, 1, 1),
            date_added=datetime.datetime(1900, 1, 1),
            date_updated=None,
            date_deleted=None,
        )

    @staticmethod
    def irregular(
        *,
        advance_days: int,
        category: TodoCategory,
        date_added: datetime.datetime,
        date_deleted: datetime.datetime | None,
        date_updated: datetime.datetime | None,
        description: str,
        expire_days: int,
        month: Month,
        note: str,
        start_date: datetime.date | None,
        todo_id: str,
        week_day: Weekday,
        week_number: int,
    ) -> Todo:
        return Todo(
            todo_id=todo_id,
            advance_days=advance_days,
            expire_days=expire_days,
            category=category,
            description=description,
            frequency=Frequency.irregular(
                month=month,
                week_day=week_day,
                week_number=week_number,
            ),
            note=note,
            start_date=start_date,
            date_added=date_added,
            date_updated=date_updated,
            date_deleted=date_deleted,
        )

    @staticmethod
    def monthly(
        *,
        advance_days: int,
        category: TodoCategory,
        date_added: datetime.datetime,
        date_deleted: datetime.datetime | None,
        date_updated: datetime.datetime | None,
        description: str,
        expire_days: int,
        month_day: int,
        note: str,
        start_date: datetime.date | None,
        todo_id: str,
    ) -> Todo:
        return Todo(
            todo_id=todo_id,
            advance_days=advance_days,
            expire_days=expire_days,
            category=category,
            description=description,
            frequency=Frequency.monthly(month_day=month_day),
            note=note,
            start_date=start_date,
            date_added=date_added,
            date_updated=date_updated,
            date_deleted=date_deleted,
        )

    @staticmethod
    def once(
        *,
        advance_days: int,
        category: TodoCategory,
        date_added: datetime.datetime,
        date_deleted: datetime.datetime | None,
        date_updated: datetime.datetime | None,
        description: str,
        due_date: datetime.date,
        expire_days: int,
        note: str,
        start_date: datetime.date | None,
        todo_id: str,
    ) -> Todo:
        return Todo(
            todo_id=todo_id,
            advance_days=advance_days,
            expire_days=expire_days,
            category=category,
            description=description,
            frequency=Frequency.once(due_date=due_date),
            note=note,
            start_date=start_date,
            date_added=date_added,
            date_updated=date_updated,
            date_deleted=date_deleted,
        )

    @staticmethod
    def weekly(
        *,
        advance_days: int,
        category: TodoCategory,
        date_added: datetime.datetime,
        date_deleted: datetime.datetime | None,
        date_updated: datetime.datetime | None,
        description: str,
        expire_days: int,
        note: str,
        start_date: datetime.date | None,
        todo_id: str,
        week_day: Weekday,
    ) -> Todo:
        return Todo(
            todo_id=todo_id,
            advance_days=advance_days,
            expire_days=expire_days,
            category=category,
            description=description,
            frequency=Frequency.weekly(week_day=week_day),
            note=note,
            start_date=start_date,
            date_added=date_added,
            date_updated=date_updated,
            date_deleted=date_deleted,
        )

    @staticmethod
    def xdays(
        *,
        advance_days: int,
        category: TodoCategory,
        date_added: datetime.datetime,
        date_deleted: datetime.datetime | None,
        date_updated: datetime.datetime | None,
        days: int,
        description: str,
        expire_days: int,
        note: str,
        start_date: datetime.date | None,
        todo_id: str,
    ) -> Todo:
        return Todo(
            todo_id=todo_id,
            advance_days=advance_days,
            expire_days=expire_days,
            category=category,
            description=description,
            frequency=Frequency.xdays(days=days),
            note=note,
            start_date=start_date,
            date_added=date_added,
            date_updated=date_updated,
            date_deleted=date_deleted,
        )

    @staticmethod
    def yearly(
        *,
        advance_days: int,
        category: TodoCategory,
        date_added: datetime.datetime,
        date_deleted: datetime.datetime | None,
        date_updated: datetime.datetime | None,
        description: str,
        expire_days: int,
        month: Month,
        month_day: int,
        note: str,
        start_date: datetime.date | None,
        todo_id: str,
    ) -> Todo:
        return Todo(
            todo_id=todo_id,
            advance_days=advance_days,
            expire_days=expire_days,
            category=category,
            description=description,
            frequency=Frequency.yearly(month=month, month_day=month_day),
            note=note,
            start_date=start_date,
            date_added=date_added,
            date_updated=date_updated,
            date_deleted=date_deleted,
        )


DEFAULT_TODO = Todo.daily(
    todo_id="",
    description="",
    start_date=datetime.date.today(),
    note="",
    category=TodoCategory.Todo,
    date_added=datetime.datetime.now(),
    date_updated=None,
    date_deleted=None,
)
