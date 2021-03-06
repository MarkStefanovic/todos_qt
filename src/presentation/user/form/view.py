from __future__ import annotations

import datetime

from PyQt5 import QtCore as qtc, QtWidgets as qtw

from src.presentation.shared import fonts, icons
from src.presentation.user.form.state import UserFormState

import qtawesome as qta

__all__ = ("UserForm",)


class UserForm(qtw.QWidget):
    def __init__(self, *, parent: qtw.QWidget | None = None):
        super().__init__(parent=parent)

        back_btn_icon = qta.icon(icons.back_btn_icon_name, color=self.parent().palette().text().color())
        self.back_btn = qtw.QPushButton(back_btn_icon, "Back")
        self.back_btn.setMaximumWidth(100)

        display_name_lbl = qtw.QLabel("Name")
        display_name_lbl.setFont(fonts.bold)
        self._display_name_txt = qtw.QLineEdit()
        self._display_name_txt.setMaximumWidth(400)

        username_lbl = qtw.QLabel("Username")
        username_lbl.setFont(fonts.bold)
        self._username_txt = qtw.QLineEdit()
        self._username_txt.setMaximumWidth(400)

        form_layout = qtw.QFormLayout()
        form_layout.addRow(display_name_lbl, self._display_name_txt)
        form_layout.addRow(username_lbl, self._username_txt)

        save_btn_icon = qta.icon(icons.save_btn_icon_name, color=self.parent().palette().text().color())
        self.save_btn = qtw.QPushButton(save_btn_icon, "Save")
        self.save_btn.setMaximumWidth(100)

        layout = qtw.QVBoxLayout()
        layout.addWidget(self.back_btn, alignment=qtc.Qt.AlignLeft)
        layout.addLayout(form_layout)
        layout.addWidget(self.save_btn, alignment=qtc.Qt.AlignRight)

        self.setLayout(layout)

        self._user_id = ""
        self._is_admin = False
        self._date_added = datetime.datetime.now()
        self._date_updated: datetime.datetime | None = None

    def get_state(self) -> UserFormState:
        return UserFormState(
            user_id=self._user_id,
            username=self._username_txt.text(),
            display_name=self._display_name_txt.text(),
            is_admin=self._is_admin,
            date_added=self._date_added,
            date_updated=self._date_updated,
        )

    def set_state(self, *, state: UserFormState) -> None:
        self._user_id = state.user_id
        self._is_admin = state.is_admin
        self._date_added = state.date_added
        self._date_updated = state.date_updated
        self._username_txt.setText(state.username)
        self._display_name_txt.setText(state.display_name)
