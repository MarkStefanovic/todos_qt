from __future__ import annotations

import datetime

# noinspection PyPep8Naming
from PyQt5 import QtCore as qtc, QtWidgets as qtw
from loguru import logger

from src import domain
from src.presentation.category.form import requests
from src.presentation.category.form.state import CategoryFormState
from src.presentation.shared import fonts, icons

import qtawesome as qta

__all__ = ("CategoryForm",)


class CategoryForm(qtw.QWidget, domain.View[CategoryFormState]):
    def __init__(
        self,
        *,
        form_requests: requests.CategoryFormRequests,
        parent: qtw.QWidget | None = None,
    ):
        super().__init__(parent=parent)

        self._form_requests = form_requests

        back_btn_icon = qta.icon(
            icons.back_btn_icon_name,
            color=self.parent().palette().text().color(),
        )
        self.back_btn = qtw.QPushButton(back_btn_icon, "Back")
        self.back_btn.setFont(fonts.BOLD)
        self.back_btn.setMaximumWidth(100)

        name_lbl = qtw.QLabel("Name")
        name_lbl.setFont(fonts.BOLD)
        self._name_txt = qtw.QLineEdit()
        self._name_txt.setMaximumWidth(400)

        note_lbl = qtw.QLabel("Note")
        note_lbl.setFont(fonts.BOLD)
        self._note_txt = qtw.QTextEdit()

        form_layout = qtw.QFormLayout()
        form_layout.addRow(name_lbl, self._name_txt)
        form_layout.addRow(note_lbl, self._note_txt)

        self._category_id: str = ""
        self._date_added: datetime.datetime = datetime.datetime.now()
        self._date_updated: datetime.datetime | None = None

        save_btn_icon = qta.icon(
            icons.save_btn_icon_name,
            color=self.parent().palette().text().color(),
        )
        self.save_btn = qtw.QPushButton(save_btn_icon, "Save")
        self.save_btn.setFont(fonts.BOLD)
        self.save_btn.setFixedWidth(100)

        layout = qtw.QVBoxLayout()
        layout.addWidget(self.back_btn, alignment=qtc.Qt.AlignLeft)
        layout.addLayout(form_layout)
        layout.addWidget(self.save_btn, alignment=qtc.Qt.AlignRight)

        self.setLayout(layout)

        # noinspection PyUnresolvedReferences
        self.back_btn.clicked.connect(self._on_back_btn_clicked)
        # noinspection PyUnresolvedReferences
        self.save_btn.clicked.connect(self._on_save_btn_clicked)

    def get_state(self) -> CategoryFormState:
        return CategoryFormState(
            category_id=self._category_id,
            name=self._name_txt.text(),
            note=self._note_txt.toPlainText(),
            date_added=self._date_added,
            date_updated=self._date_updated,
        )

    def save(self) -> None:
        return self.save()

    def set_state(self, /, state: CategoryFormState) -> None:
        self._category_id = state.category_id
        self._name_txt.setText(state.name)
        self._note_txt.setText(state.note)
        self._date_added = state.date_added
        self._date_updated = state.date_updated

    def _on_back_btn_clicked(self, /, _: bool) -> None:
        logger.debug(f"{self.__class__.__name__}._on_back_btn_clicked()")

        self._form_requests.back.emit()

    def _on_save_btn_clicked(self, /, _: bool) -> None:
        logger.debug(f"{self.__class__.__name__}._on_save_btn_clicked()")

        category = domain.Category(
            category_id=self._category_id,
            name=self._name_txt.text(),
            note=self._note_txt.toPlainText(),
            date_added=self._date_added,
            date_updated=self._date_updated,
            date_deleted=None,
        )

        request = requests.Save(category=category)

        self._form_requests.save.emit(request)
