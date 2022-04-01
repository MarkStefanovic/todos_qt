import datetime

from src.domain.frequency import Frequency
from src.domain.frequency_type import FrequencyType
from src.domain.next_date import next_date
from src.domain.prior_date import prior_date

__all__ = ("due_date",)


def due_date(*, frequency: Frequency, today: datetime.date) -> datetime.date:
    if frequency.name == FrequencyType.Once:
        assert frequency.due_date is not None, "Frequency was Once, but [due_date] was None."
        return frequency.due_date

    prior_due_date = prior_date(frequency=frequency, today=today)
    current_due_date = next_date(frequency=frequency, today=prior_due_date)  # type: ignore
    next_due_date = next_date(frequency=frequency, today=today)
    return min(  # type: ignore
        dt for dt in (prior_due_date, current_due_date, next_due_date)
        if today <= dt + datetime.timedelta(days=frequency.expire_display_days)  # type: ignore
    )
