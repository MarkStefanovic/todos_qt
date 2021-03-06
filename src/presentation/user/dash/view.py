from __future__ import annotations

from PyQt5 import QtCore as qtc, QtWidgets as qtw

from src import domain
from src.presentation.shared import fonts, icons
from src.presentation.shared.widgets import table
from src.presentation.user.dash.state import UserDashState

import qtawesome as qta

__all__ = ("UserDash",)


class UserDash(qtw.QWidget):
    delete_btn_clicked = qtc.pyqtSignal()
    edit_btn_clicked = qtc.pyqtSignal()

    def __init__(self, *, parent: qtw.QWidget | None = None):
        super().__init__(parent=parent)

        self._current_user = domain.DEFAULT_USER

        refresh_btn_icon = qta.icon(icons.refresh_btn_icon_name, color=self.parent().palette().text().color())
        self.refresh_btn = qtw.QPushButton(refresh_btn_icon, "Refresh")
        self.refresh_btn.setFont(fonts.bold)
        self.refresh_btn.setMaximumWidth(100)

        add_btn_icon = qta.icon(icons.add_btn_icon_name, color=self.parent().palette().text().color())
        self.add_btn = qtw.QPushButton(add_btn_icon, "Add")
        self.add_btn.setFont(fonts.bold)
        self.add_btn.setMaximumWidth(100)

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
                    display_format="%m/%d/%y",
                    column_width=100,
                    alignment=table.ColAlignment.Center,
                ),
                table.timestamp_col(
                    display_name="Updated",
                    attr_name="date_updated",
                    display_format="%m/%d/%y",
                    column_width=100,
                    alignment=table.ColAlignment.Center,
                ),
                table.button_col(
                    button_text="Edit",
                    on_click=lambda _: self.edit_btn_clicked.emit(),  # noqa
                    column_width=60,
                    enable_when=lambda user: domain.permissions.user_can_edit_user(
                        current_user=self._current_user,
                        user=user,
                    ),
                ),
                table.button_col(
                    button_text="Delete",
                    on_click=lambda _: self.delete_btn_clicked.emit(),  # noqa
                    column_width=80,
                    enable_when=lambda user: domain.permissions.user_can_edit_user(
                        current_user=self._current_user,
                        user=user,
                    ),
                ),
            ],
            key_attr="user_id",
        )
        self._table.double_click.connect(
            lambda: self.edit_btn_clicked.emit() if domain.permissions.user_can_edit_user(  # noqa
                current_user=self._current_user,
                user=self._table.selected_item,
            ) else None
        )

        self._status_bar = qtw.QStatusBar()

        layout = qtw.QVBoxLayout()
        layout.addLayout(toolbar)
        layout.addWidget(self._table)
        layout.addWidget(self._status_bar)

        self.setLayout(layout)

    def get_state(self) -> UserDashState:
        return UserDashState(
            users=self._table.items,
            current_user=self._current_user,
            selected_user=self._table.selected_item,
            status=self._status_bar.currentMessage(),
        )

    def set_state(self, *, state: UserDashState) -> None:
        self._current_user = state.current_user
        self._table.set_all(state.users)
        if user := state.selected_user:
            self._table.select_item_by_key(key=user.user_id)
        self._status_bar.showMessage(state.status)
