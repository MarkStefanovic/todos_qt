from PyQt5 import QtWidgets as qtw

from src.presentation.todo.todo_edit_form import edit_form_model

__all__ = ("OnceTodoForm",)


class OnceTodoForm(qtw.QGroupBox):
    def __init__(self, /, model: edit_form_model.TodoEditFormModel):
        super().__init__()

        self._model = model

        self.once_date_widget = qtw.QDateEdit(calendarPopup=True)  # type: ignore
        self.once_date_widget.setDate(self._model.start_date)
        self.once_date_widget.dateChanged.connect(self._model.set_start_date)

        layout = qtw.QFormLayout()
        layout.addRow(qtw.QLabel("On"), self.once_date_widget)
        self.setLayout(layout)
