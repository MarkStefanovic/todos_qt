import calendar
import datetime
import functools
import itertools

from src.domain.frequency import Frequency
from src.domain.month import Month
from src.domain.weekday import Weekday

__all__ = ("should_display",)


def should_display(
    *,
    frequency: Frequency,
    advance_days: int,
    expire_days: int,
    start_date: datetime.date,
    last_completed: datetime.date | None,
    today: datetime.date,
) -> bool:
    if frequency.name == "daily":
        return last_completed is None or last_completed < today
    elif frequency.name == "easter":
        return _easter_should_display(
            today=today,
            advance_days=advance_days,
            expire_days=expire_days,
            start_date=start_date,
            last_completed=last_completed,
        )
    elif frequency.name == "irregular":
        assert frequency.month is not None, f"The frequency was 'irregular', but [month] was {frequency.month!r}."
        assert frequency.week_day is not None, f"The frequency was 'irregular', but [week_day] was {frequency.week_day!r}."

        return _irregular_should_display(
            month=frequency.month,
            week_number=frequency.week_number,
            week_day=frequency.week_day,
            today=today,
            advance_days=advance_days,
            expire_days=expire_days,
            start_date=start_date,
            last_completed=last_completed,
        )
    elif frequency.name == "monthly":
        assert frequency.month_day is not None, f"The frequency was 'monthly' but [month_day] was {frequency.month_day!r}."

        return _monthly_should_display(
            month_day=frequency.month_day,
            today=today,
            advance_days=advance_days,
            expire_days=expire_days,
            start_date=start_date,
            last_completed=last_completed,
        )
    elif frequency.name == "once":
        assert frequency.due_date is not None, f"The frequency was 'once' but [due_date] was {frequency.due_date!r}."

        return _one_off_should_display(
            due_date=frequency.due_date,
            today=today,
            advance_days=advance_days,
            expire_days=expire_days,
            last_completed=last_completed,
        )
    elif frequency.name == "weekly":
        assert frequency.due_date is not None, f"The frequency was 'weekly' but [week_day] was {frequency.week_day!r}."

        return _weekly_should_display(
            week_day=frequency.week_day,
            today=today,
            advance_days=advance_days,
            expire_days=expire_days,
            start_date=start_date,
            last_completed=last_completed,
        )
    elif frequency.name == "xdays":
        assert frequency.days is not None, f"The frequency was 'xdays' but [days] was {frequency.days!r}."

        return _x_days_should_display(
            days=frequency.days,
            today=today,
            advance_days=advance_days,
            expire_days=expire_days,
            start_date=start_date,
            last_completed=last_completed,
        )
    elif frequency.name == "yearly":
        assert frequency.due_date is not None, f"The frequency was 'yearly' but [month] was {frequency.month!r}."
        assert frequency.due_date is not None, f"The frequency was 'yearly' but [month_day] was {frequency.month_day!r}."

        return _yearly_should_display(
            month=frequency.month,
            day=frequency.month_day,
            today=today,
            advance_days=advance_days,
            expire_days=expire_days,
            start_date=start_date,
            last_completed=last_completed,
        )
    else:
        raise ValueError(f"Unrecognized frequency name, {frequency!r}")


def _should_display(
    *,
    start_date: datetime.date,
    today: datetime.date,
    last_completed: datetime.date | None,
    next_date: datetime.date,
    next_start_display: datetime.date,
    next_end_display: datetime.date,
    current_date: datetime.date,
    current_start_display: datetime.date,
    current_end_display: datetime.date,
    prior_date: datetime.date,
    prior_start_display: datetime.date,
    prior_end_display: datetime.date,
) -> bool:
    if next_start_display <= today <= next_end_display:
        if last_completed is None:
            return start_date >= next_date
        elif last_completed >= next_start_display:
            return False
        else:
            return start_date >= next_date
    elif current_start_display <= today <= current_end_display:
        if last_completed is None:
            return start_date >= current_date
        elif last_completed >= current_start_display:
            return False
        else:
            return start_date >= current_date
    elif prior_start_display <= today <= prior_end_display:
        if last_completed is None:
            return start_date >= prior_date
        elif last_completed >= prior_start_display:
            return False
        else:
            return start_date >= prior_date
    else:
        return False


def _easter_should_display(
    *,
    advance_days: int,
    expire_days: int,
    last_completed: datetime.date | None,
    start_date: datetime.date,
    today: datetime.date,
) -> bool:
    ny = _calculate_easter(today.year + 1)
    cy = _calculate_easter(today.year)
    py = _calculate_easter(today.year)

    return _should_display(
        today=today,
        last_completed=last_completed,
        start_date=start_date,
        next_date=ny,
        next_start_display=ny - datetime.timedelta(days=advance_days),
        next_end_display=ny + datetime.timedelta(days=expire_days),
        current_date=cy,
        current_start_display=cy - datetime.timedelta(days=advance_days),
        current_end_display=cy + datetime.timedelta(days=expire_days),
        prior_date=py,
        prior_start_display=py - datetime.timedelta(days=advance_days),
        prior_end_display=py + datetime.timedelta(days=expire_days),
    )


@functools.lru_cache()
def _calculate_easter(year: int, /) -> datetime.date:
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = ((19 * a) + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + (2 * e) + (2 * i) - h - k) % 7
    m = (a + (11 * h) + (22 * l)) // 451
    month = (h + l - (7 * m) + 114) // 31
    day = ((h + l - (7 * m) + 114) % 31) + 1
    return datetime.date(year, month, day)


def _irregular_should_display(
    *,
    month: Month,
    week_number: int,
    week_day: Weekday,
    start_date: datetime.date,
    advance_days: int,
    expire_days: int,
    last_completed: datetime.date | None,
    today: datetime.date,
) -> bool:
    prior_date = _get_x_weekday_of_month(
        year=today.year - 1,
        month=month.to_int(),
        week_num=week_number,
        week_day=week_day,
    )

    current_date = _get_x_weekday_of_month(
        year=today.year,
        month=month.to_int(),
        week_num=week_number,
        week_day=week_day,
    )

    next_date = _get_x_weekday_of_month(
        year=today.year + 1,
        month=month.to_int(),
        week_num=week_number,
        week_day=week_day,
    )

    return _should_display(
        today=today,
        start_date=start_date,
        last_completed=last_completed,
        next_date=next_date,
        next_start_display=next_date - datetime.timedelta(days=advance_days),
        next_end_display=next_date + datetime.timedelta(days=expire_days),
        current_date=current_date,
        current_start_display=current_date - datetime.timedelta(days=advance_days),
        current_end_display=current_date + datetime.timedelta(days=expire_days),
        prior_date=prior_date,
        prior_start_display=prior_date - datetime.timedelta(days=advance_days),
        prior_end_display=prior_date + datetime.timedelta(days=expire_days),
    )


@functools.lru_cache()
def _get_x_weekday_of_month(
    *, year: int, month: int, week_num: int, week_day: Weekday
) -> datetime.date:
    days_in_month = calendar.monthrange(year, month)[1]
    return list(
        itertools.islice(
            (
                dt
                for day in range(1, days_in_month, 1)
                if (dt := datetime.date(year, month, day)).weekday() == week_day.value
            ),
            week_num,
        )
    )[-1]


def _monthly_should_display(
    *,
    month_day: int,
    start_date: datetime.date,
    advance_days: int,
    expire_days: int,
    last_completed: datetime.date | None,
    today: datetime.date,
) -> bool:
    prior_month, prior_month_year = {
        1: (12, today.year - 1),
        2: (1, today.year),
        3: (2, today.year),
        4: (3, today.year),
        5: (4, today.year),
        6: (5, today.year),
        7: (6, today.year),
        8: (7, today.year),
        9: (8, today.year),
        10: (9, today.year),
        11: (10, today.year),
        12: (11, today.year),
    }[today.month]
    prior_month_date = datetime.date(prior_month_year, prior_month, month_day)

    current_month_date = datetime.date(year=today.year, month=today.month, day=month_day)

    next_month, next_month_year = {
        1: (2, today.year),
        2: (3, today.year),
        3: (4, today.year),
        4: (5, today.year),
        5: (6, today.year),
        6: (7, today.year),
        7: (8, today.year),
        8: (9, today.year),
        9: (10, today.year),
        10: (11, today.year),
        11: (12, today.year),
        12: (1, today.year + 1),
    }[today.month]
    next_month_date = datetime.date(year=next_month_year, month=next_month, day=month_day)

    return _should_display(
        today=today,
        start_date=start_date,
        last_completed=last_completed,
        next_date=next_month_date,
        next_start_display=next_month_date - datetime.timedelta(days=advance_days),
        next_end_display=next_month_date + datetime.timedelta(days=expire_days),
        current_date=current_month_date,
        current_start_display=current_month_date - datetime.timedelta(days=advance_days),
        current_end_display=current_month_date + datetime.timedelta(days=expire_days),
        prior_date=prior_month_date,
        prior_start_display=prior_month_date - datetime.timedelta(days=advance_days),
        prior_end_display=prior_month_date + datetime.timedelta(days=expire_days),
    )


def _one_off_should_display(
    *,
    due_date: datetime.date,
    advance_days: int,
    expire_days: int,
    last_completed: datetime.date | None,
    today: datetime.date,
) -> bool:

    if last_completed:
        return False
    else:
        start_display = due_date - datetime.timedelta(days=advance_days)
        end_display = due_date + datetime.timedelta(days=expire_days)
        return start_display <= today <= end_display


def _weekly_should_display(
    *,
    week_day: Weekday,
    start_date: datetime.date,
    advance_days: int,
    expire_days: int,
    last_completed: datetime.date | None,
    today: datetime.date,
) -> bool:
    weekday_diff = Weekday.from_date(today).value - week_day.value
    if weekday_diff == 0:
        next_date = today + datetime.timedelta(days=7)
    elif weekday_diff < 0:
        next_date = today - datetime.timedelta(days=weekday_diff)
    else:
        next_date = today + datetime.timedelta(days=7 - weekday_diff)

    prior_date = next_date - datetime.timedelta(days=14)
    current_date = next_date - datetime.timedelta(days=7)

    return _should_display(
        today=today,
        start_date=start_date,
        last_completed=last_completed,
        next_date=next_date,
        next_start_display=next_date - datetime.timedelta(days=advance_days),
        next_end_display=next_date + datetime.timedelta(days=expire_days),
        current_date=current_date,
        current_start_display=current_date - datetime.timedelta(days=advance_days),
        current_end_display=current_date + datetime.timedelta(days=expire_days),
        prior_date=prior_date,
        prior_start_display=prior_date - datetime.timedelta(days=advance_days),
        prior_end_display=prior_date + datetime.timedelta(days=expire_days),
    )


def _x_days_should_display(
    *,
    days: int,
    start_date: datetime.date,
    advance_days: int,
    expire_days: int,
    last_completed: datetime.date | None,
    today: datetime.date,
) -> bool:
    days_since_start = (today - start_date).days
    days_since_last = days_since_start % days

    prior_date = today - datetime.timedelta(days=days_since_last)
    current_date = prior_date + datetime.timedelta(days=days)
    next_date = current_date + datetime.timedelta(days=days)

    return _should_display(
        today=today,
        start_date=start_date,
        last_completed=last_completed,
        next_date=next_date,
        next_start_display=next_date - datetime.timedelta(days=advance_days),
        next_end_display=next_date + datetime.timedelta(days=expire_days),
        current_date=current_date,
        current_start_display=current_date - datetime.timedelta(days=advance_days),
        current_end_display=current_date + datetime.timedelta(days=expire_days),
        prior_date=prior_date,
        prior_start_display=prior_date - datetime.timedelta(days=advance_days),
        prior_end_display=prior_date + datetime.timedelta(days=expire_days),
    )


def _yearly_should_display(
    *,
    month: Month,
    day: int,
    start_date: datetime.date,
    advance_days: int,
    expire_days: int,
    last_completed: datetime.date | None,
    today: datetime.date,
) -> bool:
    yr = today.year

    ny = datetime.date(yr + 1, month.value, day)
    cy = datetime.date(yr, month.value, day)
    py = datetime.date(yr - 1, month.value, day)

    return _should_display(
        today=today,
        start_date=start_date,
        last_completed=last_completed,
        next_date=ny,
        next_start_display=ny - datetime.timedelta(days=advance_days),
        next_end_display=ny + datetime.timedelta(days=expire_days),
        current_date=cy,
        current_start_display=cy - datetime.timedelta(days=advance_days),
        current_end_display=cy + datetime.timedelta(days=expire_days),
        prior_date=py,
        prior_start_display=py - datetime.timedelta(days=advance_days),
        prior_end_display=py + datetime.timedelta(days=expire_days),
    )
