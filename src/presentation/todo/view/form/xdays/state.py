from __future__ import annotations

import dataclasses
import datetime

from src import domain

__all__ = ("XDaysFrequencyFormState",)


@dataclasses.dataclass(frozen=True)
class XDaysFrequencyFormState:
    days: int

    @staticmethod
    def from_domain(*, frequency: domain.Frequency) -> XDaysFrequencyFormState:
        assert frequency.days is not None, "[days] is required for an xdays todo."

        return XDaysFrequencyFormState(days=frequency.days)

    @staticmethod
    def initial() -> XDaysFrequencyFormState:
        return XDaysFrequencyFormState(days=10)

    def to_domain(
        self,
        *,
        advance_display_days: int,
        expire_display_days: int,
        start_date: datetime.date,
    ) -> domain.Frequency:
        return domain.Frequency.xdays(
            days=self.days,
            advance_display_days=advance_display_days,
            expire_display_days=expire_display_days,
            start_date=start_date,
        )
