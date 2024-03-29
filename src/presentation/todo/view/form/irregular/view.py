from __future__ import annotations

import typing

# noinspection PyPep8Naming
from PyQt6 import QtCore as qtc, QtWidgets as qtw

from src import domain
from src.presentation.shared import widgets
from src.presentation.shared.theme import font
from src.presentation.todo.view.form.irregular.state import IrregularFrequencyFormState

__all__ = ("IrregularFrequencyForm",)


class IrregularFrequencyForm(qtw.QWidget):
    def __init__(self, *, label_width: int, parent: qtw.QWidget | None):
        super().__init__(parent=parent)

        month_lbl = qtw.QLabel("Month")
        month_lbl.setFont(font.BOLD_FONT)
        month_lbl.setFixedWidth(label_width)
        self._month_cbo: widgets.MapCBO[domain.Month] = widgets.MapCBO()
        self._month_cbo.set_values(
            {
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
            }
        )
        self._month_cbo.set_value(domain.Month.January)
        self._month_cbo.setFixedWidth(150)

        week_number_lbl = qtw.QLabel("Week #")
        week_number_lbl.setFont(font.BOLD_FONT)
        self._week_number_sb = qtw.QSpinBox()
        self._week_number_sb.setRange(1, 5)
        self._week_number_sb.setFixedWidth(150)

        weekday_lbl = qtw.QLabel("Weekday")
        weekday_lbl.setFont(font.BOLD_FONT)
        self._weekday_cbo: typing.Final[widgets.MapCBO[domain.Weekday]] = widgets.MapCBO()
        self._weekday_cbo.set_values(
            {
                domain.Weekday.Monday: "Monday",
                domain.Weekday.Tuesday: "Tuesday",
                domain.Weekday.Wednesday: "Wednesday",
                domain.Weekday.Thursday: "Thursday",
                domain.Weekday.Friday: "Friday",
                domain.Weekday.Saturday: "Saturday",
                domain.Weekday.Sunday: "Sunday",
            },
        )
        self._weekday_cbo.set_value(domain.Weekday.Monday)
        self._weekday_cbo.setFixedWidth(150)

        form_layout = qtw.QFormLayout()
        form_layout.setAlignment(qtc.Qt.AlignmentFlag.AlignLeft)
        form_layout.addRow(month_lbl, self._month_cbo)
        form_layout.addRow(week_number_lbl, self._week_number_sb)
        form_layout.addRow(weekday_lbl, self._weekday_cbo)
        form_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(form_layout)

    def get_state(self) -> IrregularFrequencyFormState | domain.Error:
        month = self._month_cbo.get_value()
        if month is None:
            return domain.Error.new("month is required.")

        weekday = self._weekday_cbo.get_value()
        if weekday is None:
            return domain.Error.new("weekday is required.")

        return IrregularFrequencyFormState(
            month=month,
            week_number=self._week_number_sb.value(),
            week_day=weekday,
        )

    def set_state(self, /, state: IrregularFrequencyFormState) -> None:
        self._month_cbo.set_value(value=state.month)
        self._week_number_sb.setValue(state.week_number)
        self._weekday_cbo.set_value(value=state.week_day)
