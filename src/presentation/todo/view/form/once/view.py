from __future__ import annotations

import datetime

from PyQt5 import QtWidgets as qtw  # noqa

from src.presentation.shared import fonts, widgets
from src.presentation.todo.view.form.once.state import OnceFrequencyFormState

__all__ = ("OnceFrequencyForm",)


class OnceFrequencyForm(qtw.QWidget):
    def __init__(self, *, parent: qtw.QWidget | None = None):
        super().__init__(parent=parent)

        due_date_lbl = qtw.QLabel("Due Date")
        due_date_lbl.setFont(fonts.BOLD)
        self._due_date_edit = widgets.DateEditor()
        self._due_date_edit.setFixedWidth(150)

        form_layout = qtw.QFormLayout()
        form_layout.addRow(due_date_lbl, self._due_date_edit)

        self.setLayout(form_layout)

    def get_state(self) -> OnceFrequencyFormState:
        return OnceFrequencyFormState(
            due_date=self._due_date_edit.get_value() or datetime.date.today(),
        )

    def set_state(self, /, state: OnceFrequencyFormState) -> None:
        self._due_date_edit.set_value(state.due_date)
