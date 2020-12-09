from PyQt5 import QtWidgets as qtw

from src.presentation.todo.todo_edit_form import edit_form_model

__all__ = ("XDaysForm",)


class XDaysForm(qtw.QGroupBox):
    def __init__(self, /, model: edit_form_model.TodoEditFormModel):
        super().__init__()

        self._model = model

        self.start_date_widget = qtw.QDateEdit(calendarPopup=True)  # type: ignore
        self.start_date_widget.setDate(self._model.start_date)
        self.start_date_widget.dateChanged.connect(self._model.set_start_date)

        self.x_days_widget = qtw.QSpinBox()
        self.x_days_widget.setMinimum(2)
        self.x_days_widget.setValue(self._model.days or 2)
        self.x_days_widget.valueChanged.connect(self._model.set_days)

        layout = qtw.QFormLayout()
        layout.addRow(qtw.QLabel("Start"), self.start_date_widget)
        layout.addRow(qtw.QLabel("Days"), self.x_days_widget)
        self.setLayout(layout)
