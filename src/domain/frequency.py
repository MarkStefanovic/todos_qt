from __future__ import annotations

import dataclasses
import datetime

from src.domain.frequency_type import FrequencyType
from src.domain.month import Month
from src.domain.weekday import Weekday

__all__ = ("Frequency",)


@dataclasses.dataclass(frozen=True)
class Frequency:
    name: FrequencyType
    month: Month | None
    week_day: Weekday | None
    week_number: int | None
    month_day: int | None
    days: int | None
    start_date: datetime.date
    advance_display_days: int
    expire_display_days: int
    due_date: datetime.date | None

    @staticmethod
    def daily(*, start_date: datetime.date) -> Frequency:
        return Frequency(
            name=FrequencyType.Daily,
            month=None,
            week_day=None,
            week_number=None,
            month_day=None,
            days=None,
            due_date=None,
            advance_display_days=0,
            expire_display_days=1,
            start_date=start_date,
        )

    @staticmethod
    def easter(
        *,
        advance_display_days: int,
        expire_display_days: int,
        start_date: datetime.date,
    ) -> Frequency:
        return Frequency(
            name=FrequencyType.Easter,
            month=None,
            week_day=None,
            week_number=None,
            month_day=None,
            days=None,
            due_date=None,
            advance_display_days=advance_display_days,
            expire_display_days=expire_display_days,
            start_date=start_date,
        )

    @staticmethod
    def irregular(
        *,
        month: Month,
        week_day: Weekday,
        week_number: int,
        advance_display_days: int,
        expire_display_days: int,
        start_date: datetime.date,
    ) -> Frequency:
        return Frequency(
            name=FrequencyType.Irregular,
            month=month,
            week_day=week_day,
            week_number=week_number,
            month_day=None,
            days=None,
            due_date=None,
            advance_display_days=advance_display_days,
            expire_display_days=expire_display_days,
            start_date=start_date,
        )

    @staticmethod
    def memorial_day(
        *,
        advance_display_days: int,
        expire_display_days: int,
        start_date: datetime.date,
    ) -> Frequency:
        return Frequency(
            name=FrequencyType.MemorialDay,
            month=None,
            week_day=None,
            week_number=None,
            month_day=None,
            days=None,
            due_date=None,
            advance_display_days=advance_display_days,
            expire_display_days=expire_display_days,
            start_date=start_date,
        )

    @staticmethod
    def monthly(
        *,
        month_day: int,
        advance_display_days: int,
        expire_display_days: int,
        start_date: datetime.date,
    ) -> Frequency:
        return Frequency(
            name=FrequencyType.Monthly,
            month=None,
            week_day=None,
            week_number=None,
            month_day=month_day,
            days=None,
            due_date=None,
            advance_display_days=advance_display_days,
            expire_display_days=expire_display_days,
            start_date=start_date,
        )

    @staticmethod
    def once(
        *,
        due_date: datetime.date,
        advance_display_days: int,
        expire_display_days: int,
        start_date: datetime.date,
    ) -> Frequency:
        return Frequency(
            name=FrequencyType.Once,
            month=None,
            week_day=None,
            week_number=None,
            month_day=None,
            days=None,
            due_date=due_date,
            advance_display_days=advance_display_days,
            expire_display_days=expire_display_days,
            start_date=start_date,
        )

    @staticmethod
    def weekly(
        *,
        week_day: Weekday,
        advance_display_days: int,
        expire_display_days: int,
        start_date: datetime.date,
    ) -> Frequency:
        return Frequency(
            name=FrequencyType.Weekly,
            month=None,
            week_day=week_day,
            week_number=None,
            month_day=None,
            days=None,
            due_date=None,
            advance_display_days=advance_display_days,
            expire_display_days=expire_display_days,
            start_date=start_date,
        )

    @staticmethod
    def xdays(
        *,
        days: int,
        advance_display_days: int,
        expire_display_days: int,
        start_date: datetime.date,
    ) -> Frequency:
        return Frequency(
            name=FrequencyType.XDays,
            month=None,
            week_day=None,
            week_number=None,
            month_day=None,
            days=days,
            due_date=None,
            advance_display_days=advance_display_days,
            expire_display_days=expire_display_days,
            start_date=start_date,
        )

    @staticmethod
    def yearly(
        *,
        month: Month,
        month_day: int,
        advance_display_days: int,
        expire_display_days: int,
        start_date: datetime.date,
    ) -> Frequency:
        return Frequency(
            name=FrequencyType.Yearly,
            month=month,
            week_day=None,
            week_number=None,
            month_day=month_day,
            days=None,
            due_date=None,
            advance_display_days=advance_display_days,
            expire_display_days=expire_display_days,
            start_date=start_date,
        )
