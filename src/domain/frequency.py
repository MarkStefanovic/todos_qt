from __future__ import annotations

import abc
import datetime
import typing


__all__ = ("Frequency",)

from src.domain import frequency_db_name


class Frequency(abc.ABC):
    def display(
        self,
        advance_days: int,
        date_completed: typing.Optional[datetime.date],
        today: datetime.date = datetime.date.today(),
    ) -> bool:
        current_date = self.current_date(advance_days=advance_days, today=today)
        current_advance_date = current_date - datetime.timedelta(days=advance_days)
        if date_completed and date_completed >= current_advance_date:  # noqa
            return False
        elif today >= current_advance_date:
            return True
        else:
            return False

    @abc.abstractmethod
    def current_date(
        self, *, advance_days: int, today: datetime.date = datetime.date.today()
    ) -> datetime.date:
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def db_name() -> frequency_db_name.FrequencyDbName:
        raise NotImplementedError

    def __repr__(self) -> str:
        return self.__class__.__name__
