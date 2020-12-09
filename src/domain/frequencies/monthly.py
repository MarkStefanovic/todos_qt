from __future__ import annotations

import calendar
import datetime
import typing

from src.domain import frequency_db_name, frequency

__all__ = ("Monthly",)


class Monthly(frequency.Frequency):
    def __init__(self, /, month_day: int):
        self._month_day = month_day

    def current_date(
        self, *, advance_days: int, today: datetime.date = datetime.date.today()
    ) -> datetime.date:
        cm_days = calendar.monthrange(today.year, today.month)[1]
        next_month = today + datetime.timedelta(days=cm_days - today.day + 1)
        dt1 = datetime.date(year=today.year, month=today.month, day=self._month_day)
        dt2 = datetime.date(
            year=next_month.year, month=next_month.month, day=self._month_day
        )
        if today > dt2 - datetime.timedelta(days=advance_days):
            return dt2
        else:
            return dt1

    @staticmethod
    def db_name() -> typing.Literal[frequency_db_name.FrequencyDbName.MONTHLY]:
        return frequency_db_name.FrequencyDbName.MONTHLY

    @property
    def month_day(self) -> int:
        return self._month_day

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(month_day={self._month_day!r})"

    def __str__(self) -> str:
        return f"Monthly, day {self._month_day}"
