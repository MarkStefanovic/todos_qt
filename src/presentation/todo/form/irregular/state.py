from __future__ import annotations

import dataclasses

from src import domain

__all__ = ("IrregularFrequencyFormState",)


@dataclasses.dataclass(frozen=True)
class IrregularFrequencyFormState:
    month: domain.Month
    week_number: int
    week_day: domain.Weekday

    @staticmethod
    def from_domain(*, frequency: domain.Frequency) -> IrregularFrequencyFormState:
        assert frequency.month is not None, "[month] is required for an irregular todo."
        assert frequency.week_number is not None, "[week_number] is required for an irregular todo."
        assert frequency.week_day is not None, "[week_day] is required for an irregular todo."

        return IrregularFrequencyFormState(
            month=frequency.month,
            week_number=frequency.week_number,
            week_day=frequency.week_day,
        )

    @staticmethod
    def initial() -> IrregularFrequencyFormState:
        return IrregularFrequencyFormState(
            month=domain.Month.January,
            week_number=1,
            week_day=domain.Weekday.Monday,
        )

    def to_domain(self) -> domain.Frequency:
        return domain.Frequency.irregular(
            month=self.month,
            week_day=self.week_day,
            week_number=self.week_number,
        )
