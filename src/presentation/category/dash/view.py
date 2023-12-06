from __future__ import annotations


from PyQt5 import QtCore as qtc, QtWidgets as qtw  # noqa
from loguru import logger

from src import domain
from src.presentation.category import requests
from src.presentation.category.dash.state import CategoryDashState
from src.presentation.shared import fonts, icons
from src.presentation.shared.widgets import table_view

import qtawesome as qta

__all__ = ("CategoryDash",)


class CategoryDash(qtw.QWidget):
    delete_requests = qtc.pyqtSignal(requests.DeleteCategory)
    edit_requests = qtc.pyqtSignal(requests.EditCategory)
    refresh_requests = qtc.pyqtSignal()

    def __init__(self, *, parent: qtw.QWidget | None = None):
        super().__init__(parent=parent)

        self._current_user = domain.DEFAULT_USER

        refresh_btn_icon = qta.icon(
            icons.refresh_btn_icon_name,
            color=self.parent().palette().text().color(),  # type: ignore
        )
        self.refresh_btn = qtw.QPushButton(refresh_btn_icon, "Refresh")
        self.refresh_btn.setFont(fonts.BOLD)
        self.refresh_btn.setMaximumWidth(100)
        self.refresh_btn.setDefault(True)

        add_btn_icon = qta.icon(
            icons.add_btn_icon_name,
            color=self.parent().palette().text().color(),  # type: ignore
        )
        self.add_btn = qtw.QPushButton(add_btn_icon, "Add")
        self.add_btn.setFont(fonts.BOLD)
        self.add_btn.setMaximumWidth(100)

        toolbar_layout = qtw.QHBoxLayout()
        toolbar_layout.addWidget(self.refresh_btn)
        toolbar_layout.addWidget(self.add_btn)
        toolbar_layout.addStretch()

        self.table: table_view.TableView[domain.Category, str] = table_view.TableView(
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
                    width=60,
                    enabled_selector=lambda category: domain.permissions.user_can_edit_category(
                        user=self._current_user,
                        category=category,
                    ),
                ),
                table_view.button(
                    name="delete",
                    button_text="Delete",
                    width=60,
                    enabled_selector=lambda category: domain.permissions.user_can_edit_category(
                        user=self._current_user,
                        category=category,
                    ),
                ),
            ),
            parent=self,
        )

        self._status_bar = qtw.QStatusBar()

        layout = qtw.QVBoxLayout()
        layout.addLayout(toolbar_layout)
        layout.addWidget(self.table)
        layout.addWidget(self._status_bar)
        self.setLayout(layout)

        self.table.button_clicked.connect(self._on_button_clicked)
        self.table.double_click.connect(self._on_double_click)
        # noinspection PyUnresolvedReferences
        self.refresh_btn.clicked.connect(lambda _: self.refresh_requests.emit())

    def get_state(self) -> CategoryDashState:
        return CategoryDashState(
            categories=self.table.items,
            selected_category=self.table.selected_item,
            status=self._status_bar.currentMessage(),
            current_user=self._current_user,
        )

    def refresh(self) -> None:
        self.refresh_requests.emit()

    def set_state(self, *, state: CategoryDashState) -> None:
        self._current_user = state.current_user
        self.table.set_items(state.categories)
        if state.selected_category is None:
            self.table.clear_selection()
        else:
            self.table.select_item_by_key(key=state.selected_category.category_id)
        self._status_bar.showMessage(state.status)

    def _on_button_clicked(self, /, event: table_view.ButtonClickedEvent[domain.Category, str]) -> None:
        logger.debug(f"{self.__class__.__name__}._on_button_clicked({event=!r})")

        match event.attr.name:
            case "delete":
                if domain.permissions.user_can_edit_category(
                    user=self._current_user,
                    category=event.item,
                ):
                    request = requests.DeleteCategory(category=event.item)

                    self.delete_requests.emit(request)
            case "edit":
                if domain.permissions.user_can_edit_category(
                    user=self._current_user,
                    category=event.item,
                ):
                    request = requests.EditCategory(category=event.item)

                    self.edit_requests.emit(request)
            case _:
                logger.error(f"attr name, {event.attr.name!r}, not recognized.")

    def _on_double_click(self, /, event: table_view.DoubleClickEvent[domain.Category, str]) -> None:
        if domain.permissions.user_can_edit_category(
            user=self._current_user,
            category=self.table.selected_item,
        ):
            delete_request = requests.DeleteCategory(category=event.item)

            self.delete_requests.emit(delete_request)
