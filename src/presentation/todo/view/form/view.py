from __future__ import annotations

import datetime
import typing

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa
from loguru import logger

from src import domain
from src.presentation.category_selector import CategorySelectorWidget
from src.presentation.shared import fonts, icons, widgets
from src.presentation.shared.widgets import DateEditor
from src.presentation.shared.widgets.rich_text_editor import RichTextEditor
from src.presentation.todo import requests
from src.presentation.todo.view.form.irregular.state import IrregularFrequencyFormState
from src.presentation.todo.view.form.irregular.view import IrregularFrequencyForm
from src.presentation.todo.view.form.monthly.state import MonthlyFrequencyFormState
from src.presentation.todo.view.form.monthly.view import MonthlyFrequencyForm
from src.presentation.todo.view.form.once.state import OnceFrequencyFormState
from src.presentation.todo.view.form.once.view import OnceFrequencyForm
from src.presentation.todo.view.form.state import TodoFormState
from src.presentation.todo.view.form.weekly.state import WeeklyFrequencyFormState
from src.presentation.todo.view.form.weekly.view import WeeklyFrequencyForm
from src.presentation.todo.view.form.xdays.state import XDaysFrequencyFormState
from src.presentation.todo.view.form.xdays.view import XDaysFrequencyForm
from src.presentation.todo.view.form.yearly.state import YearlyFrequencyFormState
from src.presentation.todo.view.form.yearly.view import YearlyFrequencyForm
from src.presentation.user_selector.widget import UserSelectorWidget

import qtawesome as qta

__all__ = ("TodoForm",)


class TodoForm(qtw.QWidget):
    back_requests = qtc.pyqtSignal()
    save_requests = qtc.pyqtSignal(requests.SaveRequest)

    def __init__(
        self,
        *,
        category_selector: CategorySelectorWidget,
        user_selector: UserSelectorWidget,
        parent: qtw.QWidget | None = None,
    ):
        super().__init__(parent=parent)

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
        self._frequency_cbo = widgets.MapCBO(
            mapping={
                domain.FrequencyType.Daily: "Daily",
                domain.FrequencyType.Irregular: "Irregular",
                domain.FrequencyType.Monthly: "Monthly",
                domain.FrequencyType.Once: "Once",
                domain.FrequencyType.Weekly: "Weekly",
                domain.FrequencyType.XDays: "XDays",
                domain.FrequencyType.Yearly: "Yearly",
            },
            value=domain.FrequencyType.Daily,
        )
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
            category=self._category_selector.get_selected_item(),
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

    def set_state(
        self,
        *,
        todo_id: str | domain.Unspecified = domain.Unspecified,
        template_todo_id: str | None | domain.Unspecified = domain.Unspecified,
        advance_days: int | domain.Unspecified = domain.Unspecified,
        expire_days: int | domain.Unspecified = domain.Unspecified,
        user: domain.User | domain.Unspecified = domain.Unspecified,
        category: domain.Category | domain.Unspecified = domain.Unspecified,
        description: str | domain.Unspecified = domain.Unspecified,
        frequency_name: domain.FrequencyType | domain.Unspecified = domain.Unspecified,
        note: str | domain.Unspecified = domain.Unspecified,
        start_date: datetime.date | domain.Unspecified = domain.Unspecified,
        date_added: datetime.datetime | domain.Unspecified = domain.Unspecified,
        date_updated: datetime.datetime | None | domain.Unspecified = domain.Unspecified,
        last_completed: datetime.date | None | domain.Unspecified = domain.Unspecified,
        prior_completed: datetime.date | None | domain.Unspecified = domain.Unspecified,
        last_completed_by: domain.User | None | domain.Unspecified = domain.Unspecified,
        prior_completed_by: domain.User | None | domain.Unspecified = domain.Unspecified,
        irregular_frequency_form_state: IrregularFrequencyFormState | domain.Unspecified = domain.Unspecified,
        monthly_frequency_form_state: MonthlyFrequencyFormState | domain.Unspecified = domain.Unspecified,
        once_frequency_form_state: OnceFrequencyFormState | domain.Unspecified = domain.Unspecified,
        weekly_frequency_form_state: WeeklyFrequencyFormState | domain.Unspecified = domain.Unspecified,
        xdays_frequency_form_state: XDaysFrequencyFormState | domain.Unspecified = domain.Unspecified,
        yearly_frequency_form_state: YearlyFrequencyFormState | domain.Unspecified = domain.Unspecified,
        categories_stale: bool | domain.Unspecified | domain.Unspecified = domain.Unspecified,
        users_stale: bool | domain.Unspecified | domain.Unspecified = domain.Unspecified,
        focus_description: bool | domain.Unspecified = domain.Unspecified,
    ) -> None:
        if not isinstance(todo_id, domain.Unspecified):
            self._todo_id = todo_id

        if not isinstance(template_todo_id, domain.Unspecified):
            self._template_todo_id = template_todo_id

        if not isinstance(date_added, domain.Unspecified):
            self._date_added = date_added

        if not isinstance(date_updated, domain.Unspecified):
            self._date_updated = date_updated

        if not isinstance(last_completed, domain.Unspecified):
            self._last_completed = last_completed

        if not isinstance(prior_completed, domain.Unspecified):
            self._prior_completed = prior_completed

        if not isinstance(users_stale, domain.Unspecified):
            self._user_selector.refresh()

        if not isinstance(user, domain.Unspecified):
            self._user_selector.select_item(user)

        if not isinstance(description, domain.Unspecified):
            self._description_txt.setText(description)

        if not isinstance(advance_days, domain.Unspecified):
            self._advance_days_sb.setValue(advance_days)

        if not isinstance(expire_days, domain.Unspecified):
            self._expire_days_sb.setValue(expire_days)

        if not isinstance(frequency_name, domain.Unspecified):
            self._advance_days_sb.setEnabled(frequency_name != domain.FrequencyType.Daily)
            self._expire_days_sb.setEnabled(frequency_name != domain.FrequencyType.Daily)

        if not isinstance(categories_stale, domain.Unspecified):
            self._category_selector.refresh()

        if not isinstance(category, domain.Unspecified):
            self._category_selector.select_item(category)

        if not isinstance(note, domain.Unspecified):
            self._note_txt.set_value(note)

        if not isinstance(start_date, domain.Unspecified):
            self._start_date_edit.set_value(start_date)

        if not isinstance(frequency_name, domain.Unspecified):
            self._frequency_cbo.set_value(value=frequency_name)

        if not isinstance(irregular_frequency_form_state, domain.Unspecified):
            self._irregular_frequency_form.set_state(state=irregular_frequency_form_state)

        if not isinstance(monthly_frequency_form_state, domain.Unspecified):
            self._monthly_frequency_form.set_state(state=monthly_frequency_form_state)

        if not isinstance(once_frequency_form_state, domain.Unspecified):
            self._one_off_frequency_form.set_state(state=once_frequency_form_state)

        if not isinstance(weekly_frequency_form_state, domain.Unspecified):
            self._weekly_frequency_form.set_state(state=weekly_frequency_form_state)

        if not isinstance(xdays_frequency_form_state, domain.Unspecified):
            self._xdays_frequency_form.set_state(state=xdays_frequency_form_state)

        if not isinstance(yearly_frequency_form_state, domain.Unspecified):
            self._yearly_frequency_form.set_state(state=yearly_frequency_form_state)

        if not isinstance(last_completed_by, domain.Unspecified):
            self._last_completed_by = last_completed_by

        if not isinstance(prior_completed_by, domain.Unspecified):
            self._prior_completed_by = prior_completed_by

        if not isinstance(focus_description, domain.Unspecified):
            if focus_description and not self._description_txt.hasFocus():
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

        self.back_requests.emit()

    def _on_save_btn_clicked(self, /, _: bool) -> None:
        logger.debug(f"{self.__class__.__name__}._on_save_btn_clicked()")

        todo_state = self.get_state()

        todo = todo_state.to_domain()

        request = requests.SaveRequest(todo=todo)

        self.save_requests.emit(request)
