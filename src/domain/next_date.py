import datetime
import functools

from src.domain.easter import calculate_easter
from src.domain.frequency import Frequency
from src.domain.frequency_type import FrequencyType
from src.domain.irregular import x_weekday_of_month
from src.domain.memorial_day import calculate_memorial_day
from src.domain.weekday import Weekday

__all__ = ("next_date",)


def next_date(
    *,
    frequency: Frequency,
    today: datetime.date,
) -> datetime.date | None:
    if frequency.name == FrequencyType.Daily:
        return today + datetime.timedelta(days=1)
    elif frequency.name == FrequencyType.Easter:
        cy = calculate_easter(today.year)
        if cy > today:
            return cy
        return calculate_easter(today.year + 1)
    elif frequency.name == FrequencyType.Irregular:
        assert frequency.month is not None, f"The frequency was 'irregular', but [month] was {frequency.month!r}."
        assert frequency.week_day is not None, f"The frequency was 'irregular', but [week_day] was {frequency.week_day!r}."

        cy = x_weekday_of_month(
            year=today.year,
            month=frequency.month.to_int(),
            week_num=frequency.week_number,
            week_day=frequency.week_day,
        )
        if cy > today:
            return cy
        return x_weekday_of_month(
            year=today.year + 1,
            month=frequency.month.to_int(),
            week_num=frequency.week_number,
            week_day=frequency.week_day,
        )
    elif frequency.name == FrequencyType.MemorialDay:
        cy = calculate_memorial_day(year=today.year)
        if cy > today:
            return cy
        return calculate_memorial_day(year=today.year + 1)
    elif frequency.name == FrequencyType.Monthly:
        assert frequency.month_day is not None, f"The frequency was 'monthly' but [month_day] was {frequency.month_day!r}."

        return _monthly_next(
            year=today.year,
            month=today.month,
            month_day=frequency.month_day,
        )
    elif frequency.name == FrequencyType.Once:
        assert frequency.due_date is not None, f"The frequency was 'once' but [due_date] was {frequency.due_date!r}."

        if frequency.due_date > today:
            return frequency.due_date
        return None
    elif frequency.name == FrequencyType.Weekly:
        assert frequency.week_day is not None, f"The frequency was 'weekly' but [week_day] was {frequency.week_day!r}."

        day_offset = {
            1: {1: 7, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6},
            2: {1: 6, 2: 7, 3: 1, 4: 2, 5: 3, 6: 4, 7: 5},
            3: {1: 5, 2: 6, 3: 7, 4: 1, 5: 2, 6: 3, 7: 4},
            4: {1: 4, 2: 5, 3: 6, 4: 7, 5: 1, 6: 2, 7: 3},
            5: {1: 3, 2: 4, 3: 5, 4: 6, 5: 7, 6: 1, 7: 2},
            6: {1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 1},
            7: {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7},
        }[Weekday.from_date(today).value][frequency.week_day.value]

        return today + datetime.timedelta(days=day_offset)
    elif frequency.name == FrequencyType.XDays:
        assert frequency.days is not None, f"The frequency was 'xdays' but [days] was {frequency.days!r}."

        days_since_start = (today - frequency.start_date).days
        days_since_last = days_since_start % frequency.days

        prior_date = today - datetime.timedelta(days=days_since_last)
        current_date = prior_date + datetime.timedelta(days=frequency.days)
        if current_date > today:
            return current_date
        return current_date + datetime.timedelta(days=frequency.days)
    elif frequency.name == FrequencyType.Yearly:
        assert frequency.month is not None, f"The frequency was 'yearly' but [month] was {frequency.month!r}."
        assert frequency.month_day is not None, f"The frequency was 'yearly' but [month_day] was {frequency.month_day!r}."

        cy = datetime.date(today.year, month=frequency.month.value, day=frequency.month_day)
        if cy > today:
            return cy
        return datetime.date(today.year + 1, month=frequency.month.value, day=frequency.month_day)
    else:
        raise ValueError(f"Unrecognized frequency name, {frequency!r}")


@functools.lru_cache(maxsize=10000)
def _monthly_next(
    *,
    month: int,
    year: int,
    month_day: int,
) -> datetime.date:
    mo, yr = {
        1: (2, year),
        2: (3, year),
        3: (4, year),
        4: (5, year),
        5: (6, year),
        6: (7, year),
        7: (8, year),
        8: (9, year),
        9: (10, year),
        10: (11, year),
        11: (12, year),
        12: (1, year + 1),
    }[month]
    return datetime.date(yr, mo, month_day)
