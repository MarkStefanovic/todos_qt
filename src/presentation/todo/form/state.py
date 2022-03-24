from __future__ import annotations

import datetime

import pydantic

from src import domain
from src.presentation.todo.form.irregular.state import IrregularFrequencyFormState
from src.presentation.todo.form.monthly.state import MonthlyFrequencyFormState
from src.presentation.todo.form.once.state import OnceFrequencyFormState
from src.presentation.todo.form.weekly.state import WeeklyFrequencyFormState
from src.presentation.todo.form.xdays.state import XDaysFrequencyFormState
from src.presentation.todo.form.yearly.state import YearlyFrequencyFormState

__all__ = ("TodoFormState",)


class TodoFormState(pydantic.BaseModel):
    advance_days: int
    expire_days: int
    category: domain.TodoCategory
    description: str
    frequency: domain.Frequency
    note: str
    start_date: datetime.date
    irregular_frequency_form_state: IrregularFrequencyFormState
    monthly_frequency_form_state: MonthlyFrequencyFormState
    once_frequency_form_state: OnceFrequencyFormState
    weekly_frequency_form_state: WeeklyFrequencyFormState
    xdays_frequency_form_state: XDaysFrequencyFormState
    yearly_frequency_form_state: YearlyFrequencyFormState

    @staticmethod
    def initial() -> TodoFormState:
        return TodoFormState(
            advance_days=0,
            expire_days=1,
            category=domain.TodoCategory.Todo,
            description="",
            frequency=domain.Frequency.daily(start_date=datetime.date.today()),
            note="",
            start_date=datetime.date.today(),
            irregular_frequency_form_state=IrregularFrequencyFormState.initial(),
            monthly_frequency_form_state=MonthlyFrequencyFormState.initial(),
            once_frequency_form_state=OnceFrequencyFormState.initial(),
            weekly_frequency_form_state=WeeklyFrequencyFormState.initial(),
            xdays_frequency_form_state=XDaysFrequencyFormState.initial(),
            yearly_frequency_form_state=YearlyFrequencyFormState.initial(),
        )

    def to_domain(
        self,
        *,
        todo_id: str,
        date_added: datetime.datetime,
        date_updated: datetime.datetime,
        date_deleted: datetime.datetime,
    ) -> domain.Todo:
        return domain.Todo(
            todo_id=todo_id,
            frequency=self.frequency,
            category=self.category,
            description=self.description,
            note=self.note,
            date_added=date_added,
            date_updated=date_updated,
            date_deleted=date_deleted,
        )

    @staticmethod
    def from_domain(*, todo: domain.Todo) -> TodoFormState:
        return TodoFormState(
            category=todo.category,
            description=todo.description,
            frequency=todo.frequency,
            note=todo.note,
            irregular_frequency_form_state=IrregularFrequencyFormState.from_domain(frequency=todo.frequency),
            monthly_frequency_form_state=MonthlyFrequencyFormState.from_domain(frequency=todo.frequency),
            once_frequency_form_state=OnceFrequencyFormState.from_domain(frequency=todo.frequency),
            weekly_frequency_form_state=WeeklyFrequencyFormState.from_domain(frequency=todo.frequency),
            xdays_frequency_form_state=XDaysFrequencyFormState.from_domain(frequency=todo.frequency),
            yearly_frequency_form_state=YearlyFrequencyFormState.from_domain(frequency=todo.frequency),
        )
