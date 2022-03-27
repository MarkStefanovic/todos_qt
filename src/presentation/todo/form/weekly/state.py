from __future__ import annotations

import dataclasses
import datetime

from src import domain

__all__ = ("WeeklyFrequencyFormState",)


@dataclasses.dataclass(frozen=True)
class WeeklyFrequencyFormState:
    week_day: domain.Weekday

    @staticmethod
    def from_domain(*, frequency: domain.Frequency) -> WeeklyFrequencyFormState:
        assert frequency.week_day is not None, "[week_day] is required for an weekly todo."

        return WeeklyFrequencyFormState(week_day=frequency.week_day)

    @staticmethod
    def initial() -> WeeklyFrequencyFormState:
        return WeeklyFrequencyFormState(week_day=domain.Weekday.Monday)

    def to_domain(
        self,
        *,
        advance_display_days: int,
        expire_display_days: int,
        start_date: datetime.date,
    ) -> domain.Frequency:
        return domain.Frequency.weekly(
            week_day=self.week_day,
            advance_display_days=advance_display_days,
            expire_display_days=expire_display_days,
            start_date=start_date,
        )
