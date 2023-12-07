from __future__ import annotations

import dataclasses
import datetime

from src import domain
from src.presentation.todo.view.form.irregular import IrregularFrequencyFormState
from src.presentation.todo.view.form.monthly.state import MonthlyFrequencyFormState
from src.presentation.todo.view.form.once import OnceFrequencyFormState
from src.presentation.todo.form.weekly.state import WeeklyFrequencyFormState
from src.presentation.todo.view.form.xdays.state import XDaysFrequencyFormState
from src.presentation.todo.view.form.yearly.state import YearlyFrequencyFormState

__all__ = ("TodoFormState",)


@dataclasses.dataclass(frozen=True)
class TodoFormState:
    todo_id: str
    template_todo_id: str | None
    advance_days: int
    expire_days: int
    user: domain.User
    category: domain.Category
    description: str
    frequency_name: domain.FrequencyType
    note: str
    start_date: datetime.date
    date_added: datetime.datetime
    date_updated: datetime.datetime | None
    last_completed: datetime.date | None
    prior_completed: datetime.date | None
    last_completed_by: domain.User | None
    prior_completed_by: domain.User | None
    irregular_frequency_form_state: IrregularFrequencyFormState
    monthly_frequency_form_state: MonthlyFrequencyFormState
    once_frequency_form_state: OnceFrequencyFormState
    weekly_frequency_form_state: WeeklyFrequencyFormState
    xdays_frequency_form_state: XDaysFrequencyFormState
    yearly_frequency_form_state: YearlyFrequencyFormState
    category_options: list[domain.Category]
    user_options: list[domain.User]
    focus_description: bool

    @staticmethod
    def initial(
        *,
        category_options: list[domain.Category],
        user_options: list[domain.User],
        current_user: domain.User | None,
    ) -> TodoFormState:
        return TodoFormState(
            todo_id=domain.create_uuid(),
            template_todo_id=None,
            advance_days=0,
            expire_days=99,
            user=current_user or domain.DEFAULT_USER,
            category=domain.TODO_CATEGORY,
            description="",
            frequency_name=domain.FrequencyType.Once,
            note="",
            start_date=datetime.date.today(),
            date_added=datetime.datetime.now(),
            date_updated=None,
            last_completed=None,
            prior_completed=None,
            last_completed_by=None,
            prior_completed_by=None,
            irregular_frequency_form_state=IrregularFrequencyFormState.initial(),
            monthly_frequency_form_state=MonthlyFrequencyFormState.initial(),
            once_frequency_form_state=OnceFrequencyFormState.initial(),
            weekly_frequency_form_state=WeeklyFrequencyFormState.initial(),
            xdays_frequency_form_state=XDaysFrequencyFormState.initial(),
            yearly_frequency_form_state=YearlyFrequencyFormState.initial(),
            category_options=category_options,
            user_options=user_options,
            focus_description=True,
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
            template_todo_id=self.template_todo_id,
            frequency=frequency,
            user=self.user,
            category=self.category,
            description=self.description,
            note=self.note,
            date_added=self.date_added,
            date_updated=self.date_updated,
            last_completed=self.last_completed,
            prior_completed=self.prior_completed,
            last_completed_by=self.last_completed_by,
            prior_completed_by=self.prior_completed_by,
        )

    @staticmethod
    def from_domain(
        *,
        todo: domain.Todo,
        category_options: list[domain.Category],
        user_options: list[domain.User],
    ) -> TodoFormState:
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
            template_todo_id=todo.template_todo_id,
            user=todo.user,
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
            last_completed=todo.last_completed,
            prior_completed=todo.prior_completed,
            last_completed_by=todo.last_completed_by,
            prior_completed_by=todo.prior_completed_by,
            category_options=category_options,
            user_options=user_options,
            focus_description=True,
        )

    def __eq__(self, other: object) -> bool:
        assert isinstance(other, TodoFormState)

        mod_self = dataclasses.replace(self, note=_standardize_str(self.note))
        mod_other = dataclasses.replace(other, note=_standardize_str(other.note))

        return dataclasses.astuple(mod_self) == dataclasses.astuple(mod_other)


def _standardize_str(s: str) -> str:
    return s.replace("\xa0", " ").replace("\r", "\n").strip("\xef\xbb\xbf ")
