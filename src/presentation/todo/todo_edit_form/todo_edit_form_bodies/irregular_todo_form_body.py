from PyQt5 import QtWidgets as qtw

from src import domain
from src.presentation.todo.todo_edit_form import edit_form_model

__all__ = ("IrregularTodoForm",)


class IrregularTodoForm(qtw.QGroupBox):
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

        self.week_number_field = qtw.QSpinBox()
        self.week_number_field.setRange(1, 5)
        self.week_number_field.setValue((self._model.week_number or 1) - 1)
        self.week_number_field.valueChanged.connect(
            lambda wk: self._model.set_week_number(wk - 1)
        )

        self.week_day_field = qtw.QComboBox()
        for w in domain.Weekday:  # type: ignore
            self.week_day_field.addItem(str(w), w.value)
        self.week_day_field.setCurrentIndex((self._model.week_day or 1) - 1)
        self.week_day_field.currentIndexChanged.connect(
            lambda wd: self._model.set_week_day(wd - 1)
        )

        layout = qtw.QFormLayout()
        layout.addRow(qtw.QLabel("Month"), self.month_field)
        layout.addRow(qtw.QLabel("Week"), self.week_number_field)
        layout.addRow(qtw.QLabel("Weekday"), self.week_day_field)
        self.setLayout(layout)
