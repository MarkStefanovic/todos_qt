from PyQt5 import QtCore as qtc, QtWidgets as qtw

from src import domain
from src.presentation.category.dash.state import CategoryDashState
from src.presentation.shared import fonts, icons
from src.presentation.shared.widgets import table

import qtawesome as qta

__all__ = ("CategoryDash",)


class CategoryDash(qtw.QWidget):
    delete_btn_clicked = qtc.pyqtSignal()
    edit_btn_clicked = qtc.pyqtSignal()

    def __init__(self, *, parent: qtw.QWidget | None = None):
        super().__init__(parent=parent)

        self._current_user = domain.DEFAULT_USER

        refresh_btn_icon = qta.icon(icons.refresh_btn_icon_name, color=self.parent().palette().text().color())
        self.refresh_btn = qtw.QPushButton(refresh_btn_icon, "Refresh")
        self.refresh_btn.setFont(fonts.bold)
        self.refresh_btn.setMaximumWidth(100)
        self.refresh_btn.setDefault(True)

        add_btn_icon = qta.icon(icons.add_btn_icon_name, color=self.parent().palette().text().color())
        self.add_btn = qtw.QPushButton(add_btn_icon, "Add")
        self.add_btn.setFont(fonts.bold)
        self.add_btn.setMaximumWidth(100)

        toolbar_layout = qtw.QHBoxLayout()
        toolbar_layout.addWidget(self.refresh_btn)
        toolbar_layout.addWidget(self.add_btn)
        toolbar_layout.addSpacerItem(qtw.QSpacerItem(0, 0, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum))

        self.table: table.Table[domain.Category, str] = table.Table(
            col_specs=[
                table.text_col(
                    display_name="ID",
                    attr_name="category_id",
                    hidden=True,
                ),
                table.text_col(
                    display_name="Name",
                    attr_name="name",
                    column_width=200,
                ),
                table.rich_text_col(
                    display_name="Note",
                    attr_name="note",
                    column_width=400,
                ),
                table.timestamp_col(
                    attr_name="date_added",
                    display_name="Added",
                    alignment=table.ColAlignment.Center,
                    display_format="%m/%d/%Y",
                    # display_format="%m/%d/%Y %I:%M %p",
                    column_width=100,
                ),
                table.timestamp_col(
                    attr_name="date_updated",
                    display_name="Updated",
                    alignment=table.ColAlignment.Center,
                    display_format="%m/%d/%Y",
                    # display_format="%m/%d/%Y %I:%M %p",
                    column_width=100,
                ),
                table.button_col(
                    button_text="Edit",
                    on_click=lambda _: self.edit_btn_clicked.emit(),
                    column_width=60,
                    enable_when=lambda category: domain.permissions.user_can_edit_category(
                        user=self._current_user,
                        category=category,
                    ),
                ),
                table.button_col(
                    button_text="Delete",
                    on_click=lambda _: self.delete_btn_clicked.emit(),
                    column_width=60,
                    enable_when=lambda category: domain.permissions.user_can_edit_category(
                        user=self._current_user,
                        category=category,
                    ),
                ),
            ],
            key_attr="category_id",
        )
        self.table.double_click.connect(
            lambda: self.edit_btn_clicked.emit() if domain.permissions.user_can_edit_category(
                user=self._current_user,
                category=self.table.selected_item,
            ) else None
        )

        self._status_bar = qtw.QStatusBar()

        layout = qtw.QVBoxLayout()
        layout.addLayout(toolbar_layout)
        layout.addWidget(self.table)
        layout.addWidget(self._status_bar)
        self.setLayout(layout)

    def get_state(self) -> CategoryDashState:
        return CategoryDashState(
            categories=self.table.items,
            selected_category=self.table.selected_item,
            status=self._status_bar.currentMessage(),
            current_user=self._current_user,
        )

    def set_state(self, *, state: CategoryDashState) -> None:
        self._current_user = state.current_user
        self.table.set_all(state.categories)
        if state.selected_category is None:
            self.table.clear_selection()
        else:
            self.table.select_item_by_key(key=state.selected_category.category_id)
        self._status_bar.showMessage(state.status)
