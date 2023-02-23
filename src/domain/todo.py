from __future__ import annotations

import dataclasses
import datetime
import functools
import typing

from loguru import logger

from src.domain import date_calc
from src.domain.frequency_type import FrequencyType
from src.domain.category import Category, TODO_CATEGORY
from src.domain.frequency import Frequency
from src.domain.month import Month
from src.domain.user import DEFAULT_USER, User
from src.domain.weekday import Weekday

__all__ = ("Todo", "DEFAULT_TODO",)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Todo:
    todo_id: str
    user: User
    category: Category
    description: str
    frequency: Frequency
    note: str
    template_todo_id: str | None
    last_completed: datetime.date | None
    last_completed_by: User | None
    prior_completed: datetime.date | None
    prior_completed_by: User | None
    date_added: datetime.datetime
    date_updated: datetime.datetime | None

    @functools.cached_property
    def days(self) -> int | None:
        due_date = date_calc.due_date(frequency=self.frequency)
        if (
            self.last_completed
            and due_date
            and self.last_completed >= (due_date - datetime.timedelta(days=self.frequency.advance_display_days))
        ):
            if self.frequency.name == FrequencyType.Once:
                return None

            next_date = date_calc.next_date(frequency=self.frequency, ref_date=due_date)
            if next_date:
                return (next_date - datetime.date.today()).days
            return None

        if due_date is None:
            return None

        return (due_date - datetime.date.today()).days

    @functools.cached_property
    def due_date(self) -> datetime.date:
        try:
            return date_calc.due_date(frequency=self.frequency) or datetime.date(1900, 1, 1)
        except Exception as e:
            logger.exception(f"Failed to calculate due_date() for todo, {self.description}\n{e}")
            raise e

    @functools.cached_property
    def should_display(self) -> bool:
        try:
            if self.last_completed:
                latest: datetime.date | None = self.last_completed
            elif self.prior_completed:
                latest = self.prior_completed
            else:
                latest = None

            return date_calc.should_display(frequency=self.frequency, last_completed=latest)
        except Exception as e:
            logger.exception(f"Failed to calculate should_display() for todo, {self.description}\n{e}")
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
        last_completed_by: typing.Optional[User],
        prior_completed_by: typing.Optional[User],
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
            last_completed_by=last_completed_by,
            prior_completed_by=prior_completed_by,
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
        last_completed_by: typing.Optional[User],
        prior_completed_by: typing.Optional[User],
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
            last_completed_by=last_completed_by,
            prior_completed_by=prior_completed_by,
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
        last_completed_by: typing.Optional[User],
        prior_completed_by: typing.Optional[User],
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
            last_completed_by=last_completed_by,
            prior_completed_by=prior_completed_by,
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
        last_completed_by: typing.Optional[User],
        prior_completed_by: typing.Optional[User],
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
            last_completed_by=last_completed_by,
            prior_completed_by=prior_completed_by,
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
        last_completed_by: typing.Optional[User],
        prior_completed_by: typing.Optional[User],
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
            last_completed_by=last_completed_by,
            prior_completed_by=prior_completed_by,
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
        last_completed_by: typing.Optional[User],
        prior_completed_by: typing.Optional[User],
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
            last_completed_by=last_completed_by,
            prior_completed_by=prior_completed_by,
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
        last_completed_by: typing.Optional[User],
        prior_completed_by: typing.Optional[User],
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
            last_completed_by=last_completed_by,
            prior_completed_by=prior_completed_by,
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
    last_completed_by=None,
    prior_completed_by=None,
    user=DEFAULT_USER,
    category=TODO_CATEGORY,
    date_added=datetime.datetime.now(),
    date_updated=None,
)
