from __future__ import annotations

import dataclasses
import datetime

from src import domain

__all__ = ("IrregularFrequencyFormState",)


@dataclasses.dataclass(frozen=True)
class IrregularFrequencyFormState:
    month: domain.Month
    week_number: int
    week_day: domain.Weekday
    advance_display_days: int
    expire_display_days: int
    start_date: datetime.date

    @staticmethod
    def from_domain(*, frequency: domain.Frequency) -> IrregularFrequencyFormState:
        assert frequency.month is not None, "[month] is required for an irregular todo."
        assert frequency.week_number is not None, "[week_number] is required for an irregular todo."
        assert frequency.week_day is not None, "[week_day] is required for an irregular todo."

        return IrregularFrequencyFormState(
            month=frequency.month,
            week_number=frequency.week_number,
            week_day=frequency.week_day,
            advance_display_days=frequency.advance_display_days,
            expire_display_days=frequency.expire_display_days,
            start_date=frequency.start_date,
        )

    @staticmethod
    def initial() -> IrregularFrequencyFormState:
        return IrregularFrequencyFormState(
            month=domain.Month.January,
            week_number=1,
            week_day=domain.Weekday.Monday,
            advance_display_days=0,
            expire_display_days=30,
            start_date=datetime.date.today(),
        )

    def to_domain(self) -> domain.Frequency:
        return domain.Frequency.irregular(
            month=self.month,
            week_day=self.week_day,
            week_number=self.week_number,
            advance_display_days=self.advance_display_days,
            expire_display_days=self.expire_display_days,
            start_date=self.start_date,
        )
