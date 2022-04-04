import datetime

from PyQt5 import QtCore as qtc, QtWidgets as qtw

from src import domain
from src.presentation.category.dash.state import CategoryDashState
from src.presentation.shared.widgets import table

__all__ = ("CategoryDash",)


class CategoryDash(qtw.QWidget):
    delete_btn_clicked = qtc.pyqtSignal()
    edit_btn_clicked = qtc.pyqtSignal()

    def __init__(self, *, state: CategoryDashState):
        super().__init__()

        self.refresh_btn = qtw.QPushButton("Refresh")
        self.refresh_btn.setMinimumWidth(100)
        self.refresh_btn.setDefault(True)

        self.add_btn = qtw.QPushButton("Add")
        self.add_btn.setMinimumWidth(100)

        toolbar_layout = qtw.QHBoxLayout()
        toolbar_layout.addWidget(self.refresh_btn)
        toolbar_layout.addWidget(self.add_btn)
        toolbar_layout.addSpacerItem(qtw.QSpacerItem(0, 0, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum))

        self.table: table.Table[domain.Category, str] = table.Table(
            spec=table.TableSpec(
                col_specs=[
                    table.text_col(display_name="ID", attr_name="category_id", hidden=True),
                    table.text_col(display_name="Name", attr_name="name", column_width=200),
                    table.text_col(display_name="Note", attr_name="note", column_width=400),
                    table.timestamp_col(
                        attr_name="date_added",
                        display_name="Added",
                        alignment=table.ColAlignment.Center,
                        display_format="%m/%d/%Y %I:%M %p",
                        column_width=110,
                    ),
                    table.timestamp_col(
                        attr_name="date_updated",
                        display_name="Updated",
                        alignment=table.ColAlignment.Center,
                        display_format="%m/%d/%Y %I:%M %p",
                        column_width=110,
                    ),
                    table.button_col(
                        button_text="Edit",
                        on_click=self.edit_btn_clicked.emit,
                        column_width=100,
                        enable_when=lambda category: category.name not in ("Holiday", "Todo"),
                    ),
                    table.button_col(
                        button_text="Delete",
                        on_click=self.delete_btn_clicked.emit,
                        column_width=100,
                        enable_when=lambda category: category.name not in ("Holiday", "Todo"),
                    ),
                ],
                key_attr="category_id",
            ),
        )

        self._status_bar = qtw.QStatusBar()

        layout = qtw.QVBoxLayout()
        layout.addLayout(toolbar_layout)
        layout.addWidget(self.table)
        layout.addWidget(self._status_bar)
        self.setLayout(layout)

        self.set_state(state=state)

    def get_state(self) -> CategoryDashState:
        return CategoryDashState(
            categories=self.table.items,
            selected_category=self.table.selected_item,
            status=self._status_bar.currentMessage(),
        )

    def set_state(self, *, state: CategoryDashState) -> None:
        self.table.set_all(state.categories)
        if state.selected_category is None:
            self.table.clear_selection()
        else:
            self.table.select_item_by_key(key=state.selected_category.category_id)
        self._set_status(message=state.status)

    def _set_status(self, *, message: str) -> None:
        if message:
            ts_str = datetime.datetime.now().strftime("%-m/%-d @ %-I:%M %p")
            self._status_bar.showMessage(f"{ts_str}: {message}")
            self.repaint()
        else:
            self._status_bar.clearMessage()
