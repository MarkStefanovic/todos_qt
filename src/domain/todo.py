from __future__ import annotations

import dataclasses
import datetime
import typing

from loguru import logger

from src.domain.category import Category, TODO_CATEGORY
from src.domain.due_date import due_date
from src.domain.frequency import Frequency
from src.domain.month import Month
from src.domain.should_display import should_display
from src.domain.user import DEFAULT_USER, User
from src.domain.weekday import Weekday

__all__ = ("Todo", "DEFAULT_TODO",)


@dataclasses.dataclass(frozen=True)
class Todo:
    todo_id: str
    user: User
    category: Category
    description: str
    frequency: Frequency
    note: str
    template_todo_id: str | None
    last_completed: datetime.date | None
    prior_completed: datetime.date | None
    date_added: datetime.datetime
    date_updated: datetime.datetime | None

    def due_date(self, *, today: datetime.date) -> datetime.date:
        try:
            return due_date(
                frequency=self.frequency,
                today=today,
                last_completed=self.last_completed,
            )
        except Exception as e:
            logger.exception(f"Failed to calculate due_date({today=}) for todo, {self.description}\n{e}")
            raise e

    def should_display(self, *, today: datetime.date) -> bool:
        try:
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
        except Exception as e:
            logger.exception(f"Failed to calculate should_display({today=}) for todo, {self.description}\n{e}")
            raise e

    @staticmethod
    def daily(
        *,
        user: User,
        category: Category,
        description: str,
        note: str,
        start_date: datetime.date,
        todo_id: str,
        template_todo_id: str | None,
        last_completed: typing.Optional[datetime.date],
        prior_completed: typing.Optional[datetime.date],
        date_added: datetime.datetime,
        date_updated: typing.Optional[datetime.datetime],
    ) -> Todo:
        return Todo(
            todo_id=todo_id,
            user=user,
            category=category,
            description=description,
            frequency=Frequency.daily(start_date=start_date),
            note=note,
            template_todo_id=template_todo_id,
            last_completed=last_completed,
            prior_completed=prior_completed,
            date_added=date_added,
            date_updated=date_updated,
        )

    @staticmethod
    def irregular(
        *,
        user: User,
        category: Category,
        description: str,
        month: Month,
        note: str,
        start_date: datetime.date,
        todo_id: str,
        week_day: Weekday,
        week_number: int,
        advance_display_days: int,
        expire_display_days: int,
        template_todo_id: str | None,
        last_completed: typing.Optional[datetime.date],
        prior_completed: typing.Optional[datetime.date],
        date_added: datetime.datetime,
        date_updated: typing.Optional[datetime.datetime],
    ) -> Todo:
        return Todo(
            todo_id=todo_id,
            user=user,
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
            template_todo_id=template_todo_id,
            last_completed=last_completed,
            prior_completed=prior_completed,
            date_added=date_added,
            date_updated=date_updated,
        )

    @staticmethod
    def monthly(
        *,
        user: User,
        category: Category,
        description: str,
        month_day: int,
        note: str,
        start_date: datetime.date,
        todo_id: str,
        advance_display_days: int,
        expire_display_days: int,
        template_todo_id: str | None,
        last_completed: typing.Optional[datetime.date],
        prior_completed: typing.Optional[datetime.date],
        date_added: datetime.datetime,
        date_updated: typing.Optional[datetime.datetime],
    ) -> Todo:
        return Todo(
            todo_id=todo_id,
            user=user,
            category=category,
            description=description,
            frequency=Frequency.monthly(
                month_day=month_day,
                start_date=start_date,
                advance_display_days=advance_display_days,
                expire_display_days=expire_display_days,
            ),
            note=note,
            template_todo_id=template_todo_id,
            last_completed=last_completed,
            prior_completed=prior_completed,
            date_added=date_added,
            date_updated=date_updated,
        )

    @staticmethod
    def once(
        *,
        user: User,
        category: Category,
        description: str,
        due_date: datetime.date,
        note: str,
        start_date: datetime.date,
        todo_id: str,
        advance_display_days: int,
        expire_display_days: int,
        template_todo_id: str | None,
        last_completed: typing.Optional[datetime.date],
        prior_completed: typing.Optional[datetime.date],
        date_added: datetime.datetime,
        date_updated: typing.Optional[datetime.datetime],
    ) -> Todo:
        return Todo(
            todo_id=todo_id,
            user=user,
            category=category,
            description=description,
            frequency=Frequency.once(
                due_date=due_date,
                start_date=start_date,
                advance_display_days=advance_display_days,
                expire_display_days=expire_display_days,
            ),
            note=note,
            template_todo_id=template_todo_id,
            last_completed=last_completed,
            prior_completed=prior_completed,
            date_added=date_added,
            date_updated=date_updated,
        )

    @staticmethod
    def weekly(
        *,
        user: User,
        category: Category,
        description: str,
        note: str,
        start_date: datetime.date,
        todo_id: str,
        week_day: Weekday,
        advance_display_days: int,
        expire_display_days: int,
        template_todo_id: str | None,
        last_completed: typing.Optional[datetime.date],
        prior_completed: typing.Optional[datetime.date],
        date_added: datetime.datetime,
        date_updated: typing.Optional[datetime.datetime],
    ) -> Todo:
        return Todo(
            todo_id=todo_id,
            user=user,
            category=category,
            description=description,
            frequency=Frequency.weekly(
                week_day=week_day,
                start_date=start_date,
                advance_display_days=advance_display_days,
                expire_display_days=expire_display_days,
            ),
            note=note,
            template_todo_id=template_todo_id,
            last_completed=last_completed,
            prior_completed=prior_completed,
            date_added=date_added,
            date_updated=date_updated,
        )

    @staticmethod
    def xdays(
        *,
        user: User,
        category: Category,
        days: int,
        description: str,
        note: str,
        start_date: datetime.date,
        todo_id: str,
        advance_display_days: int,
        expire_display_days: int,
        template_todo_id: str | None,
        last_completed: typing.Optional[datetime.date],
        prior_completed: typing.Optional[datetime.date],
        date_added: datetime.datetime,
        date_updated: typing.Optional[datetime.datetime],
    ) -> Todo:
        return Todo(
            todo_id=todo_id,
            user=user,
            category=category,
            description=description,
            frequency=Frequency.xdays(
                days=days,
                start_date=start_date,
                advance_display_days=advance_display_days,
                expire_display_days=expire_display_days,
            ),
            note=note,
            template_todo_id=template_todo_id,
            last_completed=last_completed,
            prior_completed=prior_completed,
            date_added=date_added,
            date_updated=date_updated,
        )

    @staticmethod
    def yearly(
        *,
        user: User,
        category: Category,
        description: str,
        month: Month,
        month_day: int,
        note: str,
        start_date: datetime.date,
        todo_id: str,
        advance_display_days: int,
        expire_display_days: int,
        template_todo_id: str | None,
        last_completed: typing.Optional[datetime.date],
        prior_completed: typing.Optional[datetime.date],
        date_added: datetime.datetime,
        date_updated: typing.Optional[datetime.datetime],
    ) -> Todo:
        return Todo(
            todo_id=todo_id,
            user=user,
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
            template_todo_id=template_todo_id,
            last_completed=last_completed,
            prior_completed=prior_completed,
            date_added=date_added,
            date_updated=date_updated,
        )


DEFAULT_TODO = Todo.daily(
    todo_id="",
    description="",
    start_date=datetime.date.today(),
    note="",
    template_todo_id=None,
    last_completed=None,
    prior_completed=None,
    user=DEFAULT_USER,
    category=TODO_CATEGORY,
    date_added=datetime.datetime.now(),
    date_updated=None,
)
