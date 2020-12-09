from __future__ import annotations

import datetime
import typing

from src.domain import frequency_db_name, frequency

__all__ = ("Once",)


class Once(frequency.Frequency):
    def __init__(self, /, once_date: datetime.date):
        self._once_date = once_date

    def current_date(
        self, *, advance_days: int, today: datetime.date = datetime.date.today()
    ) -> datetime.date:
        return self._once_date

    @staticmethod
    def db_name() -> typing.Literal[frequency_db_name.FrequencyDbName.ONCE]:
        return frequency_db_name.FrequencyDbName.ONCE

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(once_date={self._once_date!r})"

    def __str__(self) -> str:
        return self._once_date.strftime("%Y-%m-%d")
