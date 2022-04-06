import datetime

from PyQt5 import QtCore as qtc, QtWidgets as qtw

from src import domain
from src.presentation.shared import fonts, widgets
from src.presentation.shared.widgets import MapCBO
from src.presentation.todo.form.irregular.view import IrregularFrequencyForm
from src.presentation.todo.form.monthly.view import MonthlyFrequencyForm
from src.presentation.todo.form.once.view import OnceFrequencyForm
from src.presentation.todo.form.state import TodoFormState
from src.presentation.todo.form.weekly.view import WeeklyFrequencyForm
from src.presentation.todo.form.xdays.view import XDaysFrequencyForm
from src.presentation.todo.form.yearly.view import YearlyFrequencyForm

__all__ = ("TodoForm",)


class TodoForm(qtw.QWidget):
    def __init__(self, *, state: TodoFormState):
        super().__init__()

        description_lbl = qtw.QLabel("Description")
        description_lbl.setFont(fonts.bold)
        self._description_txt = qtw.QLineEdit()

        advance_days_lbl = qtw.QLabel("Advance Days")
        advance_days_lbl.setFont(fonts.bold)
        self._advance_days_sb = qtw.QSpinBox()
        self._advance_days_sb.setRange(0, 364)
        self._advance_days_sb.setFixedWidth(80)

        expire_days_lbl = qtw.QLabel("Expire Days")
        expire_days_lbl.setFont(fonts.bold)
        self._expire_days_sb = qtw.QSpinBox()
        self._expire_days_sb.setRange(1, 364)
        self._expire_days_sb.setFixedWidth(80)

        user_lbl = qtw.QLabel("User")
        user_lbl.setFont(fonts.bold)
        self._user_cbo: MapCBO[domain.User] = MapCBO(
            mapping={user: user.display_name for user in state.user_options},
            value=state.user,
        )
        self._user_cbo.setFixedWidth(150)

        category_lbl = qtw.QLabel("Category")
        category_lbl.setFont(fonts.bold)
        self._category_cbo: MapCBO[domain.Category] = MapCBO(
            mapping={category: category.name for category in state.category_options},
            value=state.category,
        )
        self._category_cbo.setFixedWidth(150)

        note_lbl = qtw.QLabel("Note")
        note_lbl.setFont(fonts.bold)
        self._note_txt = qtw.QTextEdit()
        self._note_txt.setPlainText(state.note)

        start_date_lbl = qtw.QLabel("Start")
        start_date_lbl.setFont(fonts.bold)
        self._start_date_edit = qtw.QDateEdit()
        self._start_date_edit.setMinimumDate(datetime.date(1900, 1, 1))

        frequency_lbl = qtw.QLabel("Frequency")
        frequency_lbl.setFont(fonts.bold)
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
            value=state.frequency_name,
        )
        self._frequency_cbo.value_changed.connect(self._frequency_changed)
        self._frequency_cbo.setFixedWidth(150)

        self._irregular_frequency_form = IrregularFrequencyForm(state=state.irregular_frequency_form_state)
        self._monthly_frequency_form = MonthlyFrequencyForm(state=state.monthly_frequency_form_state)
        self._one_off_frequency_form = OnceFrequencyForm(state=state.once_frequency_form_state)
        self._weekly_frequency_form = WeeklyFrequencyForm(state=state.weekly_frequency_form_state)
        self._xdays_frequency_form = XDaysFrequencyForm(state=state.xdays_frequency_form_state)
        self._yearly_frequency_form = YearlyFrequencyForm(state=state.yearly_frequency_form_state)

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
        form_layout.addRow(advance_days_lbl, self._advance_days_sb)
        form_layout.addRow(expire_days_lbl, self._expire_days_sb)
        form_layout.addRow(user_lbl, self._user_cbo)
        form_layout.addRow(category_lbl, self._category_cbo)
        form_layout.addRow(note_lbl, self._note_txt)
        form_layout.addRow(frequency_lbl, self._frequency_cbo)

        self.back_btn = qtw.QPushButton("Back")
        self.back_btn.setFont(fonts.bold)
        self.back_btn.setFixedWidth(100)

        self.save_btn = qtw.QPushButton("Save")
        self.save_btn.setFont(fonts.bold)
        self.save_btn.setFixedWidth(100)

        main_layout = qtw.QVBoxLayout()
        main_layout.addWidget(self.back_btn, alignment=qtc.Qt.AlignLeft)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(self._frequency_subform_layout)
        main_layout.addSpacerItem(qtw.QSpacerItem(0, 0, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Expanding))
        main_layout.addWidget(self.save_btn, alignment=qtc.Qt.AlignRight)

        self.setLayout(main_layout)

        self._todo_id = state.todo_id
        self._date_added = state.date_added
        self._date_updated = state.date_updated
        self._user = state.user
        self._last_completed = state.last_completed
        self._prior_completed = state.prior_completed

        self.set_state(state=state)

    def get_state(self) -> TodoFormState:
        return TodoFormState(
            todo_id=self._todo_id,
            user=self._user,
            advance_days=self._advance_days_sb.value(),
            expire_days=self._expire_days_sb.value(),
            category=self._category_cbo.get_value(),
            description=self._description_txt.text(),
            frequency_name=self._frequency_cbo.get_value(),
            note=self._note_txt.toPlainText(),
            start_date=self._start_date_edit.date().toPyDate(),
            date_added=self._date_added,
            date_updated=self._date_updated,
            last_completed=self._last_completed,
            prior_completed=self._prior_completed,
            irregular_frequency_form_state=self._irregular_frequency_form.get_state(),
            monthly_frequency_form_state=self._monthly_frequency_form.get_state(),
            once_frequency_form_state=self._one_off_frequency_form.get_state(),
            weekly_frequency_form_state=self._weekly_frequency_form.get_state(),
            xdays_frequency_form_state=self._xdays_frequency_form.get_state(),
            yearly_frequency_form_state=self._yearly_frequency_form.get_state(),
            category_options=self._category_cbo.get_values(),
            user_options=self._user_cbo.get_values(),
        )

    def set_state(self, *, state: TodoFormState) -> None:
        self._todo_id = state.todo_id
        self._date_added = state.date_added
        self._date_updated = state.date_updated
        self._user = state.user
        self._last_completed = state.last_completed
        self._prior_completed = state.prior_completed

        self._description_txt.setText(state.description)
        self._advance_days_sb.setValue(state.advance_days)
        self._expire_days_sb.setValue(state.expire_days)
        self._advance_days_sb.setEnabled(state.frequency_name != domain.FrequencyType.Daily)
        self._expire_days_sb.setEnabled(state.frequency_name != domain.FrequencyType.Daily)
        self._category_cbo.set_values(mapping={category: category.name for category in state.category_options})
        self._category_cbo.set_value(value=state.category)
        self._user_cbo.set_values(mapping={user: user.display_name for user in state.user_options})
        self._user_cbo.set_value(value=state.user)
        self._note_txt.setPlainText(state.note)
        self._start_date_edit.setDate(state.start_date)
        self._frequency_cbo.set_value(value=state.frequency_name)

        self._irregular_frequency_form = IrregularFrequencyForm(state=state.irregular_frequency_form_state)
        self._monthly_frequency_form = MonthlyFrequencyForm(state=state.monthly_frequency_form_state)
        self._one_off_frequency_form = OnceFrequencyForm(state=state.once_frequency_form_state)
        self._weekly_frequency_form = WeeklyFrequencyForm(state=state.weekly_frequency_form_state)
        self._xdays_frequency_form = XDaysFrequencyForm(state=state.xdays_frequency_form_state)
        self._yearly_frequency_form = YearlyFrequencyForm(state=state.yearly_frequency_form_state)

    def _frequency_changed(self) -> None:
        frequency = self._frequency_cbo.get_value()

        self._advance_days_sb.setEnabled(frequency != domain.FrequencyType.Daily)
        self._expire_days_sb.setEnabled(frequency != domain.FrequencyType.Daily)

        if frequency == domain.FrequencyType.Daily:
            self._frequency_subform_layout.setCurrentIndex(0)
        elif frequency == domain.FrequencyType.Easter:
            raise ValueError("Easter is not meant to be created by the user.")
        elif frequency == domain.FrequencyType.Irregular:
            self._frequency_subform_layout.setCurrentIndex(1)
        elif frequency == domain.FrequencyType.Monthly:
            self._frequency_subform_layout.setCurrentIndex(2)
        elif frequency == domain.FrequencyType.Once:
            self._frequency_subform_layout.setCurrentIndex(3)
        elif frequency == domain.FrequencyType.Weekly:
            self._frequency_subform_layout.setCurrentIndex(4)
        elif frequency == domain.FrequencyType.XDays:
            self._frequency_subform_layout.setCurrentIndex(5)
        elif frequency == domain.FrequencyType.Yearly:
            self._frequency_subform_layout.setCurrentIndex(6)
        else:
            raise ValueError(f"Unrecognized frequency: {frequency!r}.")
