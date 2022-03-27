from __future__ import annotations

import dataclasses
import datetime

from src import domain
from src.presentation.todo.form.irregular.state import IrregularFrequencyFormState
from src.presentation.todo.form.monthly.state import MonthlyFrequencyFormState
from src.presentation.todo.form.once.state import OnceFrequencyFormState
from src.presentation.todo.form.weekly.state import WeeklyFrequencyFormState
from src.presentation.todo.form.xdays.state import XDaysFrequencyFormState
from src.presentation.todo.form.yearly.state import YearlyFrequencyFormState

__all__ = ("TodoFormState",)


@dataclasses.dataclass(frozen=True)
class TodoFormState:
    todo_id: str
    advance_days: int
    expire_days: int
    category: domain.TodoCategory
    description: str
    frequency_name: domain.FrequencyType
    note: str
    start_date: datetime.date
    date_added: datetime.datetime
    date_updated: datetime.datetime | None
    date_deleted: datetime.datetime | None
    last_completed: datetime.date | None
    prior_completed: datetime.date | None
    irregular_frequency_form_state: IrregularFrequencyFormState
    monthly_frequency_form_state: MonthlyFrequencyFormState
    once_frequency_form_state: OnceFrequencyFormState
    weekly_frequency_form_state: WeeklyFrequencyFormState
    xdays_frequency_form_state: XDaysFrequencyFormState
    yearly_frequency_form_state: YearlyFrequencyFormState

    @staticmethod
    def initial() -> TodoFormState:
        return TodoFormState(
            todo_id=domain.create_uuid(),
            advance_days=0,
            expire_days=1,
            category=domain.TodoCategory.Todo,
            description="",
            frequency_name=domain.FrequencyType.Daily,
            note="",
            start_date=datetime.date.today(),
            date_added=datetime.datetime.now(),
            date_updated=None,
            date_deleted=None,
            last_completed=None,
            prior_completed=None,
            irregular_frequency_form_state=IrregularFrequencyFormState.initial(),
            monthly_frequency_form_state=MonthlyFrequencyFormState.initial(),
            once_frequency_form_state=OnceFrequencyFormState.initial(),
            weekly_frequency_form_state=WeeklyFrequencyFormState.initial(),
            xdays_frequency_form_state=XDaysFrequencyFormState.initial(),
            yearly_frequency_form_state=YearlyFrequencyFormState.initial(),
        )

    def to_domain(self) -> domain.Todo:
        if self.frequency_name == domain.FrequencyType.Daily:
            frequency: domain.Frequency = domain.Frequency.daily(start_date=self.start_date)
        elif self.frequency_name == domain.FrequencyType.Easter:
            frequency = domain.Frequency.easter(
                advance_display_days=self.advance_days,
                expire_display_days=self.expire_days,
                start_date=self.start_date,
            )
        elif self.frequency_name == domain.FrequencyType.Irregular:
            frequency = self.irregular_frequency_form_state.to_domain(
                advance_display_days=self.advance_days,
                expire_display_days=self.expire_days,
                start_date=self.start_date,
            )
        elif self.frequency_name == domain.FrequencyType.Monthly:
            frequency = self.monthly_frequency_form_state.to_domain(
                advance_display_days=self.advance_days,
                expire_display_days=self.expire_days,
                start_date=self.start_date,
            )
        elif self.frequency_name == domain.FrequencyType.Once:
            frequency = self.once_frequency_form_state.to_domain(
                advance_display_days=self.advance_days,
                expire_display_days=self.expire_days,
                start_date=self.start_date,
            )
        elif self.frequency_name == domain.FrequencyType.Weekly:
            frequency = self.weekly_frequency_form_state.to_domain(
                advance_display_days=self.advance_days,
                expire_display_days=self.expire_days,
                start_date=self.start_date,
            )
        elif self.frequency_name == domain.FrequencyType.XDays:
            frequency = self.xdays_frequency_form_state.to_domain(
                advance_display_days=self.advance_days,
                expire_display_days=self.expire_days,
                start_date=self.start_date,
            )
        elif self.frequency_name == domain.FrequencyType.Yearly:
            frequency = self.yearly_frequency_form_state.to_domain(
                advance_display_days=self.advance_days,
                expire_display_days=self.expire_days,
                start_date=self.start_date,
            )
        else:
            raise ValueError(f"Unrecognized [frequency_name], {self.frequency_name!r}.")

        return domain.Todo(
            todo_id=self.todo_id,
            frequency=frequency,
            category=self.category,
            description=self.description,
            note=self.note,
            date_added=self.date_added,
            date_updated=self.date_updated,
            date_deleted=self.date_deleted,
            last_completed=self.last_completed,
            prior_completed=self.prior_completed,
        )

    @staticmethod
    def from_domain(*, todo: domain.Todo) -> TodoFormState:
        irregular_frequency_form_state = IrregularFrequencyFormState.initial()
        monthly_frequency_form_state = MonthlyFrequencyFormState.initial()
        once_frequency_form_state = OnceFrequencyFormState.initial()
        weekly_frequency_form_state = WeeklyFrequencyFormState.initial()
        xdays_frequency_form_state = XDaysFrequencyFormState.initial()
        yearly_frequency_form_state = YearlyFrequencyFormState.initial()

        if todo.frequency.name == domain.FrequencyType.Irregular:
            irregular_frequency_form_state = IrregularFrequencyFormState.from_domain(frequency=todo.frequency)
        elif todo.frequency.name == domain.FrequencyType.Monthly:
            monthly_frequency_form_state = MonthlyFrequencyFormState.from_domain(frequency=todo.frequency)
        elif todo.frequency.name == domain.FrequencyType.Once:
            once_frequency_form_state = OnceFrequencyFormState.from_domain(frequency=todo.frequency)
        elif todo.frequency.name == domain.FrequencyType.Weekly:
            weekly_frequency_form_state = WeeklyFrequencyFormState.from_domain(frequency=todo.frequency)
        elif todo.frequency.name == domain.FrequencyType.XDays:
            xdays_frequency_form_state = XDaysFrequencyFormState.from_domain(frequency=todo.frequency)
        elif todo.frequency.name == domain.FrequencyType.Yearly:
            yearly_frequency_form_state = YearlyFrequencyFormState.from_domain(frequency=todo.frequency)

        return TodoFormState(
            todo_id=todo.todo_id,
            category=todo.category,
            description=todo.description,
            frequency_name=todo.frequency.name,
            note=todo.note,
            irregular_frequency_form_state=irregular_frequency_form_state,
            monthly_frequency_form_state=monthly_frequency_form_state,
            once_frequency_form_state=once_frequency_form_state,
            weekly_frequency_form_state=weekly_frequency_form_state,
            xdays_frequency_form_state=xdays_frequency_form_state,
            yearly_frequency_form_state=yearly_frequency_form_state,
            advance_days=todo.frequency.advance_display_days,
            expire_days=todo.frequency.expire_display_days,
            start_date=todo.frequency.start_date,
            date_added=todo.date_added,
            date_updated=todo.date_updated,
            date_deleted=todo.date_deleted,
            last_completed=todo.last_completed,
            prior_completed=todo.prior_completed,
        )
