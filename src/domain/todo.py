from __future__ import annotations

import dataclasses
import datetime

import typing

import pydantic

from src.domain import (
    weekday,
    frequency_db_name,
    frequencies,
    month,
    frequency,
    todo_category,
)


__all__ = (
    "TodoDTO",
    "Todo",
    "DEFAULT_TODO",
)

TODAY = datetime.date.today()
FLOOR_DATE = datetime.date(1970, 1, 1)


class TodoDTO(pydantic.BaseModel):
    id: int
    advance_days: int
    date_added: datetime.date
    date_completed: typing.Optional[datetime.date]
    days: typing.Optional[int]
    description: str
    month: typing.Optional[int]
    month_day: typing.Optional[int]
    note: str
    start_date: typing.Optional[datetime.date]
    category: todo_category.TodoCategory
    week_day: typing.Optional[int]
    week_number: typing.Optional[int]
    year: typing.Optional[int]
    frequency: frequency_db_name.FrequencyDbName  # needs to come last for pydantic validators

    class Config:
        allow_mutation = False
        anystr_strip_whitespace = True
        validate_assignment = True

    @staticmethod
    def default() -> TodoDTO:
        return TodoDTO(
            advance_days=0,
            category=todo_category.TodoCategory("todo"),
            date_added=datetime.date(1970, 1, 1),
            date_completed=None,
            days=None,
            description="",
            frequency=frequency_db_name.FrequencyDbName.ONCE,
            id=-1,
            month=None,
            month_day=None,
            note="",
            start_date=datetime.date.today(),
            week_day=None,
            week_number=None,
            year=None,
        )

    def to_domain(self) -> Todo:
        if self.frequency == frequency_db_name.FrequencyDbName.DAILY:
            freq: frequency.Frequency = frequencies.Daily()
        elif self.frequency == frequency_db_name.FrequencyDbName.EASTER:
            freq = frequencies.Easter()
        elif self.frequency == frequency_db_name.FrequencyDbName.IRREGULAR:
            assert self.month is not None
            assert self.week_number is not None
            assert self.week_day is not None
            freq = frequencies.Irregular(
                month=month.Month(self.month),
                week_number=self.week_number,
                week_day=weekday.Weekday(self.week_day),
            )
        elif self.frequency == frequency_db_name.FrequencyDbName.MONTHLY:
            assert self.month_day is not None
            freq = frequencies.Monthly(self.month_day)
        elif self.frequency == frequency_db_name.FrequencyDbName.ONCE:
            assert self.start_date is not None
            freq = frequencies.Once(self.start_date)
        elif self.frequency == frequency_db_name.FrequencyDbName.WEEKLY:
            assert self.week_day is not None
            freq = frequencies.Weekly(weekday.Weekday(self.week_day))
        elif self.frequency == frequency_db_name.FrequencyDbName.XDAYS:
            assert self.days is not None
            assert self.start_date is not None
            freq = frequencies.XDays(
                days=self.days,
                start_date=self.start_date,
            )
        elif self.frequency == frequency_db_name.FrequencyDbName.YEARLY:
            assert self.month_day is not None
            assert self.month is not None
            freq = frequencies.Yearly(
                day=self.month_day,
                month=month.Month(self.month),
            )
        else:
            raise ValueError(f"Unrecognized frequency: {self.frequency!r}.")

        return Todo(
            todo_id=self.id,
            advance_days=self.advance_days,
            date_added=self.date_added,
            date_completed=self.date_completed,
            description=self.description,
            frequency=freq,
            note=self.note,
            start_date=self.start_date,
            category=self.category,
        )

    @pydantic.validator("frequency")
    def required_fields_for_frequency_are_supplied(
        cls,
        v: frequency_db_name.FrequencyDbName,
        values: typing.Dict[str, typing.Any],
        **kwargs: typing.Dict[str, typing.Any],
    ) -> frequency_db_name.FrequencyDbName:
        if v in (
            frequency_db_name.FrequencyDbName.DAILY,
            frequency_db_name.FrequencyDbName.EASTER,
        ):
            return v
        elif v == frequency_db_name.FrequencyDbName.IRREGULAR:
            if (mo := values["month"]) is None or mo < 1 or mo > 12:
                raise ValueError(
                    f"If the frequency 'irregular', then the month must be between 1 and 12, but got {mo}."
                )
            elif (wk := values["week_number"]) is None or wk < 1 or wk > 5:
                raise ValueError(
                    f"If the frequency 'irregular', then the week_number must be between 1 and 5, but got {wk}."
                )
            elif (wk_day := values["week_day"]) is None or wk < 1 or wk > 7:
                raise ValueError(
                    f"If the frequency 'irregular', then the week_day must be between 1 and 7, but got {wk_day}."
                )
            else:
                return v
        elif v == frequency_db_name.FrequencyDbName.MONTHLY:
            if (
                (month_day := values["month_day"]) is None
                or month_day < 1
                or month_day > 29
            ):
                raise ValueError(
                    f"If the frequency 'irregular', then the month_day must be between 1 and 29, but got {month_day}."
                )
            else:
                return v
        elif v == frequency_db_name.FrequencyDbName.ONCE:
            if values["start_date"] is None:
                raise ValueError(
                    f"If the frequency is 'once', then a start_date must be provided."
                )
            else:
                return v
        else:
            return v


@dataclasses.dataclass(frozen=True)
class Todo:
    advance_days: int
    category: todo_category.TodoCategory
    date_added: datetime.date
    date_completed: typing.Optional[datetime.date]
    description: str
    frequency: frequency.Frequency
    todo_id: int
    note: str
    start_date: typing.Optional[datetime.date]

    def display(self, /, today: datetime.date = datetime.date.today()) -> bool:
        return self.frequency.display(
            advance_days=self.advance_days,
            date_completed=self.date_completed,
            today=today,
        )

    def current_date(
        self, /, today: datetime.date = datetime.date.today()
    ) -> datetime.date:
        return self.frequency.current_date(advance_days=self.advance_days, today=today)

    def days_until(self, /, today: datetime.date = datetime.date.today()) -> int:
        return (self.current_date(today) - today).days

    def to_dto(self) -> TodoDTO:
        if isinstance(self.frequency, frequencies.Daily):
            days: typing.Optional[int] = None
            month: typing.Optional[int] = None
            month_day: typing.Optional[int] = None
            week_day: typing.Optional[int] = None
            week_number: typing.Optional[int] = None
            year: typing.Optional[int] = None
        elif isinstance(self.frequency, frequencies.Easter):
            days = None
            month = None
            month_day = None
            week_day = None
            week_number = None
            year = None
        elif isinstance(self.frequency, frequencies.Irregular):
            days = None
            month = self.frequency.month
            month_day = None
            week_day = self.frequency.week_day.value
            week_number = self.frequency.week_number
            year = None
        elif isinstance(self.frequency, frequencies.Monthly):
            days = None
            month = None
            month_day = self.frequency.month_day
            week_day = None
            week_number = None
            year = None
        elif isinstance(self.frequency, frequencies.Once):
            days = None
            month = None
            month_day = None
            week_day = None
            week_number = None
            year = None
        elif isinstance(self.frequency, frequencies.Weekly):
            days = None
            month = None
            month_day = None
            week_day = self.frequency.week_day
            week_number = None
            year = None
        elif isinstance(self.frequency, frequencies.XDays):
            days = self.frequency.days
            month = None
            month_day = None
            week_day = None
            week_number = None
            year = None
        elif isinstance(self.frequency, frequencies.Yearly):
            days = None
            month = self.frequency.month
            month_day = self.frequency.day
            week_day = None
            week_number = None
            year = None
        else:
            raise ValueError(f"Unrecognized frequency: {self.frequency!r}.")

        return TodoDTO(
            id=self.todo_id,
            description=self.description,
            frequency=self.frequency.db_name(),
            year=year,
            month=month,
            month_day=month_day,
            week_day=week_day,
            week_number=week_number,
            date_added=self.date_added,
            date_completed=self.date_completed,
            advance_days=self.advance_days,
            start_date=self.start_date,
            days=days,
            note=self.note,
            category=self.category.value,
        )

    # def __str__(self) -> str:
    #     return (
    #         f"{self.todo_id}: {self.description}\n\tnote: {self.note}\n\tcurrent_date: {self.current_date()}\n\t"
    #         f"date_completed: {self.date_completed}\n\tadvance_days: {self.advance_days}\n\t"
    #         f"frequency: {self.frequency!s}\n\tdays_until: {self.days_until()}"
    #     )


DEFAULT_TODO = TodoDTO(
    id=-1,
    description="",
    frequency=frequency_db_name.FrequencyDbName.ONCE,
    year=TODAY.year,
    month=TODAY.month,
    month_day=TODAY.day,
    week_day=1,
    week_number=1,
    date_added=TODAY,
    date_completed=FLOOR_DATE,
    advance_days=0,
    start_date=TODAY,
    days=1,
    note="",
    category=todo_category.TodoCategory.Todo,
)
