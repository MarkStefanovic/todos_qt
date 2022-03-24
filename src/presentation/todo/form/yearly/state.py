from __future__ import annotations

import dataclasses
import datetime

from src import domain

__all__ = ("YearlyFrequencyFormState",)


@dataclasses.dataclass(frozen=True)
class YearlyFrequencyFormState:
    month: domain.Month
    month_day: int
    advance_display_days: int
    expire_display_days: int
    start_date: datetime.date

    @staticmethod
    def from_domain(*, frequency: domain.Frequency) -> YearlyFrequencyFormState:
        assert frequency.month is not None, "[month] is required for a yearly todo."
        assert frequency.month_day is not None, "[month_day] is required for a yearly todo."

        return YearlyFrequencyFormState(
            month=frequency.month,
            month_day=frequency.month_day,
            advance_display_days=frequency.advance_display_days,
            expire_display_days=frequency.expire_display_days,
            start_date=frequency.start_date,
        )

    @staticmethod
    def initial() -> YearlyFrequencyFormState:
        return YearlyFrequencyFormState(
            month=domain.Month.January,
            month_day=1,
            advance_display_days=7,
            expire_display_days=90,
            start_date=datetime.date.today(),
        )

    def to_domain(self) -> domain.Frequency:
        return domain.Frequency.yearly(
            month=self.month,
            month_day=self.month_day,
            advance_display_days=self.advance_display_days,
            expire_display_days=self.expire_display_days,
            start_date=self.start_date,
        )
