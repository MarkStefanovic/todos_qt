from __future__ import annotations

import dataclasses
import datetime

from src import domain

__all__ = ("MonthlyFrequencyFormState",)


@dataclasses.dataclass(frozen=True)
class MonthlyFrequencyFormState:
    month_day: int

    @staticmethod
    def from_domain(*, frequency: domain.Frequency) -> MonthlyFrequencyFormState:
        assert frequency.month_day is not None, "[month_day] is required for a monthly todo."

        return MonthlyFrequencyFormState(month_day=frequency.month_day)

    @staticmethod
    def initial() -> MonthlyFrequencyFormState:
        return MonthlyFrequencyFormState(month_day=1)

    def to_domain(
        self,
        *,
        advance_display_days: int,
        expire_display_days: int,
        start_date: datetime.date,
    ) -> domain.Frequency:
        return domain.Frequency.monthly(
            month_day=self.month_day,
            advance_display_days=advance_display_days,
            expire_display_days=expire_display_days,
            start_date=start_date,
        )
