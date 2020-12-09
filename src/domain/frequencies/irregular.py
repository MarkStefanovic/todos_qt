from __future__ import annotations

import calendar
import datetime
import functools
import itertools
import typing

from src.domain import frequency_db_name, frequency, month, weekday

__all__ = ("Irregular",)


class Irregular(frequency.Frequency):
    def __init__(
        self,
        *,
        month: month.Month,
        week_day: weekday.Weekday,
        week_number: int,
    ):
        self._month = month
        self._week_day = week_day
        self._week_number = week_number

    def current_date(
        self, *, advance_days: int, today: datetime.date = datetime.date.today()
    ) -> datetime.date:
        assert advance_days < 365
        dt1 = get_x_weekday_of_month(
            year=today.year,
            month=self._month,
            week_num=self._week_number,
            week_day=self._week_day,
        )
        dt2 = get_x_weekday_of_month(
            year=today.year + 1,
            month=self._month,
            week_num=self._week_number,
            week_day=self._week_day,
        )
        if today > dt2 - datetime.timedelta(days=advance_days):
            return dt2
        else:
            return dt1

    @staticmethod
    def db_name() -> typing.Literal[frequency_db_name.FrequencyDbName.IRREGULAR]:
        return frequency_db_name.FrequencyDbName.IRREGULAR

    @property
    def month(self) -> int:
        return self._month

    @property
    def week_day(self) -> weekday.Weekday:
        return self._week_day

    @property
    def week_number(self) -> int:
        return self._week_number

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(month={self._month!r}, week_number={self._week_number!r}, "
            f"week_day={self._week_day!r})"
        )

    def __str__(self) -> str:
        return f"Irregular"


@functools.lru_cache()
def get_x_weekday_of_month(
    year: int, month: int, week_num: int, week_day: weekday.Weekday
) -> datetime.date:
    days_in_month = calendar.monthrange(year, month)[1]
    return list(
        itertools.islice(
            (
                dt
                for day in range(1, days_in_month, 1)
                if (dt := datetime.date(year, month, day)).weekday()
                == week_day.py_weekday
            ),
            week_num,
        )
    )[-1]
