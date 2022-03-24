from __future__ import annotations

import dataclasses
import datetime

from src import domain

__all__ = ("WeeklyFrequencyFormState",)


@dataclasses.dataclass(frozen=True)
class WeeklyFrequencyFormState:
    week_day: domain.Weekday
    advance_display_days: int
    expire_display_days: int
    start_date: datetime.date

    @staticmethod
    def from_domain(*, frequency: domain.Frequency) -> WeeklyFrequencyFormState:
        assert frequency.week_day is not None, "[week_day] is required for an weekly todo."

        return WeeklyFrequencyFormState(
            week_day=frequency.week_day,
            advance_display_days=frequency.advance_display_days,
            expire_display_days=frequency.expire_display_days,
            start_date=frequency.start_date,
        )

    @staticmethod
    def initial() -> WeeklyFrequencyFormState:
        return WeeklyFrequencyFormState(
            week_day=domain.Weekday.Monday,
            advance_display_days=0,
            expire_display_days=6,
            start_date=datetime.date.today(),
        )

    def to_domain(self) -> domain.Frequency:
        return domain.Frequency.weekly(
            week_day=self.week_day,
            advance_display_days=self.advance_display_days,
            expire_display_days=self.expire_display_days,
            start_date=self.start_date,
        )
