import datetime

from PyQt5 import QtCore as qtc, QtWidgets as qtw

from src import domain
from src.presentation.shared.widgets import table

__all__ = ("UserDash",)

from src.presentation.user.dash.state import UserDashState


class UserDash(qtw.QWidget):
    delete_btn_clicked = qtc.pyqtSignal(domain.User)
    edit_btn_clicked = qtc.pyqtSignal(domain.User)

    def __init__(self):
        super().__init__()

        self.refresh_btn = qtw.QPushButton("Refresh")
        self.refresh_btn.setFixedWidth(100)

        self.add_btn = qtw.QPushButton("Add")
        self.add_btn.setFixedWidth(100)

        toolbar = qtw.QHBoxLayout()
        toolbar.addWidget(self.refresh_btn)
        toolbar.addWidget(self.add_btn)
        toolbar.addSpacerItem(qtw.QSpacerItem(0, 0, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum))

        self._table: table.Table[domain.User, str] = table.Table(
            col_specs=[
                table.text_col(
                    display_name="ID",
                    attr_name="user_id",
                    hidden=True,
                ),
                table.text_col(
                    display_name="Username",
                    attr_name="username",
                    column_width=200,
                ),
                table.text_col(
                    display_name="Name",
                    attr_name="display_name",
                    column_width=200,
                ),
                table.timestamp_col(
                    display_name="Added",
                    attr_name="date_added",
                ),
                table.timestamp_col(
                    display_name="Updated",
                    attr_name="date_updated",
                ),
                table.button_col(
                    button_text="Edit",
                    on_click=self.edit_btn_clicked.emit,
                    column_width=100,
                    enable_when=lambda user: user.is_admin,
                ),
                table.button_col(
                    button_text="Delete",
                    on_click=self.delete_btn_clicked.emit,
                    column_width=100,
                    enable_when=lambda user: user.is_admin,
                ),
            ],
            key_attr="user_id",
        )

        self._status_bar = qtw.QStatusBar()

        layout = qtw.QVBoxLayout()
        layout.addLayout(toolbar)
        layout.addWidget(self._table)
        layout.addWidget(self._status_bar)

        self.setLayout(layout)

        self._current_user = domain.DEFAULT_USER

    def get_state(self) -> UserDashState:
        return UserDashState(
            users=self._table.items,
            current_user=self._current_user,
            status=self._status_bar.currentMessage(),
        )

    def set_state(self, *, state: UserDashState) -> None:
        self._table.set_all(state.users)
        self._current_user = state.current_user
        self._status_bar.showMessage(state.status)
