import datetime

from PyQt5 import QtCore as qtc, QtWidgets as qtw
import qtawesome as qta

from src.presentation.category.form.state import CategoryFormState
from src.presentation.shared import fonts

__all__ = ("CategoryForm",)


class CategoryForm(qtw.QWidget):
    def __init__(self, *, parent: qtw.QWidget | None = None):
        super().__init__(parent=parent)

        back_btn_icon = qta.icon("ei.arrow-left")
        self.back_btn = qtw.QPushButton(back_btn_icon, "Back")
        self.back_btn.setFont(fonts.bold)
        self.back_btn.setMaximumWidth(100)

        name_lbl = qtw.QLabel("Name")
        name_lbl.setFont(fonts.bold)
        self._name_txt = qtw.QLineEdit()
        self._name_txt.setMaximumWidth(400)

        note_lbl = qtw.QLabel("Note")
        note_lbl.setFont(fonts.bold)
        self._note_txt = qtw.QTextEdit()

        form_layout = qtw.QFormLayout()
        form_layout.addRow(name_lbl, self._name_txt)
        form_layout.addRow(note_lbl, self._note_txt)

        self._category_id: str = ""
        self._date_added: datetime.datetime = datetime.datetime.now()
        self._date_updated: datetime.datetime | None = None

        save_btn_icon = qta.icon("fa5.save")
        self.save_btn = qtw.QPushButton(save_btn_icon, "Save")
        self.save_btn.setFont(fonts.bold)
        self.save_btn.setFixedWidth(100)

        layout = qtw.QVBoxLayout()
        layout.addWidget(self.back_btn, alignment=qtc.Qt.AlignLeft)
        layout.addLayout(form_layout)
        layout.addWidget(self.save_btn, alignment=qtc.Qt.AlignRight)

        self.setLayout(layout)

    def get_state(self) -> CategoryFormState:
        return CategoryFormState(
            category_id=self._category_id,
            name=self._name_txt.text(),
            note=self._note_txt.toPlainText(),
            date_added=self._date_added,
            date_updated=self._date_updated,
        )

    def set_state(self, *, state: CategoryFormState) -> None:
        self._name_txt.setText(state.name)
        self._note_txt.setText(state.note)
        self._category_id = state.category_id
        self._date_added = state.date_added
        self._date_updated = state.date_updated
