from __future__ import annotations

import typing

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa

from src import domain
from src.presentation.todo.state import TodoState
from src.presentation.todo.view.dash.state import TodoDashState
from src.presentation.todo.view.dash.view import TodoDash
from src.presentation.todo.view.form.state import TodoFormState
from src.presentation.todo.view.form.view import TodoForm

__all__ = ("TodoView",)


class TodoView(qtw.QWidget):
    def __init__(
        self,
        *,
        current_user: domain.User,
        parent: qtw.QWidget | None = None,
    ):
        super().__init__(parent=parent)

        self.dash = TodoDash(
            parent=self,
            current_user=current_user,
        )

        self.form = TodoForm(
            parent=self,
        )

        self.stacked_layout = qtw.QStackedLayout()
        self.stacked_layout.addWidget(self.dash)
        self.stacked_layout.addWidget(self.form)

        self.setLayout(self.stacked_layout)

    def refresh_dash(self) -> None:
        self.dash.refresh()

    def get_state(self) -> TodoState:
        return TodoState(
            dash_state=self.dash.get_state(),
            form_state=self.form.get_state(),
            dash_active=self.stacked_layout.currentIndex() == 0,
        )

    def save_form(self) -> None:
        self.form.save_btn.click()

    def set_state(
        self,
        *,
        dash_state: TodoDashState | domain.Unspecified = domain.Unspecified,
        form_state: TodoFormState | domain.Unspecified = domain.Unspecified,
        dash_active: bool | domain.Unspecified = domain.Unspecified,
    ) -> None:
        if not isinstance(dash_state, domain.Unspecified):
            self.dash.set_state(dash_state)

        if not isinstance(form_state, domain.Unspecified):
            self.form.set_state(
                todo_id=form_state.todo_id,
                template_todo_id=form_state.template_todo_id,
                advance_days=form_state.advance_days,
                expire_days=form_state.expire_days,
                user=form_state.user,
                category=form_state.category,
                description=form_state.description,
                frequency_name=form_state.frequency_name,
                note=form_state.note,
                start_date=form_state.start_date,
                date_added=form_state.date_added,
                date_updated=form_state.date_updated,
                last_completed=form_state.last_completed,
                prior_completed=form_state.prior_completed,
                last_completed_by=form_state.last_completed_by,
                prior_completed_by=form_state.prior_completed_by,
                irregular_frequency_form_state=form_state.irregular_frequency_form_state,
                monthly_frequency_form_state=form_state.monthly_frequency_form_state,
                once_frequency_form_state=form_state.once_frequency_form_state,
                weekly_frequency_form_state=form_state.weekly_frequency_form_state,
                xdays_frequency_form_state=form_state.xdays_frequency_form_state,
                yearly_frequency_form_state=form_state.yearly_frequency_form_state,
                categories_stale=form_state.categories_stale,
                users_stale=form_state.users_stale,
                focus_description=form_state.focus_description,
            )

        if not isinstance(dash_active, domain.Unspecified):
            if dash_active:
                self.stacked_layout.setCurrentIndex(0)
            else:
                self.stacked_layout.setCurrentIndex(1)

    def current_view(self) -> typing.Literal["dash", "form"]:
        if self.stacked_layout.currentIndex() == 0:
            return "dash"
        return "form"
