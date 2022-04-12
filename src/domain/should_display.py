import datetime
import functools

from src.domain.frequency import Frequency
from src.domain.next_date import next_date
from src.domain.prior_date import prior_date

__all__ = ("should_display",)


@functools.lru_cache(maxsize=10000)
def should_display(
    *,
    frequency: Frequency,
    today: datetime.date,
    last_completed: datetime.date | None,
) -> bool:
    due_dates: list[datetime.date] = []
    prior_due_date = prior_date(frequency=frequency, today=today)
    if prior_due_date:
        due_dates.append(prior_due_date)
        current_due_date = next_date(frequency=frequency, today=prior_due_date)
        if current_due_date:
            due_dates.append(current_due_date)
            next_due_date = next_date(frequency=frequency, today=current_due_date)
            if next_due_date:
                due_dates.append(next_due_date)

    display_windows: list[tuple[datetime.date, datetime.date]] = []
    for dt in due_dates:
        if dt >= frequency.start_date:
            display_windows.append(
                (
                    dt - datetime.timedelta(days=frequency.advance_display_days),
                    dt + datetime.timedelta(days=frequency.expire_display_days),
                )
            )

    applicable_display_windows = [w for w in display_windows if w[0] <= today <= w[1]]
    if applicable_display_windows:
        if last_completed is None:
            return True

    for (start_display, _) in applicable_display_windows:
        if last_completed is None:
            return True
        elif last_completed < start_display:
            return True

    return False
