import datetime
import functools

__all__ = ("calculate_memorial_day",)


@functools.lru_cache(maxsize=1000)
def calculate_memorial_day(*, year: int) -> datetime.date:
    dt = datetime.date(year, 6, 1) - datetime.timedelta(days=1)
    while dt.weekday() > 0:
        dt -= datetime.timedelta(days=1)
    return dt
