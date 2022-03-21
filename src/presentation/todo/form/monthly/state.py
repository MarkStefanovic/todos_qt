from __future__ import annotations

import dataclasses

from src import domain

__all__ = ("MonthlyFrequencyFormState",)


@dataclasses.dataclass(frozen=True)
class MonthlyFrequencyFormState:
    month_day: int

    @staticmethod
    def from_domain(*, frequency: domain.Frequency) -> MonthlyFrequencyFormState:
        assert frequency.month_day is not None, "[month_day] is required for a monthly todo."

        return MonthlyFrequencyFormState(month_day=frequency.month_day)

    @staticmethod
    def initial() -> MonthlyFrequencyFormState:
        return MonthlyFrequencyFormState(month_day=1)

    def to_domain(self) -> domain.Frequency:
        return domain.Frequency.monthly(month_day=self.month_day)
