from __future__ import annotations

import datetime

from PyQt5 import QtCore as qtc, QtWidgets as qtw

from src import domain
from src.presentation.shared import fonts
from src.presentation.shared.widgets import MapCBO, table
from src.presentation.todo.dash.state import ALL_CATEGORY, TodoDashState

__all__ = ("TodoDash",)


class TodoDash(qtw.QWidget):
    delete_btn_clicked = qtc.pyqtSignal()
    edit_btn_clicked = qtc.pyqtSignal()
    complete_btn_clicked = qtc.pyqtSignal()
    incomplete_btn_clicked = qtc.pyqtSignal()

    def __init__(self, *, state: TodoDashState):
        super().__init__()

        self.refresh_btn = qtw.QPushButton("Refresh")
        self.refresh_btn.setMinimumWidth(100)
        self.refresh_btn.setDefault(True)

        self.add_btn = qtw.QPushButton("Add")
        self.add_btn.setMinimumWidth(100)

        date_lbl = qtw.QLabel("Today")
        date_lbl.setFont(fonts.bold)
        self._date_edit = qtw.QDateEdit()
        self._date_edit.dateChanged.connect(self.refresh_btn.click)

        due_lbl = qtw.QLabel("Due?")
        due_lbl.setFont(fonts.bold)
        self._due_chk = qtw.QCheckBox()
        self._due_chk.stateChanged.connect(self.refresh_btn.click)

        category_lbl = qtw.QLabel("Category")
        category_lbl.setFont(fonts.bold)
        self._category_cbo: MapCBO[domain.Category] = MapCBO(
            mapping={
                ALL_CATEGORY: "All",
                domain.TODO_CATEGORY: "Todo"
            },
            value=ALL_CATEGORY,
        )
        self._category_cbo.setMinimumWidth(150)
        self._category_cbo.value_changed.connect(self.refresh_btn.click)

        description_lbl = qtw.QLabel("Description")
        description_lbl.setFont(fonts.bold)
        self._description_filter_txt = qtw.QLineEdit(state.description_filter)
        self._description_filter_txt.setMaximumWidth(200)

        toolbar_layout = qtw.QHBoxLayout()
        toolbar_layout.addWidget(self.refresh_btn)
        toolbar_layout.addWidget(self.add_btn)
        toolbar_layout.addSpacerItem(qtw.QSpacerItem(10, 0, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Minimum))
        toolbar_layout.addWidget(date_lbl)
        toolbar_layout.addWidget(self._date_edit)
        toolbar_layout.addWidget(due_lbl)
        toolbar_layout.addWidget(self._due_chk)
        toolbar_layout.addWidget(category_lbl)
        toolbar_layout.addWidget(self._category_cbo)
        toolbar_layout.addWidget(description_lbl)
        toolbar_layout.addWidget(self._description_filter_txt)
        toolbar_layout.addSpacerItem(qtw.QSpacerItem(0, 0, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum))

        self._table: table.Table[domain.Todo, str] = table.Table(
            spec=table.TableSpec(
                col_specs=[
                    table.text_col(
                        attr_name="todo_id",
                        display_name="ID",
                        hidden=True,
                    ),
                    table.text_col(
                        attr_name="description",
                        display_name="Description",
                        column_width=300,
                    ),
                    table.text_col(
                        selector=lambda todo: todo.category.name,
                        display_name="Category",
                        column_width=140,
                        hidden=False,
                        alignment=table.ColAlignment.Center,
                    ),
                    table.text_col(
                        selector=lambda todo: todo.frequency.name.value,
                        display_name="Frequency",
                        column_width=140,
                        hidden=False,
                        alignment=table.ColAlignment.Center,
                    ),
                    table.text_col(
                        attr_name="note",
                        display_name="Note",
                        column_width=500,
                    ),
                    table.date_col(
                        selector=lambda todo: todo.due_date(today=self._date_edit.date().toPyDate()),
                        display_name="Due Date",
                        alignment=table.ColAlignment.Center,
                        column_width=120,
                        display_fn=lambda due_date: due_date_description(due_date=due_date, today=self._date_edit.date().toPyDate()),
                    ),
                    table.date_col(
                        attr_name="last_completed",
                        display_name="Last Completed",
                        alignment=table.ColAlignment.Center,
                        column_width=160,
                    ),
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
                        enable_when=lambda todo: todo.frequency.name != domain.FrequencyType.Easter,
                    ),
                    table.button_col(
                        button_text="Delete",
                        on_click=self.delete_btn_clicked.emit,
                        column_width=100,
                    ),
                    table.button_col(
                        button_text="Complete",
                        on_click=self.complete_btn_clicked.emit,
                        column_width=110,
                    ),
                    table.button_col(
                        button_text="Incomplete",
                        on_click=self.incomplete_btn_clicked.emit,
                        column_width=120,
                        enable_when=lambda todo: todo.last_completed is not None,
                    ),
                ],
                key_attr="todo_id",
            )
        )

        self._status_bar = qtw.QStatusBar()

        layout = qtw.QVBoxLayout()
        layout.addLayout(toolbar_layout)
        layout.addWidget(self._table)
        layout.addWidget(self._status_bar)
        self.setLayout(layout)

        self.set_state(state=state)

    def get_state(self) -> TodoDashState:
        return TodoDashState(
            date_filter=self._date_edit.date().toPyDate(),
            due_filter=self._due_chk.isChecked(),
            description_filter=self._description_filter_txt.text(),
            category_filter=self._category_cbo.get_value(),
            selected_todo=self._table.selected_item,
            todos=self._table.items,
            category_options=self._category_cbo.get_values(),
            status=self._status_bar.currentMessage(),
        )

    def set_state(self, *, state: TodoDashState) -> None:
        self._category_cbo.set_values(
            mapping={ALL_CATEGORY: "All"} | {
                category: category.name
                for category in state.category_options
            }
        )
        if self._category_cbo.get_value() != state.category_filter:
            self._category_cbo.set_value(value=state.category_filter)
        self._date_edit.setDate(state.date_filter)
        self._due_chk.setChecked(state.due_filter)
        self._description_filter_txt.setText(state.description_filter)
        self._table.set_all(state.todos)
        if state.selected_todo is None:
            self._table.clear_selection()
        else:
            self._table.select_item_by_key(key=state.selected_todo.todo_id)
        self._set_status(message=state.status)

    def _set_status(self, *, message: str) -> None:
        if message:
            ts_str = datetime.datetime.now().strftime("%-m/%-d @ %-I:%M %p")
            self._status_bar.showMessage(f"{ts_str}: {message}")
            self.repaint()
        else:
            self._status_bar.clearMessage()


def due_date_description(*, due_date: datetime.date, today: datetime.date) -> str:
    days_until = (due_date - today).days
    return f"{due_date:%m/%d/%y}\n{days_until} days"
