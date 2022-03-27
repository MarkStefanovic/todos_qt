from __future__ import annotations

from PyQt5 import QtCore as qtc, QtWidgets as qtw

from src import domain
from src.presentation.shared import fonts
from src.presentation.shared.widgets import table
from src.presentation.todo.dash.state import TodoDashState

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

        due_lbl = qtw.QLabel("Due?")
        due_lbl.setFont(fonts.bold)
        self._due_chk = qtw.QCheckBox()

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
                    ),
                    table.date_col(
                        attr_name="last_completed",
                        display_name="Last Completed",
                        alignment=table.ColAlignment.Center,
                        column_width=160,
                    ),
                    # table.date_col(
                    #     selector=lambda todo: todo.frequency.start_date,
                    #     display_name="Start",
                    #     alignment=table.ColAlignment.Center,
                    # ),
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

        layout = qtw.QVBoxLayout()
        layout.addLayout(toolbar_layout)
        layout.addWidget(self._table)
        self.setLayout(layout)

        self.set_state(state=state)

    def get_state(self) -> TodoDashState:
        return TodoDashState(
            date_filter=self._date_edit.date().toPyDate(),
            due_filter=self._due_chk.isChecked(),
            description_filter=self._description_filter_txt.text(),
            selected_todo=self._table.selected_item,
            todos=self._table.items,
        )

    def set_state(self, *, state: TodoDashState) -> None:
        self._date_edit.setDate(state.date_filter)
        self._due_chk.setChecked(state.due_filter)
        self._description_filter_txt.setText(state.description_filter)
        self._table.set_all(state.todos)
        if state.selected_todo is None:
            self._table.clear_selection()
        else:
            self._table.select_item_by_key(key=state.selected_todo.todo_id)
