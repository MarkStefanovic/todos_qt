from PyQt5 import QtWidgets as qtw

from src import domain
from src.presentation.shared import fonts, widgets
from src.presentation.todo.form.weekly.state import WeeklyFrequencyFormState

__all__ = ("WeeklyFrequencyForm",)


class WeeklyFrequencyForm(qtw.QWidget):
    def __init__(self, *, state: WeeklyFrequencyFormState):
        super().__init__()

        weekday_lbl = qtw.QLabel("Weekday")
        weekday_lbl.setFont(fonts.bold)
        self._weekday_cbo = widgets.MapCBO(
            mapping={
                domain.Weekday.Monday: "Monday",
                domain.Weekday.Tuesday: "Tuesday",
                domain.Weekday.Wednesday: "Wednesday",
                domain.Weekday.Thursday: "Thursday",
                domain.Weekday.Friday: "Friday",
                domain.Weekday.Saturday: "Saturday",
                domain.Weekday.Sunday: "Sunday",
            },
            value=state.week_day,
        )
        self._weekday_cbo.setFixedWidth(150)

        form_layout = qtw.QFormLayout()
        form_layout.addRow(weekday_lbl, self._weekday_cbo)

        self.setLayout(form_layout)

        self.set_state(state=state)

    def get_state(self) -> WeeklyFrequencyFormState:
        return WeeklyFrequencyFormState(week_day=self._weekday_cbo.get_value())

    def set_state(self, *, state: WeeklyFrequencyFormState) -> None:
        self._weekday_cbo.set_value(value=state.week_day)
