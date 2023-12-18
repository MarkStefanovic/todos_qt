from __future__ import annotations

import datetime
import typing

import qtawesome as qta
from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa
from loguru import logger

from src import domain
from src.presentation.category_selector import CategorySelectorWidget
from src.presentation.shared import fonts, icons, widgets
from src.presentation.shared.widgets import DateEditor
from src.presentation.shared.widgets.rich_text_editor import RichTextEditor
from src.presentation.todo.view.form import requests
from src.presentation.todo.view.form.irregular.view import IrregularFrequencyForm
from src.presentation.todo.view.form.monthly.view import MonthlyFrequencyForm
from src.presentation.todo.view.form.once.view import OnceFrequencyForm
from src.presentation.todo.view.form.state import TodoFormState
from src.presentation.todo.view.form.weekly.view import WeeklyFrequencyForm
from src.presentation.todo.view.form.xdays.view import XDaysFrequencyForm
from src.presentation.todo.view.form.yearly.view import YearlyFrequencyForm
from src.presentation.user_selector.widget import UserSelectorWidget

__all__ = ("TodoForm",)


class TodoForm(qtw.QWidget):
    def __init__(
        self,
        *,
        form_requests: requests.TodoFormRequests,
        category_selector: CategorySelectorWidget,
        user_selector: UserSelectorWidget,
        parent: qtw.QWidget | None = None,
    ):
        super().__init__(parent=parent)

        self._requests: typing.Final[requests.TodoFormRequests] = form_requests
        self._category_selector: typing.Final[CategorySelectorWidget] = category_selector
        self._user_selector: typing.Final[UserSelectorWidget] = user_selector

        description_lbl = qtw.QLabel("Description")
        description_lbl.setFont(fonts.BOLD)
        self._description_txt = qtw.QLineEdit()

        advance_days_lbl = qtw.QLabel("Advance Days")
        advance_days_lbl.setFont(fonts.BOLD)
        self._advance_days_sb = qtw.QSpinBox()
        self._advance_days_sb.setRange(0, 999)
        self._advance_days_sb.setFixedWidth(80)

        expire_days_lbl = qtw.QLabel("Expire Days")
        expire_days_lbl.setFont(fonts.BOLD)
        self._expire_days_sb = qtw.QSpinBox()
        self._expire_days_sb.setRange(1, 999)
        self._expire_days_sb.setFixedWidth(80)

        user_lbl = qtw.QLabel("User")
        user_lbl.setFont(fonts.BOLD)

        category_lbl = qtw.QLabel("Category")
        category_lbl.setFont(fonts.BOLD)

        note_lbl = qtw.QLabel("Note")
        note_lbl.setFont(fonts.BOLD)
        self._note_txt = RichTextEditor(parent=self)

        start_date_lbl = qtw.QLabel("Start")
        start_date_lbl.setFont(fonts.BOLD)
        self._start_date_edit = DateEditor()

        frequency_lbl = qtw.QLabel("Frequency")
        frequency_lbl.setFont(fonts.BOLD)
        self._frequency_cbo: typing.Final[widgets.MapCBO[domain.FrequencyType]] = widgets.MapCBO()
        self._frequency_cbo.set_values(
            {
                domain.FrequencyType.Daily: "Daily",
                domain.FrequencyType.Irregular: "Irregular",
                domain.FrequencyType.Monthly: "Monthly",
                domain.FrequencyType.Once: "Once",
                domain.FrequencyType.Weekly: "Weekly",
                domain.FrequencyType.XDays: "XDays",
                domain.FrequencyType.Yearly: "Yearly",
            }
        )
        self._frequency_cbo.set_value(domain.FrequencyType.Daily)
        self._frequency_cbo.value_changed.connect(self._frequency_changed)
        self._frequency_cbo.setFixedWidth(150)

        self._irregular_frequency_form = IrregularFrequencyForm()
        self._monthly_frequency_form = MonthlyFrequencyForm()
        self._one_off_frequency_form = OnceFrequencyForm()
        self._weekly_frequency_form = WeeklyFrequencyForm()
        self._xdays_frequency_form = XDaysFrequencyForm()
        self._yearly_frequency_form = YearlyFrequencyForm()

        self._frequency_subform_layout = qtw.QStackedLayout()
        self._frequency_subform_layout.addWidget(qtw.QWidget())
        self._frequency_subform_layout.addWidget(self._irregular_frequency_form)
        self._frequency_subform_layout.addWidget(self._monthly_frequency_form)
        self._frequency_subform_layout.addWidget(self._one_off_frequency_form)
        self._frequency_subform_layout.addWidget(self._weekly_frequency_form)
        self._frequency_subform_layout.addWidget(self._xdays_frequency_form)
        self._frequency_subform_layout.addWidget(self._yearly_frequency_form)

        form_layout = qtw.QFormLayout()
        form_layout.addRow(description_lbl, self._description_txt)
        form_layout.addRow(start_date_lbl, self._start_date_edit)
        form_layout.addRow(advance_days_lbl, self._advance_days_sb)
        form_layout.addRow(expire_days_lbl, self._expire_days_sb)
        form_layout.addRow(user_lbl, self._user_selector)
        form_layout.addRow(category_lbl, self._category_selector)
        form_layout.addRow(note_lbl, self._note_txt)
        form_layout.addRow(frequency_lbl, self._frequency_cbo)

        back_btn_icon = qta.icon(icons.back_btn_icon_name, color=self.parent().palette().text().color())  # type: ignore
        self.back_btn = qtw.QPushButton(back_btn_icon, "Back")
        self.back_btn.setFont(fonts.BOLD)
        self.back_btn.setMaximumWidth(100)

        save_btn_icon = qta.icon(icons.save_btn_icon_name, color=self.parent().palette().text().color())  # type: ignore
        self.save_btn = qtw.QPushButton(save_btn_icon, "Save")
        self.save_btn.setFont(fonts.BOLD)
        self.save_btn.setMaximumWidth(100)
        self.save_btn.setDefault(True)

        main_layout = qtw.QVBoxLayout()
        main_layout.addWidget(self.back_btn, alignment=qtc.Qt.AlignLeft)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(self._frequency_subform_layout)
        main_layout.addSpacerItem(qtw.QSpacerItem(0, 0, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Expanding))
        main_layout.addWidget(self.save_btn, alignment=qtc.Qt.AlignRight)

        self.setLayout(main_layout)

        self._todo_id = ""
        self._template_todo_id: str | None = None
        self._date_added = datetime.datetime.now()
        self._date_updated: datetime.datetime | None = None
        self._last_completed: datetime.date | None = None
        self._prior_completed: datetime.date | None = None
        self._last_completed_by: domain.User | None = None
        self._prior_completed_by: domain.User | None = None

        # noinspection PyUnresolvedReferences
        self.back_btn.clicked.connect(self._on_back_btn_clicked)
        # noinspection PyUnresolvedReferences
        self.save_btn.clicked.connect(self._on_save_btn_clicked)

    def get_state(self) -> TodoFormState:
        return TodoFormState(
            todo_id=self._todo_id,
            template_todo_id=self._template_todo_id,
            user=self._user_selector.get_selected_item(),
            advance_days=self._advance_days_sb.value(),
            expire_days=self._expire_days_sb.value(),
            category=self._category_selector.selected_item(),
            description=self._description_txt.text(),
            frequency_name=self._frequency_cbo.get_value(),
            note=self._note_txt.get_value(),
            start_date=self._start_date_edit.get_value() or datetime.date(1900, 1, 1),
            date_added=self._date_added,
            date_updated=self._date_updated,
            last_completed=self._last_completed,
            prior_completed=self._prior_completed,
            last_completed_by=self._last_completed_by,
            prior_completed_by=self._prior_completed_by,
            irregular_frequency_form_state=self._irregular_frequency_form.get_state(),
            monthly_frequency_form_state=self._monthly_frequency_form.get_state(),
            once_frequency_form_state=self._one_off_frequency_form.get_state(),
            weekly_frequency_form_state=self._weekly_frequency_form.get_state(),
            xdays_frequency_form_state=self._xdays_frequency_form.get_state(),
            yearly_frequency_form_state=self._yearly_frequency_form.get_state(),
            categories_stale=False,
            users_stale=False,
            focus_description=self._description_txt.hasFocus(),
        )

    def set_state(self, /, state: TodoFormState) -> None:
        if not isinstance(state.todo_id, domain.Unspecified):
            self._todo_id = state.todo_id

        if not isinstance(state.template_todo_id, domain.Unspecified):
            self._template_todo_id = state.template_todo_id

        if not isinstance(state.date_added, domain.Unspecified):
            self._date_added = state.date_added

        if not isinstance(state.date_updated, domain.Unspecified):
            self._date_updated = state.date_updated

        if not isinstance(state.last_completed, domain.Unspecified):
            self._last_completed = state.last_completed

        if not isinstance(state.prior_completed, domain.Unspecified):
            self._prior_completed = state.prior_completed

        if not isinstance(state.users_stale, domain.Unspecified):
            if state.users_stale:
                self._user_selector.refresh()

        if not isinstance(state.user, domain.Unspecified):
            self._user_selector.select_item(state.user)

        if not isinstance(state.description, domain.Unspecified):
            self._description_txt.setText(state.description)

        if not isinstance(state.advance_days, domain.Unspecified):
            self._advance_days_sb.setValue(state.advance_days)

        if not isinstance(state.expire_days, domain.Unspecified):
            self._expire_days_sb.setValue(state.expire_days)

        if not isinstance(state.frequency_name, domain.Unspecified):
            self._advance_days_sb.setEnabled(state.frequency_name != domain.FrequencyType.Daily)
            self._expire_days_sb.setEnabled(state.frequency_name != domain.FrequencyType.Daily)

        if not isinstance(state.categories_stale, domain.Unspecified):
            if state.categories_stale:
                self._category_selector.refresh()

        if not isinstance(state.category, domain.Unspecified):
            self._category_selector.select_item(state.category)

        if not isinstance(state.note, domain.Unspecified):
            self._note_txt.set_value(state.note)

        if not isinstance(state.start_date, domain.Unspecified):
            self._start_date_edit.set_value(state.start_date)

        if not isinstance(state.frequency_name, domain.Unspecified):
            self._frequency_cbo.set_value(state.frequency_name)

        if not isinstance(state.irregular_frequency_form_state, domain.Unspecified):
            self._irregular_frequency_form.set_state(state.irregular_frequency_form_state)

        if not isinstance(state.monthly_frequency_form_state, domain.Unspecified):
            self._monthly_frequency_form.set_state(state.monthly_frequency_form_state)

        if not isinstance(state.once_frequency_form_state, domain.Unspecified):
            self._one_off_frequency_form.set_state(state.once_frequency_form_state)

        if not isinstance(state.weekly_frequency_form_state, domain.Unspecified):
            self._weekly_frequency_form.set_state(state.weekly_frequency_form_state)

        if not isinstance(state.xdays_frequency_form_state, domain.Unspecified):
            self._xdays_frequency_form.set_state(state.xdays_frequency_form_state)

        if not isinstance(state.yearly_frequency_form_state, domain.Unspecified):
            self._yearly_frequency_form.set_state(state.yearly_frequency_form_state)

        if not isinstance(state.last_completed_by, domain.Unspecified):
            self._last_completed_by = state.last_completed_by

        if not isinstance(state.prior_completed_by, domain.Unspecified):
            self._prior_completed_by = state.prior_completed_by

        if not isinstance(state.focus_description, domain.Unspecified):
            if state.focus_description and not self._description_txt.hasFocus():
                self._description_txt.setFocus()

    def _frequency_changed(self) -> None:
        frequency = self._frequency_cbo.get_value()

        self._advance_days_sb.setEnabled(frequency != domain.FrequencyType.Daily)
        self._expire_days_sb.setEnabled(frequency != domain.FrequencyType.Daily)
        self._advance_days_sb.setMaximum(999)
        self._expire_days_sb.setMaximum(999)

        if frequency == domain.FrequencyType.Daily:
            self._advance_days_sb.setValue(0)
            self._expire_days_sb.setValue(1)
            self._advance_days_sb.setMaximum(0)
            self._expire_days_sb.setMaximum(1)
            self._frequency_subform_layout.setCurrentIndex(0)
        elif frequency == domain.FrequencyType.Easter:
            raise ValueError("Easter is not meant to be created by the user.")
        elif frequency == domain.FrequencyType.Irregular:
            self._advance_days_sb.setValue(30)
            self._expire_days_sb.setValue(90)
            self._advance_days_sb.setMaximum(363)
            self._expire_days_sb.setMaximum(363)
            self._frequency_subform_layout.setCurrentIndex(1)
        elif frequency == domain.FrequencyType.Monthly:
            self._advance_days_sb.setValue(0)
            self._expire_days_sb.setValue(27)
            self._advance_days_sb.setMaximum(27)
            self._expire_days_sb.setMaximum(27)
            self._frequency_subform_layout.setCurrentIndex(2)
        elif frequency == domain.FrequencyType.Once:
            self._advance_days_sb.setValue(0)
            self._expire_days_sb.setValue(99)
            self._frequency_subform_layout.setCurrentIndex(3)
        elif frequency == domain.FrequencyType.Weekly:
            self._advance_days_sb.setValue(0)
            self._expire_days_sb.setValue(5)
            self._advance_days_sb.setMaximum(6)
            self._expire_days_sb.setMaximum(6)
            self._frequency_subform_layout.setCurrentIndex(4)
        elif frequency == domain.FrequencyType.XDays:
            self._advance_days_sb.setValue(0)
            self._expire_days_sb.setValue(9)
            self._frequency_subform_layout.setCurrentIndex(5)
        elif frequency == domain.FrequencyType.Yearly:
            self._advance_days_sb.setValue(30)
            self._expire_days_sb.setValue(90)
            self._advance_days_sb.setMaximum(363)
            self._expire_days_sb.setMaximum(363)
            self._frequency_subform_layout.setCurrentIndex(6)
        else:
            raise ValueError(f"Unrecognized frequency: {frequency!r}.")

    def _on_back_btn_clicked(self, /, _: bool) -> None:
        logger.debug(f"{self.__class__.__name__}._on_back_btn_clicked()")

        self._requests.back.emit()

    def _on_save_btn_clicked(self, /, _: bool) -> None:
        logger.debug(f"{self.__class__.__name__}._on_save_btn_clicked()")

        todo_state = self.get_state()

        todo = todo_state.to_domain()
        if isinstance(todo, domain.Error):
            logger.error(f"{self.__class__.__name__}._on_save_btn_clicked() failed: {todo!s}")
            self._requests.error.emit(str(todo))
            return None

        request = requests.SaveRequest(todo=todo)

        self._requests.save.emit(request)
