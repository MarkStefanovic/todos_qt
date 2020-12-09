from __future__ import annotations

import datetime
import typing

from src.domain import frequency_db_name, frequency

__all__ = ("XDays",)


class XDays(frequency.Frequency):
    def __init__(
        self,
        *,
        start_date: datetime.date,
        days: int,
    ):
        self._start_date = start_date
        self._days = days

    def current_date(
        self, *, advance_days: int, today: datetime.date = datetime.date.today()
    ) -> datetime.date:
        days_since_start = (today - self._start_date).days
        days_since_last = days_since_start % self._days
        prior_date = today - datetime.timedelta(days=days_since_last)
        return prior_date + datetime.timedelta(days=self._days)

    @staticmethod
    def db_name() -> typing.Literal[frequency_db_name.FrequencyDbName.XDAYS]:
        return frequency_db_name.FrequencyDbName.XDAYS

    @property
    def days(self) -> int:
        return self._days

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(days={self._days!r}, start_date={self._start_date!r})"

    def __str__(self) -> str:
        return f"Every {self._days} days"
