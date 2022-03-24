from __future__ import annotations

import dataclasses
import datetime

from src import domain

__all__ = ("MonthlyFrequencyFormState",)


@dataclasses.dataclass(frozen=True)
class MonthlyFrequencyFormState:
    month_day: int
    advance_display_days: int
    expire_display_days: int
    start_date: datetime.date

    @staticmethod
    def from_domain(*, frequency: domain.Frequency) -> MonthlyFrequencyFormState:
        assert frequency.month_day is not None, "[month_day] is required for a monthly todo."

        return MonthlyFrequencyFormState(
            month_day=frequency.month_day,
            advance_display_days=frequency.advance_display_days,
            expire_display_days=frequency.expire_display_days,
            start_date=frequency.start_date,
        )

    @staticmethod
    def initial() -> MonthlyFrequencyFormState:
        return MonthlyFrequencyFormState(
            month_day=1,
            advance_display_days=0,
            expire_display_days=14,
            start_date=datetime.date.today(),
        )

    def to_domain(self) -> domain.Frequency:
        return domain.Frequency.monthly(
            month_day=self.month_day,
            advance_display_days=self.advance_display_days,
            expire_display_days=self.expire_display_days,
            start_date=self.start_date,
        )
