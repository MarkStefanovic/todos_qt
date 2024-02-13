import typing

# noinspection PyPep8Naming
from PyQt6 import QtWidgets as qtw
from loguru import logger

from src import domain
from src.presentation.shared import widgets
from src.presentation.shared.theme import font
from src.presentation.todo.view.form.yearly.state import YearlyFrequencyFormState

__all__ = ("YearlyFrequencyForm",)


class YearlyFrequencyForm(qtw.QWidget):
    def __init__(self, *, label_width: int, parent: qtw.QWidget | None):
        super().__init__(parent=parent)

        month_lbl = qtw.QLabel("Month")
        month_lbl.setFont(font.BOLD_FONT)
        month_lbl.setFixedWidth(label_width)
        self._month_cbo: typing.Final[widgets.MapCBO[domain.Month]] = widgets.MapCBO(parent=self)
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
        self._month_cbo.setFixedWidth(100)

        month_day_lbl = qtw.QLabel("Month Day")
        month_day_lbl.setFont(font.BOLD_FONT)
        self._month_day_sb = qtw.QSpinBox()
        self._month_day_sb.setRange(1, 28)
        self._month_day_sb.setFixedWidth(100)
        self._month_day_sb.setValue(1)

        form_layout = qtw.QFormLayout()
        form_layout.addRow(month_lbl, self._month_cbo)
        form_layout.addRow(month_day_lbl, self._month_day_sb)
        form_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(form_layout)

    def get_state(self) -> YearlyFrequencyFormState | domain.Error:
        try:
            month = self._month_cbo.get_value()
            if month is None:
                return domain.Error.new("month is required.")

            return YearlyFrequencyFormState(
                month=month,
                month_day=self._month_day_sb.value(),
            )
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.get_state() failed: {e!s}")
            return domain.Error.new(str(e))

    def set_state(self, /, state: YearlyFrequencyFormState) -> None:
        self._month_cbo.set_value(value=state.month)
        self._month_day_sb.setValue(state.month_day)
