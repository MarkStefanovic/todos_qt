from PyQt5 import QtWidgets as qtw

from src.presentation.todo.todo_edit_form import edit_form_model

__all__ = ("MonthlyTodoForm",)


class MonthlyTodoForm(qtw.QGroupBox):
    def __init__(self, /, model: edit_form_model.TodoEditFormModel):
        super().__init__()

        self._model = model

        self.month_day_field = qtw.QSpinBox()
        self.month_day_field.setRange(0, 29)
        self.month_day_field.setValue(self._model.month_day or 1)
        self.month_day_field.valueChanged.connect(self._model.set_month_day)

        layout = qtw.QFormLayout()
        layout.addRow(qtw.QLabel("Day"), self.month_day_field)
        self.setLayout(layout)
