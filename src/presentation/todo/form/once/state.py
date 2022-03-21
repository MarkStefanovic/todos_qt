from __future__ import annotations

import dataclasses
import datetime

from src import domain

__all__ = ("OnceFrequencyFormState",)


@dataclasses.dataclass(frozen=True)
class OnceFrequencyFormState:
    due_date: datetime.date

    @staticmethod
    def initial() -> OnceFrequencyFormState:
        return OnceFrequencyFormState(due_date=datetime.date.today())

    @staticmethod
    def from_domain(*, frequency: domain.Frequency) -> OnceFrequencyFormState:
        assert frequency.due_date is not None, "[due_date] is required for a one-off todo."

        return OnceFrequencyFormState(due_date=frequency.due_date)

    def to_domain(self) -> domain.Frequency:
        return domain.Frequency.once(due_date=self.due_date)
