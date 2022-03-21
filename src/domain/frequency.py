from __future__ import annotations

import datetime

import pydantic

from src.domain.frequency_type import FrequencyType
from src.domain.month import Month
from src.domain.weekday import Weekday

__all__ = ("Frequency",)


class Frequency(pydantic.BaseModel):
    name: FrequencyType
    month: Month | None
    week_day: Weekday | None
    week_number: int | None
    month_day: int | None
    days: int | None
    due_date: datetime.date | None

    class Config:
        frozen = True

    @staticmethod
    def daily() -> Frequency:
        return Frequency(
            name=FrequencyType.Daily,
            month=None,
            week_day=None,
            week_number=None,
            month_day=None,
            days=None,
            due_date=None,
        )

    @staticmethod
    def easter() -> Frequency:
        return Frequency(
            name=FrequencyType.Easter,
            month=None,
            week_day=None,
            week_number=None,
            month_day=None,
            days=None,
            due_date=None,
        )

    @staticmethod
    def irregular(
        *,
        month: Month,
        week_day: Weekday,
        week_number: int,
    ) -> Frequency:
        return Frequency(
            name=FrequencyType.Irregular,
            month=month,
            week_day=week_day,
            week_number=week_number,
            month_day=None,
            days=None,
            due_date=None,
        )

    @staticmethod
    def monthly(*, month_day: int) -> Frequency:
        return Frequency(
            name=FrequencyType.Monthly,
            month=None,
            week_day=None,
            week_number=None,
            month_day=month_day,
            days=None,
            due_date=None,
        )

    @staticmethod
    def once(*, due_date: datetime.date) -> Frequency:
        return Frequency(
            name=FrequencyType.Once,
            month=None,
            week_day=None,
            week_number=None,
            month_day=None,
            days=None,
            due_date=due_date,
        )

    @staticmethod
    def weekly(*, week_day: Weekday) -> Frequency:
        return Frequency(
            name=FrequencyType.Weekly,
            month=None,
            week_day=week_day,
            week_number=None,
            month_day=None,
            days=None,
            due_date=None,
        )

    @staticmethod
    def xdays(*, days: int) -> Frequency:
        return Frequency(
            name=FrequencyType.XDays,
            month=None,
            week_day=None,
            week_number=None,
            month_day=None,
            days=days,
            due_date=None,
        )

    @staticmethod
    def yearly(*, month: Month, month_day: int) -> Frequency:
        return Frequency(
            name=FrequencyType.Yearly,
            month=month,
            week_day=None,
            week_number=None,
            month_day=month_day,
            days=None,
            due_date=None,
        )
