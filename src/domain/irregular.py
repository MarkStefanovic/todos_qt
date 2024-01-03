import calendar
import datetime
import functools
import itertools

from src.domain.weekday import Weekday

__all__ = ("x_weekday_of_month",)


@functools.lru_cache(maxsize=10000)
def x_weekday_of_month(*, year: int, month: int, week_num: int, week_day: Weekday) -> datetime.date:
    days_in_month = calendar.monthrange(year, month)[1]
    return list(
        itertools.islice(
            (
                dt
                for day in range(1, days_in_month, 1)
                if Weekday.from_int((dt := datetime.date(year, month, day)).weekday()) == week_day
            ),
            week_num,
        )
    )[-1]
