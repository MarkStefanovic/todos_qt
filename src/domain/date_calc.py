import datetime
import functools

from src.domain.frequency import Frequency
from src.domain.frequency_type import FrequencyType
from src.domain.weekday import Weekday
from src.domain.easter import calculate_easter
from src.domain.irregular import x_weekday_of_month
from src.domain.memorial_day import calculate_memorial_day

__all__ = (
    "due_date",
    "next_date",
    "prior_date",
    "should_display",
)


@functools.lru_cache(10000)
def due_date(*, frequency: Frequency) -> datetime.date | None:
    today = datetime.date.today()

    if frequency.name == FrequencyType.Once:
        assert frequency.due_date is not None, "Frequency was Once, but [due_date] was None."
        return frequency.due_date
    elif frequency.name == FrequencyType.Daily:
        return today
    else:
        prior_due_date = prior_date(frequency=frequency)
        assert prior_due_date is not None, f"If the frequency is not Once, then prior_due_date should not be None."
        # assert prior_due_date < today
        current_due_date = next_date(frequency=frequency, ref_date=prior_due_date)
        assert current_due_date is not None, f"If the frequency is not Once, then current_due_date should not be None."
        next_due_date = next_date(frequency=frequency, ref_date=current_due_date)
        assert next_due_date is not None, f"If the frequency is not Once, then next_due_date should not be None."
        # assert next_due_date > today
        return next(
            (
                dt for dt in (next_due_date, current_due_date, prior_due_date)
                if today >= dt - datetime.timedelta(days=frequency.advance_display_days)
            ),
            None
        )


def next_date(*, frequency: Frequency, ref_date: datetime.date) -> datetime.date | None:
    if frequency.name == FrequencyType.Daily:
        return ref_date + datetime.timedelta(days=1)
    elif frequency.name == FrequencyType.Easter:
        cy = calculate_easter(ref_date.year)
        if cy > ref_date:
            return cy
        return calculate_easter(ref_date.year + 1)
    elif frequency.name == FrequencyType.Irregular:
        assert frequency.month is not None, f"The frequency was 'irregular', but [month] was {frequency.month!r}."
        assert frequency.week_day is not None, f"The frequency was 'irregular', but [week_day] was {frequency.week_day!r}."

        cy = x_weekday_of_month(
            year=ref_date.year,
            month=frequency.month.to_int(),
            week_num=frequency.week_number,
            week_day=frequency.week_day,
        )
        if cy > ref_date:
            return cy
        return x_weekday_of_month(
            year=ref_date.year + 1,
            month=frequency.month.to_int(),
            week_num=frequency.week_number,
            week_day=frequency.week_day,
        )
    elif frequency.name == FrequencyType.MemorialDay:
        cy = calculate_memorial_day(year=ref_date.year)
        if cy > ref_date:
            return cy
        return calculate_memorial_day(year=ref_date.year + 1)
    elif frequency.name == FrequencyType.Monthly:
        assert frequency.month_day is not None, f"The frequency was 'monthly' but [month_day] was {frequency.month_day!r}."

        return _monthly_next(
            year=ref_date.year,
            month=ref_date.month,
            month_day=frequency.month_day,
        )
    elif frequency.name == FrequencyType.Once:
        assert frequency.due_date is not None, f"The frequency was 'once' but [due_date] was {frequency.due_date!r}."

        if frequency.due_date > ref_date:
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
        }[Weekday.from_date(ref_date).value][frequency.week_day.value]

        return ref_date + datetime.timedelta(days=day_offset)
    elif frequency.name == FrequencyType.XDays:
        assert frequency.days is not None, f"The frequency was 'xdays' but [days] was {frequency.days!r}."

        days_since_start = (ref_date - frequency.start_date).days
        days_since_last = days_since_start % frequency.days

        prior_date = ref_date - datetime.timedelta(days=days_since_last)
        current_date = prior_date + datetime.timedelta(days=frequency.days)
        if current_date > ref_date:
            return current_date
        return current_date + datetime.timedelta(days=frequency.days)
    elif frequency.name == FrequencyType.Yearly:
        assert frequency.month is not None, f"The frequency was 'yearly' but [month] was {frequency.month!r}."
        assert frequency.month_day is not None, f"The frequency was 'yearly' but [month_day] was {frequency.month_day!r}."

        cy = datetime.date(ref_date.year, month=frequency.month.value, day=frequency.month_day)
        if cy > ref_date:
            return cy
        return datetime.date(ref_date.year + 1, month=frequency.month.value, day=frequency.month_day)
    else:
        raise ValueError(f"Unrecognized frequency name, {frequency!r}")


def prior_date(frequency: Frequency) -> datetime.date | None:
    today = datetime.date.today()

    if frequency.name == FrequencyType.Daily:
        return today - datetime.timedelta(days=1)
    elif frequency.name == FrequencyType.Easter:
        cy = calculate_easter(today.year)
        if cy < today:
            return cy
        return calculate_easter(today.year - 1)
    elif frequency.name == FrequencyType.Irregular:
        assert frequency.month is not None, f"The frequency was 'irregular', but [month] was {frequency.month!r}."
        assert frequency.week_day is not None, f"The frequency was 'irregular', but [week_day] was {frequency.week_day!r}."

        cy = x_weekday_of_month(
            year=today.year,
            month=frequency.month.to_int(),
            week_num=frequency.week_number,
            week_day=frequency.week_day,
        )
        if cy < today:
            return cy
        return x_weekday_of_month(
            year=today.year - 1,
            month=frequency.month.to_int(),
            week_num=frequency.week_number,
            week_day=frequency.week_day,
        )
    elif frequency.name == FrequencyType.MemorialDay:
        cy = calculate_memorial_day(year=today.year)
        if cy < today:
            return cy
        return calculate_memorial_day(year=today.year - 1)
    elif frequency.name == FrequencyType.Monthly:
        assert frequency.month_day is not None, f"The frequency was 'monthly' but [month_day] was {frequency.month_day!r}."

        cy = _monthly_prior(
            year=today.year,
            month=today.month,
            month_day=frequency.month_day,
        )
        if cy < today:
            return cy
        return _monthly_prior(
            year=today.year - 1,
            month=today.month,
            month_day=frequency.month_day,
        )
    elif frequency.name == FrequencyType.Once:
        assert frequency.due_date is not None, f"The frequency was 'once' but [due_date] was {frequency.due_date!r}."

        if frequency.due_date < today:
            return None
        return frequency.due_date
    elif frequency.name == FrequencyType.Weekly:
        assert frequency.week_day is not None, f"The frequency was 'weekly' but [week_day] was {frequency.week_day!r}."

        day_offset = {
            1: {1: -7, 2: -6, 3: -5, 4: -4, 5: -3, 6: -2, 7: -1},
            2: {1: -1, 2: -7, 3: -6, 4: -5, 5: -4, 6: -3, 7: -2},
            3: {1: -2, 2: -1, 3: -7, 4: -6, 5: -5, 6: -4, 7: -3},
            4: {1: -3, 2: -2, 3: -1, 4: -7, 5: -6, 6: -5, 7: -4},
            5: {1: -4, 2: -3, 3: -2, 4: -1, 5: -7, 6: -6, 7: -5},
            6: {1: -5, 2: -4, 3: -3, 4: -2, 5: -1, 6: -7, 7: -6},
            7: {1: -6, 2: -5, 3: -4, 4: -3, 5: -2, 6: -1, 7: -7},
        }[Weekday.from_date(today).value][frequency.week_day.value]

        return today + datetime.timedelta(days=day_offset)

    elif frequency.name == FrequencyType.XDays:
        assert frequency.days is not None, f"The frequency was 'xdays' but [days] was {frequency.days!r}."

        days_since_start = (today - frequency.start_date).days
        days_since_last = days_since_start % frequency.days

        current = today - datetime.timedelta(days=days_since_last)
        if current < today:
            return current
        return current - datetime.timedelta(days=frequency.days)
    elif frequency.name == FrequencyType.Yearly:
        assert frequency.month is not None, f"The frequency was 'yearly' but [month] was {frequency.month!r}."
        assert frequency.month_day is not None, f"The frequency was 'yearly' but [month_day] was {frequency.month_day!r}."

        cy = datetime.date(today.year, month=frequency.month.value, day=frequency.month_day)
        if cy < today:
            return cy
        return datetime.date(today.year - 1, month=frequency.month.value, day=frequency.month_day)
    else:
        raise ValueError(f"Unrecognized frequency name, {frequency!r}")


@functools.lru_cache(maxsize=10000)
def should_display(
    *,
    frequency: Frequency,
    last_completed: datetime.date | None,
) -> bool:
    today = datetime.date.today()

    next_due_date = due_date(frequency=frequency)
    if next_due_date is None:
        return False
    else:
        start_date = next_due_date - datetime.timedelta(days=frequency.advance_display_days)
        end_date = next_due_date + datetime.timedelta(days=frequency.expire_display_days)

        if last_completed is None:
            return start_date <= today <= end_date
        if start_date <= last_completed <= end_date:
            return False
        return start_date <= today <= end_date


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


@functools.lru_cache(maxsize=10000)
def _monthly_prior(
    *,
    month: int,
    year: int,
    month_day: int,
) -> datetime.date:
    mo, yr = {
        1: (12, year-1),
        2: (1, year),
        3: (2, year),
        4: (3, year),
        5: (4, year),
        6: (5, year),
        7: (6, year),
        8: (7, year),
        9: (8, year),
        10: (9, year),
        11: (10, year),
        12: (11, year),
    }[month]
    return datetime.date(yr, mo, month_day)
