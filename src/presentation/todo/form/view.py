from PyQt5 import QtCore as qtc, QtWidgets as qtw

from src import domain
from src.presentation.shared import fonts, widgets
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

        expire_days_lbl = qtw.QLabel("Expire Days")
        expire_days_lbl.setFont(fonts.bold)
        self._expire_days_sb = qtw.QSpinBox()
        self._expire_days_sb.setRange(0, 364)

        category_lbl = qtw.QLabel("Category")
        category_lbl.setFont(fonts.bold)
        self._category_cbo = widgets.EnumCBO(cls=domain.TodoCategory, value=state.category)

        note_lbl = qtw.QLabel("Note")
        note_lbl.setFont(fonts.bold)
        self._note_txt = qtw.QTextEdit(state.note)

        start_date_lbl = qtw.QLabel("Start")
        start_date_lbl.setFont(fonts.bold)
        self._start_date_edit = qtw.QDateEdit()
        self._start_date_edit.setDate(state.start_date)

        frequency_lbl = qtw.QLabel("Frequency")
        frequency_lbl.setFont(fonts.bold)
        self._frequency_cbo = widgets.EnumCBO(cls=domain.FrequencyType, value=state.frequency.name)

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
        main_layout.addWidget(self.save_btn, alignment=qtc.Qt.AlignRight)

        self.setLayout(main_layout)

    def get_state(self) -> TodoFormState:
        return TodoFormState(
            advance_days=self._advance_days_sb.value(),
            expire_days=self._expire_days_sb.value(),
            category=self._category_cbo.get_value(),
            description=self._description_txt.text(),
            frequency=self._frequency_cbo.get_value(),
            note=self._note_txt.toPlainText(),
            start_date=self._start_date_edit.date().toPyDate(),
            irregular_frequency_form_state=self._irregular_frequency_form.get_state(),
            monthly_frequency_form_state=self._monthly_frequency_form.get_state(),
            once_frequency_form_state=self._once_frequency_form.get_state(),
            weekly_frequency_form_state=self._weekly_frequency_form.get_state(),
            xdays_frequency_form_state=self._xdays_frequency_form.get_state(),
            yearly_frequency_form_state=self._yearly_frequency_form.get_state(),
        )

    def set_state(self, *, state: TodoFormState) -> None:
        self._description_txt.setText(state.description)
        self._advance_days_sb.setValue(state.advance_days)
        self._expire_days_sb.setValue(state.expire_days)
        self._category_cbo.set_value(value=state.category)
        self._note_txt.setText(state.note)
        self._start_date_edit.setDate(state.start_date)
        self._frequency_cbo.set_value(value=state.frequency.name)

        if (freq := state.frequency.name) in (domain.FrequencyType.Daily, domain.FrequencyType.Easter):
            self._frequency_subform_layout.setCurrentIndex(0)
        elif freq == domain.FrequencyType.Irregular:
            self._frequency_subform_layout.setCurrentIndex(1)
        elif freq == domain.FrequencyType.Monthly:
            self._frequency_subform_layout.setCurrentIndex(2)
        elif freq == domain.FrequencyType.Once:
            self._frequency_subform_layout.setCurrentIndex(3)
        elif freq == domain.FrequencyType.Weekly:
            self._frequency_subform_layout.setCurrentIndex(4)
        elif freq == domain.FrequencyType.XDays:
            self._frequency_subform_layout.setCurrentIndex(5)
        elif freq == domain.FrequencyType.Yearly:
            self._frequency_subform_layout.setCurrentIndex(6)
        else:
            raise ValueError(f"Unrecognized frequency: {state.frequency.name!r}.")

        self._irregular_frequency_form = IrregularFrequencyForm(state=state.irregular_frequency_form_state)
        self._monthly_frequency_form = MonthlyFrequencyForm(state=state.monthly_frequency_form_state)
        self._one_off_frequency_form = OnceFrequencyForm(state=state.once_frequency_form_state)
        self._weekly_frequency_form = WeeklyFrequencyForm(state=state.weekly_frequency_form_state)
        self._xdays_frequency_form = XDaysFrequencyForm(state=state.xdays_frequency_form_state)
        self._yearly_frequency_form = YearlyFrequencyForm(state=state.yearly_frequency_form_state)
