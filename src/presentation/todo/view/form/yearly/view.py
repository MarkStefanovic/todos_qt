from __future__ import annotations

from PyQt5 import QtWidgets as qtw

from src import domain
from src.presentation.shared import fonts, widgets
from src.presentation.todo.view.form.yearly.state import YearlyFrequencyFormState

__all__ = ("YearlyFrequencyForm",)


class YearlyFrequencyForm(qtw.QWidget):
    def __init__(self, *, parent: qtw.QWidget | None = None):
        super().__init__(parent=parent)

        month_lbl = qtw.QLabel("Month")
        month_lbl.setFont(fonts.BOLD)
        self._month_cbo = widgets.MapCBO(
            mapping={
                domain.Month.January: "Jan",
                domain.Month.February: "Feb",
                domain.Month.March: "Mar",
                domain.Month.April: "Apr",
                domain.Month.May: "May",
                domain.Month.June: "Jun",
                domain.Month.July: "Jul",
                domain.Month.August: "Aug",
                domain.Month.September: "Sep",
                domain.Month.October: "Oct",
                domain.Month.November: "Nov",
                domain.Month.December: "Dec",
            },
            value=domain.Month.January,
        )
        self._month_cbo.setFixedWidth(100)

        month_day_lbl = qtw.QLabel("Month Day")
        month_day_lbl.setFont(fonts.BOLD)
        self._month_day_sb = qtw.QSpinBox()
        self._month_day_sb.setRange(1, 31)
        self._month_day_sb.setFixedWidth(100)

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
