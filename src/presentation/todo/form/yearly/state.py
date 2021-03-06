from __future__ import annotations

import dataclasses
import datetime

from src import domain

__all__ = ("YearlyFrequencyFormState",)


@dataclasses.dataclass(frozen=True)
class YearlyFrequencyFormState:
    month: domain.Month
    month_day: int

    @staticmethod
    def from_domain(*, frequency: domain.Frequency) -> YearlyFrequencyFormState:
        assert frequency.month is not None, "[month] is required for a yearly todo."
        assert frequency.month_day is not None, "[month_day] is required for a yearly todo."

        return YearlyFrequencyFormState(
            month=frequency.month,
            month_day=frequency.month_day,
        )

    @staticmethod
    def initial() -> YearlyFrequencyFormState:
        return YearlyFrequencyFormState(
            month=domain.Month.January,
            month_day=1,
        )

    def to_domain(
        self,
        *,
        advance_display_days: int,
        expire_display_days: int,
        start_date: datetime.date,
    ) -> domain.Frequency:
        return domain.Frequency.yearly(
            month=self.month,
            month_day=self.month_day,
            advance_display_days=advance_display_days,
            expire_display_days=expire_display_days,
            start_date=start_date,
        )
