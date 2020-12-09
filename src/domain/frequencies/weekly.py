from __future__ import annotations

import datetime
import typing

from src.domain import frequency_db_name, frequency, weekday

__all__ = ("Weekly",)


class Weekly(frequency.Frequency):
    def __init__(self, /, week_day: weekday.Weekday):
        self._week_day = week_day

    def current_date(
        self, *, advance_days: int, today: datetime.date = datetime.date.today()
    ) -> datetime.date:
        weekday_diff = weekday.Weekday.from_date(today).value - self._week_day.value
        if weekday_diff == 0:
            next_date = today
        elif weekday_diff < 0:
            next_date = today - datetime.timedelta(days=weekday_diff)
        else:
            next_date = today + datetime.timedelta(days=7 - weekday_diff)

        if today >= next_date - datetime.timedelta(days=advance_days):
            return next_date
        else:
            return next_date - datetime.timedelta(days=7)

    @staticmethod
    def db_name() -> typing.Literal[frequency_db_name.FrequencyDbName.WEEKLY]:
        return frequency_db_name.FrequencyDbName.WEEKLY

    @property
    def week_day(self) -> weekday.Weekday:
        return self._week_day

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(weekday={self._week_day!r})"

    def __str__(self) -> str:
        return self._week_day.short_name
