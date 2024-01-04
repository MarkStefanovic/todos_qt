import typing

from PyQt6 import QtCore as qtc, QtWidgets as qtw  # noqa
from loguru import logger

from src import domain
from src.presentation.shared import widgets
from src.presentation.shared.theme import font
from src.presentation.todo.view.form.weekly.state import WeeklyFrequencyFormState

__all__ = ("WeeklyFrequencyForm",)


class WeeklyFrequencyForm(qtw.QWidget):
    def __init__(self, *, label_width: int, parent: qtw.QWidget | None):
        super().__init__(parent=parent)

        weekday_lbl = qtw.QLabel("Weekday")
        weekday_lbl.setFont(font.BOLD_FONT)
        weekday_lbl.setFixedWidth(label_width)
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

        layout = qtw.QHBoxLayout()
        layout.addWidget(weekday_lbl, alignment=qtc.Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self._weekday_cbo, alignment=qtc.Qt.AlignmentFlag.AlignTop)
        layout.addStretch()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

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
