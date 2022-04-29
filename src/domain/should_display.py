from __future__ import annotations

import datetime
import functools

from src.domain.due_date import due_date
from src.domain.frequency import Frequency

__all__ = ("should_display",)


@functools.lru_cache(maxsize=10000)
def should_display(
    *,
    frequency: Frequency,
    today: datetime.date,
    last_completed: datetime.date | None,
) -> bool:
    next_due_date = due_date(frequency=frequency, today=today)
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
