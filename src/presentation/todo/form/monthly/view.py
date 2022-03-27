from PyQt5 import QtWidgets as qtw

from src.presentation.shared import fonts
from src.presentation.todo.form.monthly.state import MonthlyFrequencyFormState

__all__ = ("MonthlyFrequencyForm",)


class MonthlyFrequencyForm(qtw.QWidget):
    def __init__(self, *, state: MonthlyFrequencyFormState):
        super().__init__()

        month_day_lbl = qtw.QLabel("Month")
        month_day_lbl.setFont(fonts.bold)
        self._month_day_sb = qtw.QSpinBox()
        self._month_day_sb.setRange(1, 31)
        self._month_day_sb.setFixedWidth(100)

        form_layout = qtw.QFormLayout()
        form_layout.addRow(month_day_lbl, self._month_day_sb)

        self.setLayout(form_layout)

        self.set_state(state=state)

    def get_state(self) -> MonthlyFrequencyFormState:
        return MonthlyFrequencyFormState(month_day=self._month_day_sb.value())

    def set_state(self, *, state: MonthlyFrequencyFormState) -> None:
        self._month_day_sb.setValue(state.month_day)
