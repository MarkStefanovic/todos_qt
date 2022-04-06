from PyQt5 import QtWidgets as qtw

from src.presentation.shared import fonts
from src.presentation.todo.form.xdays.state import XDaysFrequencyFormState

__all__ = ("XDaysFrequencyForm",)


class XDaysFrequencyForm(qtw.QWidget):
    def __init__(self):
        super().__init__()

        days_lbl = qtw.QLabel("Month")
        days_lbl.setFont(fonts.bold)
        self._days_sb = qtw.QSpinBox()
        self._days_sb.setRange(1, 364)
        self._days_sb.setFixedWidth(100)

        form_layout = qtw.QFormLayout()
        form_layout.addRow(days_lbl, self._days_sb)

        self.setLayout(form_layout)

    def get_state(self) -> XDaysFrequencyFormState:
        return XDaysFrequencyFormState(days=self._days_sb.value())

    def set_state(self, *, state: XDaysFrequencyFormState) -> None:
        self._days_sb.setValue(state.days)
