import datetime
import typing


# noinspection PyPep8Naming
from PyQt5 import QtCore as qtc, QtWidgets as qtw
from loguru import logger

from src import domain
from src.presentation.shared import fonts, icons
from src.presentation.user.form import requests
from src.presentation.user.form.state import UserFormState

__all__ = ("UserForm",)


class UserForm(qtw.QWidget):
    def __init__(
        self,
        *,
        form_requests: requests.UserFormRequests,
        parent: qtw.QWidget | None = None,
    ):
        super().__init__(parent=parent)

        self._requests: typing.Final[requests.UserFormRequests] = form_requests

        back_btn_icon = icons.back_btn_icon(parent=self)
        self._back_btn = qtw.QPushButton(back_btn_icon, "Back")
        self._back_btn.setMaximumWidth(100)

        display_name_lbl = qtw.QLabel("Name")
        display_name_lbl.setFont(fonts.BOLD)
        self._display_name_txt = qtw.QLineEdit()
        self._display_name_txt.setMaximumWidth(400)

        username_lbl = qtw.QLabel("Username")
        username_lbl.setFont(fonts.BOLD)
        self._username_txt = qtw.QLineEdit()
        self._username_txt.setMaximumWidth(400)

        form_layout = qtw.QFormLayout()
        form_layout.addRow(display_name_lbl, self._display_name_txt)
        form_layout.addRow(username_lbl, self._username_txt)

        save_btn_icon = icons.save_btn_icon(parent=self)
        self._save_btn = qtw.QPushButton(save_btn_icon, "Save")
        self._save_btn.setMaximumWidth(100)

        layout = qtw.QVBoxLayout()
        layout.addWidget(self._back_btn, alignment=qtc.Qt.AlignLeft)
        layout.addLayout(form_layout)
        layout.addWidget(self._save_btn, alignment=qtc.Qt.AlignRight)

        self.setLayout(layout)

        self._user_id = ""
        self._is_admin = False
        self._date_added = datetime.datetime.now()
        self._date_updated: datetime.datetime | None = None

        # noinspection PyUnresolvedReferences
        self._back_btn.clicked.connect(self._on_back_btn_clicked)
        # noinspection PyUnresolvedReferences
        self._save_btn.clicked.connect(self._on_save_btn_clicked)

    def get_state(self) -> UserFormState:
        return UserFormState(
            user_id=self._user_id,
            username=self._username_txt.text(),
            display_name=self._display_name_txt.text(),
            is_admin=self._is_admin,
            date_added=self._date_added,
            date_updated=self._date_updated,
        )

    def save(self) -> None:
        self._save_btn.click()

    def set_state(self, *, state: UserFormState) -> None:
        if not isinstance(state.user_id, domain.Unspecified):
            self._user_id = state.user_id
        if not isinstance(state.username, domain.Unspecified):
            self._username_txt.setText(state.username)
        if not isinstance(state.display_name, domain.Unspecified):
            self._display_name_txt.setText(state.display_name)
        if not isinstance(state.is_admin, domain.Unspecified):
            self._is_admin = state.is_admin
        if not isinstance(state.date_added, domain.Unspecified):
            self._date_added = state.date_added
        if not isinstance(state.date_updated, domain.Unspecified):
            self._date_updated = state.date_updated

    def _on_back_btn_clicked(self) -> None:
        logger.debug(f"{self.__class__.__name__}._on_back_btn_clicked()")

        self._requests.back.emit()

    def _on_save_btn_clicked(self) -> None:
        logger.debug(f"{self.__class__.__name__}._on_save_btn_clicked()")

        user = domain.User(
            user_id=self._user_id,
            username=self._username_txt.text(),
            display_name=self._display_name_txt.text(),
            is_admin=self._is_admin,
            date_added=self._date_added,
            date_updated=self._date_updated,
        )

        request = requests.SaveRequest(user=user)

        self._requests.save.emit(request)
