from PyQt5 import QtWidgets as qtw

from src import domain
from src.presentation.shared import fonts, widgets
from src.presentation.todo.form.yearly.state import YearlyFrequencyFormState

__all__ = ("YearlyFrequencyForm",)


class YearlyFrequencyForm(qtw.QWidget):
    def __init__(self, *, state: YearlyFrequencyFormState):
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

        month_day_lbl = qtw.QLabel("Month Day")
        month_day_lbl.setFont(fonts.bold)
        self._month_day_sb = qtw.QSpinBox()
        self._month_day_sb.setRange(1, 28)
        self._month_day_sb.setValue(state.month_day)

        form_layout = qtw.QFormLayout()
        form_layout.addRow(month_lbl, self._month_cbo)
        form_layout.addRow(month_day_lbl, self._month_day_sb)

        self.setLayout(form_layout)

    def get_state(self) -> YearlyFrequencyFormState:
        return YearlyFrequencyFormState(
            month=self._month_cbo.get_value(),
            month_day=self._month_day_sb.value(),
        )

    def set_state(self, *, state: YearlyFrequencyFormState) -> None:
        self._month_cbo.set_value(value=state.month)
        self._month_day_sb.setValue(state.month_day)
