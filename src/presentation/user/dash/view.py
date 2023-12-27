import typing

# noinspection PyPep8Naming
from PyQt6 import QtWidgets as qtw
from loguru import logger

from src import domain
from src.presentation.shared import widgets
from src.presentation.shared.theme import font, icons
from src.presentation.shared.widgets import table_view, popup
from src.presentation.user.dash import requests
from src.presentation.user.dash.state import UserDashState


__all__ = ("UserDash",)


class UserDash(qtw.QWidget):
    def __init__(
        self,
        *,
        current_user: domain.User,
        user_requests: requests.UserDashRequests,
        parent: qtw.QWidget | None = None,
    ):
        super().__init__(parent=parent)

        self._current_user: typing.Final[domain.User] = current_user
        self._requests: typing.Final[requests.UserDashRequests] = user_requests

        refresh_btn_icon = icons.refresh_btn_icon(parent=self)
        self._refresh_btn = qtw.QPushButton(refresh_btn_icon, "")
        self._refresh_btn.setFixedWidth(font.BOLD_FONT_METRICS.height() + 8)
        self._refresh_btn.setToolTip("Refresh")

        toolbar = qtw.QHBoxLayout()
        toolbar.addWidget(self._refresh_btn)

        if self._current_user.is_admin:
            add_btn_icon = icons.add_btn_icon(parent=self)
            self._add_btn = qtw.QPushButton(add_btn_icon, "")
            self._add_btn.setFixedWidth(font.BOLD_FONT_METRICS.height() + 8)
            self._add_btn.setToolTip("Add New User")
            toolbar.addWidget(self._add_btn)

            # noinspection PyUnresolvedReferences
            self._add_btn.clicked.connect(self._on_add_btn_clicked)

        toolbar.addStretch()

        attrs: tuple[table_view.Attr[domain.User, typing.Any], ...] = (
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
                display_name="Display Name",
                width=200,
            ),
            table_view.timestamp(
                name="date_added",
                display_name="Added",
                width=100,
            ),
            table_view.timestamp(
                name="date_updated",
                display_name="Updated",
                width=100,
            ),
        )

        if self._current_user.is_admin:
            attrs += (
                table_view.button(
                    name="edit",
                    button_text="",
                    icon=icons.edit_btn_icon(parent=self),
                    width=40,
                    enabled_when=lambda _: self._current_user.is_admin,
                ),
                table_view.button(
                    name="delete",
                    button_text="",
                    icon=icons.delete_btn_icon(parent=self),
                    width=40,
                    enabled_when=lambda _: self._current_user.is_admin,
                ),
            )

        self._table_view: table_view.TableView[domain.User, str] = table_view.TableView(
            attrs=attrs,
            parent=self,
        )

        self._status_bar = widgets.StatusBar(parent=self)

        layout = qtw.QVBoxLayout()
        layout.addLayout(toolbar)
        layout.addWidget(self._table_view)
        layout.addWidget(self._status_bar)
        self.setLayout(layout)

        # noinspection PyUnresolvedReferences
        self._refresh_btn.clicked.connect(self._on_refresh_btn_clicked)
        self._table_view.button_clicked.connect(self._on_table_btn_clicked)
        if self._current_user.is_admin:
            self._table_view.double_click.connect(self._on_table_btn_double_clicked)

    def get_state(self) -> UserDashState:
        return UserDashState(
            users=self._table_view.items,
            selected_user=self._table_view.selected_item,
            status=self._status_bar.currentMessage(),
        )

    def refresh(self) -> None:
        self._refresh_btn.click()

    def set_state(self, /, state: UserDashState) -> None:
        if not isinstance(state.users, domain.Unspecified):
            self._table_view.set_items(state.users)

        if not isinstance(state.status, domain.Unspecified):
            self._status_bar.set_status(state.status)

        if not isinstance(state.selected_user, domain.Unspecified):
            if state.selected_user is not None:
                self._table_view.select_item_by_key(state.selected_user.user_id)

        if state.user_added:
            self._table_view.add_item(state.user_added)

        if state.user_deleted:
            self._table_view.delete_item(key=state.user_deleted.user_id)

        if state.user_updated:
            self._table_view.update_item(state.user_updated)

    def _on_add_btn_clicked(self, /, _: bool) -> None:
        logger.debug(f"{self.__class__.__name__}._on_add_btn_clicked()")

        if self._current_user.is_admin:
            self._requests.add.emit()

    def _on_refresh_btn_clicked(self, /, _: bool) -> None:
        self._requests.refresh.emit()

    def _on_table_btn_clicked(
        self, /, event: table_view.ButtonClickedEvent[domain.User, str]
    ) -> None:
        logger.debug(f"{self.__class__.__name__}._on_table_btn_clicked({event=!r})")

        match event.attr.name:
            case "delete":
                if self._current_user.is_admin:
                    if popup.confirm(
                        question=f"Are you sure you want to delete {event.item.display_name}?",
                        title="Confirm Delete",
                    ):
                        self._requests.delete.emit(requests.DeleteRequest(user=event.item))
            case "edit":
                if self._current_user.is_admin:
                    self._requests.edit.emit(requests.EditRequest(user=event.item))
            case _:
                logger.error(
                    f"{self.__class__.__name__}._on_table_btn_clicked({event=!r}): unrecognized button attr name, "
                    f"{event.attr.name}"
                )

    def _on_table_btn_double_clicked(
        self, /, event: table_view.DoubleClickEvent[domain.User, str]
    ) -> None:
        logger.debug(f"{self.__class__.__name__}._on_table_btn_double_clicked({event=!r})")

        if self._current_user.is_admin:
            request = requests.EditRequest(user=event.item)
            self._requests.edit.emit(request)
