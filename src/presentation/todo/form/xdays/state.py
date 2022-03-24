from __future__ import annotations

import dataclasses
import datetime

from src import domain

__all__ = ("XDaysFrequencyFormState",)


@dataclasses.dataclass(frozen=True)
class XDaysFrequencyFormState:
    days: int
    advance_display_days: int
    expire_display_days: int
    start_date: datetime.date

    @staticmethod
    def from_domain(*, frequency: domain.Frequency) -> XDaysFrequencyFormState:
        assert frequency.days is not None, "[days] is required for an xdays todo."

        return XDaysFrequencyFormState(
            days=frequency.days,
            advance_display_days=frequency.advance_display_days,
            expire_display_days=frequency.expire_display_days,
            start_date=frequency.start_date,
        )

    @staticmethod
    def initial() -> XDaysFrequencyFormState:
        return XDaysFrequencyFormState(
            days=10,
            advance_display_days=0,
            expire_display_days=9,
            start_date=datetime.date.today(),
        )

    def to_domain(self) -> domain.Frequency:
        return domain.Frequency.xdays(
            days=self.days,
            advance_display_days=self.advance_display_days,
            expire_display_days=self.expire_display_days,
            start_date=self.start_date,
        )
