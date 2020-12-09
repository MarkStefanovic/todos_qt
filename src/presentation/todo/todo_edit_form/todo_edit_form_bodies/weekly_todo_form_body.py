from PyQt5 import QtWidgets as qtw

from src import domain
from src.presentation.todo.todo_edit_form import edit_form_model

__all__ = ("WeeklyTodoForm",)


class WeeklyTodoForm(qtw.QGroupBox):
    def __init__(self, /, model: edit_form_model.TodoEditFormModel):
        super().__init__()

        self._model = model

        self.week_day_field = qtw.QComboBox()
        for w in domain.Weekday:
            self.week_day_field.addItem(str(w), w.value)
        self.week_day_field.setCurrentIndex((self._model.week_day or 1) - 1)
        self.week_day_field.currentIndexChanged.connect(
            lambda wd: self._model.set_week_day(wd - 1)
        )

        layout = qtw.QFormLayout()
        layout.addRow(qtw.QLabel("Weekday"), self.week_day_field)
        self.setLayout(layout)
