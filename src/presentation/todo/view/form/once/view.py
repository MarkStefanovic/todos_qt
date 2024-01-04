import datetime

from PyQt6 import QtCore as qtc, QtWidgets as qtw  # noqa

from src.presentation.shared import widgets
from src.presentation.shared.theme import font
from src.presentation.todo.view.form.once.state import OnceFrequencyFormState

__all__ = ("OnceFrequencyForm",)


class OnceFrequencyForm(qtw.QWidget):
    def __init__(self, *, label_width: int, parent: qtw.QWidget | None):
        super().__init__(parent=parent)

        due_date_lbl = qtw.QLabel("Due Date")
        due_date_lbl.setFont(font.BOLD_FONT)
        due_date_lbl.setFixedWidth(label_width)
        self._due_date_edit = widgets.DateEditor()
        self._due_date_edit.setFixedWidth(150)

        layout = qtw.QHBoxLayout()
        layout.addWidget(due_date_lbl, alignment=qtc.Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self._due_date_edit, alignment=qtc.Qt.AlignmentFlag.AlignTop)
        layout.addStretch()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def get_state(self) -> OnceFrequencyFormState:
        return OnceFrequencyFormState(
            due_date=self._due_date_edit.get_value() or datetime.date.today(),
        )

    def set_state(self, /, state: OnceFrequencyFormState) -> None:
        self._due_date_edit.set_value(state.due_date)
