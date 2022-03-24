from __future__ import annotations

import dataclasses
import datetime

from src import domain

__all__ = ("OnceFrequencyFormState",)


@dataclasses.dataclass(frozen=True)
class OnceFrequencyFormState:
    due_date: datetime.date
    advance_display_days: int
    expire_display_days: int
    start_date: datetime.date

    @staticmethod
    def initial() -> OnceFrequencyFormState:
        return OnceFrequencyFormState(
            due_date=datetime.date.today(),
            advance_display_days=0,
            expire_display_days=30,
            start_date=datetime.date.today(),
        )

    @staticmethod
    def from_domain(*, frequency: domain.Frequency) -> OnceFrequencyFormState:
        assert frequency.due_date is not None, "[due_date] is required for a one-off todo."

        return OnceFrequencyFormState(
            due_date=frequency.due_date,
            advance_display_days=frequency.advance_display_days,
            expire_display_days=frequency.expire_display_days,
            start_date=frequency.start_date,
        )

    def to_domain(self) -> domain.Frequency:
        return domain.Frequency.once(
            due_date=self.due_date,
            advance_display_days=self.advance_display_days,
            expire_display_days=self.expire_display_days,
            start_date=self.start_date,
        )
