from PyQt5 import QtWidgets as qtw

from src.presentation.shared import fonts
from src.presentation.todo.form.once.state import OnceFrequencyFormState

__all__ = ("OnceFrequencyForm",)


class OnceFrequencyForm(qtw.QWidget):
    def __init__(self, *, state: OnceFrequencyFormState):
        super().__init__()

        due_date_lbl = qtw.QLabel("Due Date")
        due_date_lbl.setFont(fonts.bold)
        self._due_date_edit = qtw.QDateEdit()
        self._due_date_edit.setDate(state.due_date)
        self._due_date_edit.setFixedWidth(150)

        form_layout = qtw.QFormLayout()
        form_layout.addRow(due_date_lbl, self._due_date_edit)

        self.setLayout(form_layout)

        self.set_state(state=state)

    def get_state(self) -> OnceFrequencyFormState:
        return OnceFrequencyFormState(due_date=self._due_date_edit.date().toPyDate())

    def set_state(self, *, state: OnceFrequencyFormState) -> None:
        self._due_date_edit.setDate(state.due_date)
