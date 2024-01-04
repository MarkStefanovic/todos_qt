# noinspection PyPep8Naming
from PyQt6 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw

from src.presentation.shared.theme import font
from src.presentation.todo.view.form.monthly.state import MonthlyFrequencyFormState

__all__ = ("MonthlyFrequencyForm",)


class MonthlyFrequencyForm(qtw.QWidget):
    def __init__(self, *, label_width: int, parent: qtw.QWidget | None):
        super().__init__(parent=parent)

        month_day_lbl = qtw.QLabel("Day")
        month_day_lbl.setFont(font.BOLD_FONT)
        month_day_lbl.setFixedWidth(label_width)
        self._month_day_sb = qtw.QSpinBox()
        self._month_day_sb.setRange(1, 28)
        self._month_day_sb.setFixedWidth(font.DEFAULT_FONT_METRICS.boundingRect("    28    ").width())

        layout = qtw.QHBoxLayout()
        layout.addWidget(month_day_lbl, alignment=qtc.Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self._month_day_sb, alignment=qtc.Qt.AlignmentFlag.AlignTop)
        layout.addStretch()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def get_state(self) -> MonthlyFrequencyFormState:
        return MonthlyFrequencyFormState(month_day=self._month_day_sb.value())

    def set_state(self, /, state: MonthlyFrequencyFormState) -> None:
        self._month_day_sb.setValue(state.month_day)
