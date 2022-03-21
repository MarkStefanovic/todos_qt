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
        form_layout.addRow(weekday_lbl, self._weekday_cbo)

        self.setLayout(form_layout)

    def get_state(self) -> WeeklyFrequencyFormState:
        return WeeklyFrequencyFormState(week_day=self._weekday_cbo.get_value())

    def set_state(self, *, state: WeeklyFrequencyFormState) -> None:
        self._weekday_cbo.set_value(value=state.week_day)
