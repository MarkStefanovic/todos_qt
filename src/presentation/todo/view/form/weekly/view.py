import typing

from PyQt6 import QtWidgets as qtw  # noqa
from loguru import logger

from src import domain
from src.presentation.shared import widgets
from src.presentation.todo.view.form.weekly.state import WeeklyFrequencyFormState

__all__ = ("WeeklyFrequencyForm",)


class WeeklyFrequencyForm(qtw.QWidget):
    def __init__(self, *, parent: qtw.QWidget | None = None):
        super().__init__(parent=parent)

        weekday_lbl = qtw.QLabel("Weekday")
        weekday_lbl.font().setBold(True)
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
            }
        )
        self._weekday_cbo.set_value(domain.Weekday.Monday)
        self._weekday_cbo.setFixedWidth(150)

        form_layout = qtw.QFormLayout()
        form_layout.addRow(weekday_lbl, self._weekday_cbo)

        self.setLayout(form_layout)

    def get_state(self) -> WeeklyFrequencyFormState | domain.Error:
        try:
            weekday = self._weekday_cbo.get_value()
            if weekday is None:
                return domain.Error.new("weekday is required.")

            return WeeklyFrequencyFormState(week_day=weekday)
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.get_state() failed: {e!s}")
            return domain.Error.new(str(e))

    def set_state(self, /, state: WeeklyFrequencyFormState) -> None:
        self._weekday_cbo.set_value(value=state.week_day)
