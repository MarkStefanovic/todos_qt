# noinspection PyPep8Naming
from PyQt6 import QtCore as qtc, QtWidgets as qtw

from src.presentation.shared.theme import font
from src.presentation.todo.view.form.xdays.state import XDaysFrequencyFormState

__all__ = ("XDaysFrequencyForm",)


class XDaysFrequencyForm(qtw.QWidget):
    def __init__(self, *, label_width: int, parent: qtw.QWidget | None):
        super().__init__(parent=parent)

        days_lbl = qtw.QLabel("Days Between")
        days_lbl.setFont(font.BOLD_FONT)
        days_lbl.setFixedWidth(label_width)
        self._days_sb = qtw.QSpinBox()
        self._days_sb.setRange(1, 364)
        self._days_sb.setFixedWidth(100)

        layout = qtw.QHBoxLayout()
        layout.addWidget(days_lbl, alignment=qtc.Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self._days_sb, alignment=qtc.Qt.AlignmentFlag.AlignTop)
        layout.addStretch()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def get_state(self) -> XDaysFrequencyFormState:
        return XDaysFrequencyFormState(days=self._days_sb.value())

    def set_state(self, /, state: XDaysFrequencyFormState) -> None:
        self._days_sb.setValue(state.days)
