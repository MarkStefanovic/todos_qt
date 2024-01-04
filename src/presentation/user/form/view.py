import datetime
import typing

# noinspection PyPep8Naming
from PyQt6 import QtCore as qtc, QtWidgets as qtw
from loguru import logger

from src import domain
from src.presentation.shared.theme import font, icons
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
        self._back_btn = qtw.QPushButton(back_btn_icon, "")
        self._back_btn.setFixedWidth(font.BOLD_FONT_METRICS.height() + 8)

        display_name_lbl = qtw.QLabel("Display Name")
        display_name_lbl.setFont(font.BOLD_FONT)
        self._display_name_txt = qtw.QLineEdit()
        self._display_name_txt.setMaximumWidth(font.DEFAULT_FONT_METRICS.boundingRect("  Display Name  ").width())

        username_lbl = qtw.QLabel("Username")
        username_lbl.setFont(font.BOLD_FONT)
        self._username_txt = qtw.QLineEdit()
        self._username_txt.setMaximumWidth(self._display_name_txt.maximumWidth())

        save_btn_icon = icons.save_btn_icon(parent=self)
        self._save_btn = qtw.QPushButton(save_btn_icon, "")
        self._save_btn.setFixedWidth(font.BOLD_FONT_METRICS.height() + 8)

        layout = qtw.QGridLayout()
        layout.addWidget(self._back_btn, 0, 0, alignment=qtc.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(display_name_lbl, 1, 0)
        layout.addWidget(self._display_name_txt, 1, 1)
        layout.addWidget(username_lbl, 2, 0)
        layout.addWidget(self._username_txt, 2, 1)
        layout.addWidget(self._save_btn, 3, 1, alignment=qtc.Qt.AlignmentFlag.AlignRight)
        layout.addItem(qtw.QSpacerItem(0, 0, qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Expanding), 4, 2)
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
