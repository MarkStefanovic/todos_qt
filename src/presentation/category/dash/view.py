from __future__ import annotations

import typing

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa
from loguru import logger

from src import domain
from src.presentation.category.dash import requests
from src.presentation.category.dash.state import CategoryDashState
from src.presentation.shared import icons, font
from src.presentation.shared.widgets import table_view, StatusBar, popup

__all__ = ("CategoryDash",)


class CategoryDash(qtw.QWidget):
    def __init__(
        self,
        *,
        dash_requests: requests.CategoryDashRequests,
        current_user: domain.User,
        parent: qtw.QWidget | None,
    ):
        super().__init__(parent=parent)

        self._dash_requests: typing.Final[requests.CategoryDashRequests] = dash_requests
        self._current_user: typing.Final[domain.User] = current_user

        refresh_btn_icon = icons.refresh_btn_icon(parent=self)
        self._refresh_btn = qtw.QPushButton(refresh_btn_icon, "Refresh")
        self._refresh_btn.setMaximumWidth(100)

        add_btn_icon = icons.add_btn_icon(parent=self)
        self._add_btn = qtw.QPushButton(add_btn_icon, "Add")
        self._add_btn.setMaximumWidth(100)

        toolbar_layout = qtw.QHBoxLayout()
        toolbar_layout.addWidget(self._refresh_btn)
        toolbar_layout.addWidget(self._add_btn)
        toolbar_layout.addStretch()

        self._table_view: table_view.TableView[domain.Category, str] = table_view.TableView(
            attrs=(
                table_view.text(
                    name="category_id",
                    display_name="ID",
                    key=True,
                ),
                table_view.text(
                    display_name="Name",
                    name="name",
                    width=200,
                ),
                table_view.text(
                    display_name="Note",
                    name="note",
                    width=400,
                    rich_text=True,
                ),
                table_view.date(
                    name="date_added",
                    display_name="Added",
                ),
                table_view.date(
                    name="date_updated",
                    display_name="Updated",
                ),
                table_view.button(
                    name="edit",
                    button_text="Edit",
                    width=font.BOLD_FONT_METRICS.width(" Edit "),
                    enabled_when=lambda category: domain.permissions.user_can_edit_category(
                        user=self._current_user,
                        category=category,
                    ),
                ),
                table_view.button(
                    name="delete",
                    button_text="Delete",
                    width=font.BOLD_FONT_METRICS.width(" Delete "),
                    enabled_when=lambda category: domain.permissions.user_can_edit_category(
                        user=self._current_user,
                        category=category,
                    ),
                ),
            ),
            parent=self,
        )

        self._status_bar = StatusBar(parent=self)

        layout = qtw.QVBoxLayout()
        layout.addLayout(toolbar_layout)
        layout.addWidget(self._table_view)
        layout.addWidget(self._status_bar)
        self.setLayout(layout)

        self._table_view.button_clicked.connect(self._on_button_clicked)
        self._table_view.double_click.connect(self._on_double_click)
        # noinspection PyUnresolvedReferences
        self._add_btn.clicked.connect(self._on_add_btn_clicked)
        # noinspection PyUnresolvedReferences
        self._refresh_btn.clicked.connect(self._on_refresh_btn_clicked)

    def get_state(self) -> CategoryDashState | domain.Error:
        return CategoryDashState(
            categories=self._table_view.items,
            selected_category=self._table_view.selected_item or domain.Unspecified(),
            status=self._status_bar.currentMessage(),
        )

    def refresh(self) -> None:
        logger.debug(f"{self.__class__.__name__}.refresh()")

        self._dash_requests.refresh.emit()

    def set_state(self, /, state: CategoryDashState) -> None:
        if not isinstance(state.categories, domain.Unspecified):
            self._table_view.set_items(state.categories)

        if not isinstance(state.selected_category, domain.Unspecified):
            if state.selected_category is None:
                self._table_view.clear_selection()
            else:
                self._table_view.select_item_by_key(state.selected_category.category_id)

        if not isinstance(state.status, domain.Unspecified):
            self._status_bar.set_status(state.status)

        if not isinstance(state.category_added, domain.Unspecified):
            self._table_view.add_item(state.category_added)

        if not isinstance(state.category_deleted, domain.Unspecified):
            self._table_view.delete_item(key=state.category_deleted.category_id)

        if not isinstance(state.category_edited, domain.Unspecified):
            self._table_view.update_item(state.category_edited)

    def _on_add_btn_clicked(self, /, _: bool) -> None:
        logger.debug(f"{self.__class__.__name__}._on_add_btn_clicked()")

        self._dash_requests.add.emit()

    def _on_button_clicked(
        self,
        /,
        event: table_view.ButtonClickedEvent[domain.Category, str],
    ) -> None:
        logger.debug(f"{self.__class__.__name__}._on_button_clicked({event=!r})")

        match event.attr.name:
            case "delete":
                if domain.permissions.user_can_edit_category(
                    user=self._current_user,
                    category=event.item,
                ):
                    if popup.confirm(question=f"Are you sure you want to delete {event.item.name}?"):
                        self._dash_requests.delete.emit(requests.Delete(category=event.item))
            case "edit":
                if domain.permissions.user_can_edit_category(
                    user=self._current_user,
                    category=event.item,
                ):
                    self._dash_requests.edit.emit(requests.Edit(category=event.item))
            case _:
                logger.error(f"attr name, {event.attr.name!r}, not recognized.")

    def _on_double_click(
        self,
        /,
        event: table_view.DoubleClickEvent[domain.Category, str],
    ) -> None:
        if domain.permissions.user_can_edit_category(
            user=self._current_user,
            category=self._table_view.selected_item,
        ):
            self._dash_requests.edit.emit(requests.Edit(category=event.item))

    def _on_refresh_btn_clicked(self, /, _: bool) -> None:
        logger.debug(f"{self.__class__.__name__}._on_refresh_btn_clicked()")

        self._dash_requests.refresh.emit()
