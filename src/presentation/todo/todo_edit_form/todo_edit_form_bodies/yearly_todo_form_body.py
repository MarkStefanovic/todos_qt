from PyQt5 import QtWidgets as qtw

from src import domain
from src.presentation.todo.todo_edit_form import edit_form_model

__all__ = ("YearlyTodoForm",)


class YearlyTodoForm(qtw.QGroupBox):
    def __init__(self, /, model: edit_form_model.TodoEditFormModel):
        super().__init__()

        self._model = model

        self.month_field = qtw.QComboBox()
        for w in domain.Month:
            self.month_field.addItem(str(w), w.value)
        self.month_field.setCurrentIndex((self._model.month or 1) - 1)
        self.month_field.currentIndexChanged.connect(
            lambda mo: self._model.set_month(mo - 1)
        )

        self.day_field = qtw.QSpinBox()
        self.day_field.setRange(1, 31)
        self.day_field.setValue(self._model.month_day or 1)
        self.day_field.valueChanged.connect(self._model.set_month_day)

        layout = qtw.QFormLayout()
        layout.addRow(qtw.QLabel("Month"), self.month_field)
        layout.addRow(qtw.QLabel("Day"), self.day_field)

        self.setLayout(layout)
