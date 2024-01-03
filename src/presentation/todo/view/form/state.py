from __future__ import annotations

import dataclasses
import datetime

from src import domain
from src.presentation.todo.view.form.irregular.state import IrregularFrequencyFormState
from src.presentation.todo.view.form.monthly.state import MonthlyFrequencyFormState
from src.presentation.todo.view.form.once.state import OnceFrequencyFormState
from src.presentation.todo.view.form.weekly.state import WeeklyFrequencyFormState
from src.presentation.todo.view.form.xdays.state import XDaysFrequencyFormState
from src.presentation.todo.view.form.yearly.state import YearlyFrequencyFormState

__all__ = ("TodoFormState",)


@dataclasses.dataclass(frozen=True)
class TodoFormState:
    todo_id: str | domain.Unspecified = domain.Unspecified()
    template_todo_id: str | None | domain.Unspecified = domain.Unspecified()
    advance_days: int | domain.Unspecified = domain.Unspecified()
    expire_days: int | domain.Unspecified = domain.Unspecified()
    user: domain.User | domain.Unspecified = domain.Unspecified()
    category: domain.Category | domain.Unspecified = domain.Unspecified()
    description: str | domain.Unspecified = domain.Unspecified()
    frequency_name: domain.FrequencyType | domain.Unspecified = domain.Unspecified()
    note: str | domain.Unspecified = domain.Unspecified()
    start_date: datetime.date | domain.Unspecified = domain.Unspecified()
    date_added: datetime.datetime | domain.Unspecified = domain.Unspecified()
    date_updated: datetime.datetime | None | domain.Unspecified = domain.Unspecified()
    last_completed: datetime.date | None | domain.Unspecified = domain.Unspecified()
    prior_completed: datetime.date | None | domain.Unspecified = domain.Unspecified()
    last_completed_by: domain.User | None | domain.Unspecified = domain.Unspecified()
    prior_completed_by: domain.User | None | domain.Unspecified = domain.Unspecified()
    irregular_frequency_form_state: IrregularFrequencyFormState | domain.Unspecified = domain.Unspecified()
    monthly_frequency_form_state: MonthlyFrequencyFormState | domain.Unspecified = domain.Unspecified()
    once_frequency_form_state: OnceFrequencyFormState | domain.Unspecified = domain.Unspecified()
    weekly_frequency_form_state: WeeklyFrequencyFormState | domain.Unspecified = domain.Unspecified()
    xdays_frequency_form_state: XDaysFrequencyFormState | domain.Unspecified = domain.Unspecified()
    yearly_frequency_form_state: YearlyFrequencyFormState | domain.Unspecified = domain.Unspecified()
    focus_description: bool | domain.Unspecified = domain.Unspecified()

    @staticmethod
    def initial(*, current_user: domain.User | None) -> TodoFormState:
        return TodoFormState(
            todo_id=domain.create_uuid(),
            template_todo_id=None,
            advance_days=0,
            expire_days=999,
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
            focus_description=True,
        )

    def to_domain(self) -> domain.Todo | domain.Error:
        try:
            if isinstance(self.todo_id, domain.Unspecified):
                return domain.Error.new("todo_id is unspecified.")

            if isinstance(self.template_todo_id, domain.Unspecified):
                return domain.Error.new("template_todo_id is unspecified.")

            if isinstance(self.user, domain.Unspecified):
                return domain.Error.new("user is unspecified.")

            if isinstance(self.category, domain.Unspecified):
                return domain.Error.new("category is unspecified.")

            if isinstance(self.description, domain.Unspecified):
                return domain.Error.new("description is unspecified.")

            if isinstance(self.note, domain.Unspecified):
                return domain.Error.new("note is unspecified.")

            if isinstance(self.date_added, domain.Unspecified):
                return domain.Error.new("date_added is unspecified.")

            if isinstance(self.date_updated, domain.Unspecified):
                return domain.Error.new("date_updated is unspecified.")

            if isinstance(self.last_completed, domain.Unspecified):
                return domain.Error.new("last_completed is unspecified.")

            if isinstance(self.prior_completed, domain.Unspecified):
                return domain.Error.new("prior_completed is unspecified.")

            if isinstance(self.last_completed_by, domain.Unspecified):
                return domain.Error.new("last_completed_by is unspecified.")

            if isinstance(self.prior_completed_by, domain.Unspecified):
                return domain.Error.new("prior_completed_by is unspecified.")

            if isinstance(self.advance_days, domain.Unspecified):
                return domain.Error.new("advance_days is unspecified.")

            if isinstance(self.expire_days, domain.Unspecified):
                return domain.Error.new("expire_days is unspecified.")

            if isinstance(self.start_date, domain.Unspecified):
                return domain.Error.new("start_date is unspecified.")

            if isinstance(self.frequency_name, domain.Unspecified):
                return domain.Error.new("frequency_name is unspecified.")

            match self.frequency_name:
                case domain.FrequencyType.Daily:
                    frequency: domain.Frequency = domain.Frequency.daily(start_date=self.start_date)
                case domain.FrequencyType.Easter:
                    frequency = domain.Frequency.easter(
                        advance_display_days=self.advance_days,
                        expire_display_days=self.expire_days,
                        start_date=self.start_date,
                    )
                case domain.FrequencyType.Irregular:
                    if isinstance(self.irregular_frequency_form_state, domain.Unspecified):
                        return domain.Error.new("irregular_frequency_form_state is unspecified.")

                    frequency = self.irregular_frequency_form_state.to_domain(
                        advance_display_days=self.advance_days,
                        expire_display_days=self.expire_days,
                        start_date=self.start_date,
                    )
                case domain.FrequencyType.Monthly:
                    if isinstance(self.monthly_frequency_form_state, domain.Unspecified):
                        return domain.Error.new("monthly_frequency_form_state is unspecified.")

                    frequency = self.monthly_frequency_form_state.to_domain(
                        advance_display_days=self.advance_days,
                        expire_display_days=self.expire_days,
                        start_date=self.start_date,
                    )
                case domain.FrequencyType.Once:
                    if isinstance(self.once_frequency_form_state, domain.Unspecified):
                        return domain.Error.new("once_frequency_form_state is unspecified.")

                    frequency = self.once_frequency_form_state.to_domain(
                        advance_display_days=self.advance_days,
                        expire_display_days=self.expire_days,
                        start_date=self.start_date,
                    )
                case domain.FrequencyType.Weekly:
                    if isinstance(self.weekly_frequency_form_state, domain.Unspecified):
                        return domain.Error.new("weekly_frequency_form_state is unspecified.")

                    frequency = self.weekly_frequency_form_state.to_domain(
                        advance_display_days=self.advance_days,
                        expire_display_days=self.expire_days,
                        start_date=self.start_date,
                    )
                case domain.FrequencyType.XDays:
                    if isinstance(self.xdays_frequency_form_state, domain.Unspecified):
                        return domain.Error.new("xdays_frequency_form_state is unspecified.")

                    frequency = self.xdays_frequency_form_state.to_domain(
                        advance_display_days=self.advance_days,
                        expire_display_days=self.expire_days,
                        start_date=self.start_date,
                    )
                case domain.FrequencyType.Yearly:
                    if isinstance(self.yearly_frequency_form_state, domain.Unspecified):
                        return domain.Error.new("yearly_frequency_form_state is unspecified.")

                    frequency = self.yearly_frequency_form_state.to_domain(
                        advance_display_days=self.advance_days,
                        expire_display_days=self.expire_days,
                        start_date=self.start_date,
                    )
                case _:
                    return domain.Error.new(f"Unrecognized [frequency_name], {self.frequency_name!r}.")

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
        except Exception as e:
            return domain.Error.new(str(e))

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
            focus_description=True,
        )
