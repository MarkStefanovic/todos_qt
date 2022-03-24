from __future__ import annotations

import dataclasses
import datetime

from src.domain.should_display import should_display
from src.domain.due_date import due_date
from src.domain.frequency import Frequency
from src.domain.month import Month
from src.domain.todo_category import TodoCategory
from src.domain.weekday import Weekday

__all__ = ("Todo", "DEFAULT_TODO",)


@dataclasses.dataclass(frozen=True)
class Todo:
    todo_id: str
    category: TodoCategory
    description: str
    frequency: Frequency
    note: str
    last_completed: datetime.date | None
    prior_completed: datetime.date | None
    date_added: datetime.datetime
    date_updated: datetime.datetime | None
    date_deleted: datetime.datetime | None

    def due_date(self, *, today: datetime.date) -> datetime.date:
        return due_date(frequency=self.frequency, today=today)

    def should_display(self, *, today: datetime.date) -> bool:
        if self.last_completed:
            latest: datetime.date | None = self.last_completed
        elif self.prior_completed:
            latest = self.prior_completed
        else:
            latest = None

        return should_display(
            frequency=self.frequency,
            today=today,
            last_completed=latest,
        )

    @staticmethod
    def daily(
        *,
        category: TodoCategory,
        description: str,
        note: str,
        start_date: datetime.date,
        todo_id: str,
        last_completed: datetime.date | None,
        prior_completed: datetime.date | None,
        date_added: datetime.datetime,
        date_deleted: datetime.datetime | None,
        date_updated: datetime.datetime | None,
    ) -> Todo:
        return Todo(
            todo_id=todo_id,
            category=category,
            description=description,
            frequency=Frequency.daily(start_date=start_date),
            note=note,
            last_completed=last_completed,
            prior_completed=prior_completed,
            date_added=date_added,
            date_updated=date_updated,
            date_deleted=date_deleted,
        )

    @staticmethod
    def easter(
        *,
        todo_id: str,
        advance_display_days: int,
        expire_display_days: int,
        last_completed: datetime.date | None,
        prior_completed: datetime.date | None,
        date_updated: datetime.datetime | None,
        date_deleted: datetime.datetime | None,
    ) -> Todo:
        return Todo(
            todo_id=todo_id,
            category=TodoCategory.Holiday,
            description="Easter",
            frequency=Frequency.easter(
                start_date=datetime.date(1900, 1, 1),
                advance_display_days=advance_display_days,
                expire_display_days=expire_display_days,
            ),
            note="",
            last_completed=last_completed,
            prior_completed=prior_completed,
            date_added=datetime.datetime(1900, 1, 1),
            date_updated=date_updated,
            date_deleted=date_deleted,
        )

    @staticmethod
    def irregular(
        *,
        category: TodoCategory,
        description: str,
        month: Month,
        note: str,
        start_date: datetime.date,
        todo_id: str,
        week_day: Weekday,
        week_number: int,
        advance_display_days: int,
        expire_display_days: int,
        last_completed: datetime.date | None,
        prior_completed: datetime.date | None,
        date_added: datetime.datetime,
        date_deleted: datetime.datetime | None,
        date_updated: datetime.datetime | None,
    ) -> Todo:
        return Todo(
            todo_id=todo_id,
            category=category,
            description=description,
            frequency=Frequency.irregular(
                month=month,
                week_day=week_day,
                week_number=week_number,
                start_date=start_date,
                advance_display_days=advance_display_days,
                expire_display_days=expire_display_days,
            ),
            note=note,
            last_completed=last_completed,
            prior_completed=prior_completed,
            date_added=date_added,
            date_updated=date_updated,
            date_deleted=date_deleted,
        )

    @staticmethod
    def monthly(
        *,
        category: TodoCategory,
        description: str,
        month_day: int,
        note: str,
        start_date: datetime.date,
        todo_id: str,
        advance_display_days: int,
        expire_display_days: int,
        last_completed: datetime.date | None,
        prior_completed: datetime.date | None,
        date_added: datetime.datetime,
        date_deleted: datetime.datetime | None,
        date_updated: datetime.datetime | None,
    ) -> Todo:
        return Todo(
            todo_id=todo_id,
            category=category,
            description=description,
            frequency=Frequency.monthly(
                month_day=month_day,
                start_date=start_date,
                advance_display_days=advance_display_days,
                expire_display_days=expire_display_days,
            ),
            note=note,
            last_completed=last_completed,
            prior_completed=prior_completed,
            date_added=date_added,
            date_updated=date_updated,
            date_deleted=date_deleted,
        )

    @staticmethod
    def once(
        *,
        category: TodoCategory,
        description: str,
        due_date: datetime.date,
        note: str,
        start_date: datetime.date,
        todo_id: str,
        advance_display_days: int,
        expire_display_days: int,
        last_completed: datetime.date | None,
        prior_completed: datetime.date | None,
        date_added: datetime.datetime,
        date_deleted: datetime.datetime | None,
        date_updated: datetime.datetime | None,
    ) -> Todo:
        return Todo(
            todo_id=todo_id,
            category=category,
            description=description,
            frequency=Frequency.once(
                due_date=due_date,
                start_date=start_date,
                advance_display_days=advance_display_days,
                expire_display_days=expire_display_days,
            ),
            note=note,
            last_completed=last_completed,
            prior_completed=prior_completed,
            date_added=date_added,
            date_updated=date_updated,
            date_deleted=date_deleted,
        )

    @staticmethod
    def weekly(
        *,
        category: TodoCategory,
        description: str,
        note: str,
        start_date: datetime.date,
        todo_id: str,
        week_day: Weekday,
        advance_display_days: int,
        expire_display_days: int,
        last_completed: datetime.date | None,
        prior_completed: datetime.date | None,
        date_added: datetime.datetime,
        date_deleted: datetime.datetime | None,
        date_updated: datetime.datetime | None,
    ) -> Todo:
        return Todo(
            todo_id=todo_id,
            category=category,
            description=description,
            frequency=Frequency.weekly(
                week_day=week_day,
                start_date=start_date,
                advance_display_days=advance_display_days,
                expire_display_days=expire_display_days,
            ),
            note=note,
            last_completed=last_completed,
            prior_completed=prior_completed,
            date_added=date_added,
            date_updated=date_updated,
            date_deleted=date_deleted,
        )

    @staticmethod
    def xdays(
        *,
        category: TodoCategory,
        days: int,
        description: str,
        note: str,
        start_date: datetime.date,
        todo_id: str,
        advance_display_days: int,
        expire_display_days: int,
        last_completed: datetime.date | None,
        prior_completed: datetime.date | None,
        date_added: datetime.datetime,
        date_deleted: datetime.datetime | None,
        date_updated: datetime.datetime | None,
    ) -> Todo:
        return Todo(
            todo_id=todo_id,
            category=category,
            description=description,
            frequency=Frequency.xdays(
                days=days,
                start_date=start_date,
                advance_display_days=advance_display_days,
                expire_display_days=expire_display_days,
            ),
            note=note,
            last_completed=last_completed,
            prior_completed=prior_completed,
            date_added=date_added,
            date_updated=date_updated,
            date_deleted=date_deleted,
        )

    @staticmethod
    def yearly(
        *,
        category: TodoCategory,
        description: str,
        month: Month,
        month_day: int,
        note: str,
        start_date: datetime.date,
        todo_id: str,
        advance_display_days: int,
        expire_display_days: int,
        last_completed: datetime.date | None,
        prior_completed: datetime.date | None,
        date_added: datetime.datetime,
        date_deleted: datetime.datetime | None,
        date_updated: datetime.datetime | None,
    ) -> Todo:
        return Todo(
            todo_id=todo_id,
            category=category,
            description=description,
            frequency=Frequency.yearly(
                month=month,
                month_day=month_day,
                start_date=start_date,
                advance_display_days=advance_display_days,
                expire_display_days=expire_display_days,
            ),
            note=note,
            last_completed=last_completed,
            prior_completed=prior_completed,
            date_added=date_added,
            date_updated=date_updated,
            date_deleted=date_deleted,
        )


DEFAULT_TODO = Todo.daily(
    todo_id="",
    description="",
    start_date=datetime.date.today(),
    note="",
    last_completed=None,
    prior_completed=None,
    category=TodoCategory.Todo,
    date_added=datetime.datetime.now(),
    date_updated=None,
    date_deleted=None,
)
