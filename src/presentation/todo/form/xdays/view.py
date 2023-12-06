from __future__ import annotations

from PyQt5 import QtWidgets as qtw

from src.presentation.shared import fonts
from src.presentation.todo.form.xdays.state import XDaysFrequencyFormState

__all__ = ("XDaysFrequencyForm",)


class XDaysFrequencyForm(qtw.QWidget):
    def __init__(self, *, parent: qtw.QWidget | None = None):
        super().__init__(parent=parent)

        days_lbl = qtw.QLabel("Days Between")
        days_lbl.setFont(fonts.BOLD)
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
