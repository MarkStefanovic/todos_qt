import qdarkgraystyle
from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw, sip

from src import domain
from src.presentation import widgets
from src.presentation.todo.todo_edit_form import (
    edit_form_model,
)
from src.presentation.todo.todo_edit_form.todo_edit_form_bodies import (
    once_todo_form_body,
    yearly_todo_form_body,
    x_days_form_body,
    irregular_todo_form_body,
    monthly_todo_form_body,
    weekly_todo_form_body,
)

__all__ = ("EditFormBase",)


class EditFormBase(qtw.QDialog):
    def __init__(self, /, model: edit_form_model.TodoEditFormModel):
        super().__init__()

        self._model = model

        if self._model.edit_mode == domain.EditMode.ADD:
            self.setWindowTitle("Add New Todo")
        else:
            self.setWindowTitle("Edit Todo")

        # self.setGeometry(qtc.QRect(100, 100, 400, 200))
        self.setStyleSheet(qdarkgraystyle.load_stylesheet())

        # FORM
        self.form_group = qtw.QGroupBox()
        self.frequency = qtw.QComboBox()
        self.frequency.addItems(model.frequency_options)
        self.frequency.setCurrentText(self._model.frequency)
        # self.frequency.currentTextChanged.connect(self._model.set_frequency)
        self.frequency.currentIndexChanged.connect(self.set_form_body)

        self.description = widgets.ValidatedTextWidget(
            field_name="description",
            initial_value=self._model.description,
            min_length=1,
            max_length=200,
        )
        self.description.textChanged.connect(self._model.set_description)
        # self.description.editingFinished.connect(lambda: print("editing finished"))

        self.advance_days = qtw.QSpinBox()
        self.advance_days.setRange(1, 999)
        self.advance_days.setValue(self._model.advance_days)
        self.advance_days.valueChanged.connect(self._model.set_advance_days)

        self.note = qtw.QTextEdit()
        self.note.setText(self._model.note)
        self.note.textChanged.connect(self._model.set_note)

        layout = qtw.QFormLayout()
        layout.addRow(qtw.QLabel("Frequency"), self.frequency)
        layout.addRow(qtw.QLabel("Description"), self.description)
        layout.addRow(qtw.QLabel("Notice"), self.advance_days)
        layout.addRow(qtw.QLabel("Note"), self.note)
        self.form_group.setLayout(layout)

        # BUTTON BAR
        self.button_box = qtw.QDialogButtonBox(  # type: ignore
            qtw.QDialogButtonBox.Save | qtw.QDialogButtonBox.Close
        )
        self.button_box.accepted.connect(self.save)
        self.button_box.rejected.connect(self.close)
        button_row = qtw.QHBoxLayout()
        spacer = qtw.QSpacerItem(20, 40, qtw.QSizePolicy.Expanding)
        button_row.addItem(spacer)
        button_row.addWidget(self.button_box)

        self.form_body = create_form_body(
            model=self._model, frequency=self._model.frequency
        )

        main_layout = qtw.QVBoxLayout()
        main_layout.addWidget(self.form_group)
        main_layout.addWidget(self.form_body)
        main_layout.addLayout(button_row)

        self.setLayout(main_layout)

    def save(self) -> None:
        self._model.save()
        self.close()

    def set_form_body(self, /, _: int) -> None:
        frequency = self.frequency.currentText()
        new_form = create_form_body(model=self._model, frequency=frequency)
        self.layout().replaceWidget(self.form_body, new_form)
        sip.delete(self.form_body)
        self.form_body = new_form

    def load_state(self, todo: domain.Todo) -> None:
        self.frequency.findText(todo.frequency.db_name())
        self.advance_days.setText(str(todo.advance_days))
        self.description.setText(self._model.description)
        self.note.setText(todo.note)


def create_form_body(
    model: edit_form_model.TodoEditFormModel, frequency: str
) -> qtw.QGroupBox:
    print(f"{frequency=}")
    if frequency == "daily":
        new_form = qtw.QGroupBox()
        new_form.setStyleSheet("border: 0;")
        return new_form
    elif frequency == "irregular":
        return irregular_todo_form_body.IrregularTodoForm(model)
    elif frequency == "monthly":
        return monthly_todo_form_body.MonthlyTodoForm(model)
    elif frequency == "once":
        return once_todo_form_body.OnceTodoForm(model)
    elif frequency == "weekly":
        return weekly_todo_form_body.WeeklyTodoForm(model)
    elif frequency == "xdays":
        return x_days_form_body.XDaysForm(model)
    elif frequency == "yearly":
        return yearly_todo_form_body.YearlyTodoForm(model)
    else:
        raise ValueError(f"Unrecognized frequency: {frequency}")
