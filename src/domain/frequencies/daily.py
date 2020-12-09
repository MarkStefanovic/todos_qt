from __future__ import annotations

import datetime

from src.domain import frequency_db_name, frequency

__all__ = ("Daily",)


class Daily(frequency.Frequency):
    def current_date(
        self, *, advance_days: int, today: datetime.date = datetime.date.today()
    ) -> datetime.date:
        return today

    @staticmethod
    def db_name() -> frequency_db_name.FrequencyDbName:
        return frequency_db_name.FrequencyDbName.DAILY

    def __repr__(self) -> str:
        return f"Daily()"

    def __str__(self) -> str:
        return "Daily"
