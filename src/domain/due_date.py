import datetime
import functools

from src.domain.frequency import Frequency
from src.domain.frequency_type import FrequencyType
from src.domain.next_date import next_date
from src.domain.prior_date import prior_date

__all__ = ("due_date",)


@functools.lru_cache(10000)
def due_date(
    *,
    frequency: Frequency,
    today: datetime.date,
    last_completed: datetime.date | None,
) -> datetime.date:
    if frequency.name == FrequencyType.Once:
        assert frequency.due_date is not None, "Frequency was Once, but [due_date] was None."
        return frequency.due_date
    elif frequency.name == FrequencyType.Daily:
        return today
    else:
        prior_due_date = prior_date(frequency=frequency, today=today)
        assert prior_due_date is not None, f"If the frequency is not Once, then prior_due_date should not be None."
        # assert prior_due_date < today
        current_due_date = next_date(frequency=frequency, today=prior_due_date)
        assert current_due_date is not None, f"If the frequency is not Once, then current_due_date should not be None."
        next_due_date = next_date(frequency=frequency, today=current_due_date)
        assert next_due_date is not None, f"If the frequency is not Once, then next_due_date should not be None."
        # assert next_due_date > today
        return min(
            dt for dt in (prior_due_date, current_due_date, next_due_date)
            if today <= dt + datetime.timedelta(days=frequency.expire_display_days)
            and (last_completed is None or dt > last_completed)
        )
