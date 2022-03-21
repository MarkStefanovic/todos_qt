from PyQt5 import QtWidgets as qtw

from src import domain
from src.presentation.shared import fonts, widgets
from src.presentation.todo.form.irregular.state import IrregularFrequencyFormState

__all__ = ("IrregularFrequencyForm",)


class IrregularFrequencyForm(qtw.QWidget):
    def __init__(self, *, state: IrregularFrequencyFormState):
        super().__init__()

        month_lbl = qtw.QLabel("Month")
        month_lbl.setFont(fonts.bold)
        self._month_cbo = widgets.MapCBO(
            mapping={
                "Jan": domain.Month.January,
                "Feb": domain.Month.February,
                "Mar": domain.Month.March,
                "Apr": domain.Month.April,
                "May": domain.Month.May,
                "Jun": domain.Month.June,
                "Jul": domain.Month.July,
                "Aug": domain.Month.August,
                "Sep": domain.Month.September,
                "Oct": domain.Month.October,
                "Nov": domain.Month.November,
                "Dec": domain.Month.December,
            },
            value=state.month,
        )

        week_number_lbl = qtw.QLabel("Week #")
        week_number_lbl.setFont(fonts.bold)
        self._week_number_sb = qtw.QSpinBox()
        self._week_number_sb.setRange(1, 5)
        self._week_number_sb.setValue(state.week_number)

        weekday_lbl = qtw.QLabel("Weekday")
        weekday_lbl.setFont(fonts.bold)
        self._weekday_cbo = widgets.MapCBO(
            mapping={
                "Monday": domain.Weekday.Monday,
                "Tuesday": domain.Weekday.Tuesday,
                "Wednesday": domain.Weekday.Wednesday,
                "Thursday": domain.Weekday.Thursday,
                "Friday": domain.Weekday.Friday,
                "Saturday": domain.Weekday.Saturday,
                "Sunday": domain.Weekday.Sunday,
            },
            value=state.week_day,
        )

        form_layout = qtw.QFormLayout()
        form_layout.addRow(month_lbl, self._month_cbo)
        form_layout.addRow(week_number_lbl, self._week_number_sb)
        form_layout.addRow(weekday_lbl, self._weekday_cbo)

        self.setLayout(form_layout)

    def get_state(self) -> IrregularFrequencyFormState:
        return IrregularFrequencyFormState(
            month=self._month_cbo.get_value(),
            week_number=self._week_number_sb.value(),
            week_day=self._weekday_cbo.get_value(),
        )

    def set_state(self, *, state: IrregularFrequencyFormState) -> None:
        self._month_cbo.set_value(value=state.month)
        self._week_number_sb.setValue(state.week_number)
        self._weekday_cbo.set_value(value=state.week_day)
