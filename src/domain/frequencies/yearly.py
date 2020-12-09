from __future__ import annotations

import datetime
import typing

from src.domain import frequency_db_name, frequency, month

__all__ = ("Yearly",)


class Yearly(frequency.Frequency):
    def __init__(
        self,
        *,
        day: int,
        month: month.Month,
    ):
        self._day = day
        self._month = month

    def current_date(
        self, *, advance_days: int, today: datetime.date = datetime.date.today()
    ) -> datetime.date:
        dt1 = datetime.date(year=today.year, month=self._month, day=self._day)
        dt2 = datetime.date(year=today.year + 1, month=self._month, day=self._day)
        if today > dt2 - datetime.timedelta(days=advance_days):
            return dt2
        else:
            return dt1

    @staticmethod
    def db_name() -> typing.Literal[frequency_db_name.FrequencyDbName.YEARLY]:
        return frequency_db_name.FrequencyDbName.YEARLY

    @property
    def day(self) -> int:
        return self._day

    @property
    def month(self) -> int:
        return self._month

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(day={self._day!r}, month={self._month!r})"

    def __str__(self) -> str:
        return f"{self._month!s} {self._day}"
