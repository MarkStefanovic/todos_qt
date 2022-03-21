from __future__ import annotations

import dataclasses

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

    def to_domain(self) -> domain.Frequency:
        return domain.Frequency.xdays(days=self.days)
