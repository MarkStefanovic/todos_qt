# noinspection PyPep8Naming
from PyQt5 import QtWidgets as qtw

from src import domain
from src.presentation.shared import fonts, icons
from src.presentation.shared.widgets import table_view
from src.presentation.user.dash import requests
from src.presentation.user.dash.state import UserDashState

import qtawesome as qta

__all__ = ("UserDash",)


class UserDash(qtw.QWidget):
    def __init__(
        self,
        *,
        user_requests: requests.UserDashRequests,
        parent: qtw.QWidget | None = None,
    ):
        super().__init__(parent=parent)

        self._current_user = domain.DEFAULT_USER

        refresh_btn_icon = icons.refresh_btn_icon(parent=self)
        self.refresh_btn = qtw.QPushButton(refresh_btn_icon, "Refresh")
        self.refresh_btn.setFont(fonts.BOLD)
        self.refresh_btn.setMaximumWidth(100)

        add_btn_icon = qta.icon(icons.add_btn_icon_name, color=self.parent().palette().text().color())  # type: ignore
        self.add_btn = qtw.QPushButton(add_btn_icon, "Add")
        self.add_btn.setFont(fonts.BOLD)
        self.add_btn.setMaximumWidth(100)

        toolbar = qtw.QHBoxLayout()
        toolbar.addWidget(self.refresh_btn)
        toolbar.addWidget(self.add_btn)
        toolbar.addSpacerItem(qtw.QSpacerItem(0, 0, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum))

        self._table: table_view.TableView[domain.User, str] = table_view.TableView(
            attrs=(
                table_view.text(
                    name="user_id",
                    display_name="ID",
                    key=True,
                ),
                table_view.text(
                    name="username",
                    display_name="Username",
                    width=200,
                ),
                table_view.text(
                    name="display_name",
                    display_name="Name",
                    width=200,
                ),
                table_view.timestamp(
                    name="date_added",
                    display_name="Added",
                ),
                table_view.timestamp(
                    name="date_updated",
                    display_name="Updated",
                    width=100,
                ),
                table_view.button(
                    name="edit",
                    button_text="Edit",
                    width=60,
                    enabled_selector=lambda user: domain.permissions.user_can_edit_user(
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
            ),
            parent=self,
        )

        self._table.button_clicked.connect(self._on_table_btn_clicked)

        self._table.double_click.connect(
            lambda: self.edit_btn_clicked.emit()
            if domain.permissions.user_can_edit_user(  # noqa
                current_user=self._current_user,
                user=self._table.selected_item,
            )
            else None
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
