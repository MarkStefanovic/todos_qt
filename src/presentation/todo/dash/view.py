from __future__ import annotations

from PyQt5 import QtCore as qtc, QtWidgets as qtw

from src import domain
from src.presentation.shared import fonts, widgets
from src.presentation.todo.dash.state import TodoDashState

__all__ = ("TodoDash",)


class TodoDash(qtw.QWidget):
    delete_btn_clicked = qtc.pyqtSignal(domain.Todo)
    edit_btn_clicked = qtc.pyqtSignal(domain.Todo)
    mark_complete_btn_clicked = qtc.pyqtSignal(domain.Todo)

    def __init__(self, *, state: TodoDashState):
        super().__init__()

        self.refresh_button = qtw.QPushButton("Refresh")
        self.refresh_button.setMinimumWidth(100)

        self.add_button = qtw.QPushButton("Add")
        self.add_button.setMinimumWidth(100)

        description_lbl = qtw.QLabel("DESCRIPTION")
        description_lbl.setFont(fonts.bold)
        self._description_filter_txt = qtw.QLineEdit(state.description_filter)
        self._description_filter_txt.setMaximumWidth(200)

        button_layout = qtw.QHBoxLayout()
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.add_button)
        button_layout.addSpacerItem(qtw.QSpacerItem(10, 0, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Minimum))
        button_layout.addWidget(description_lbl)
        button_layout.addWidget(self._description_filter_txt)
        button_layout.addSpacerItem(qtw.QSpacerItem(0, 0, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum))

        self._table: widgets.Table[domain.Todo, str] = widgets.Table(
            spec=widgets.TableSpec(
                col_specs=[
                    widgets.ColSpec.text(attr_name="todo_id", display_name="ID", hidden=True),
                    widgets.ColSpec.text(attr_name="description", display_name="Description", column_width=300),
                    widgets.ColSpec(
                        attr_name="category",
                        display_name="Category",
                        display_fn=lambda c: str(c),
                        column_width=140,
                        hidden=False,
                        type=widgets.ColSpecType.Text,
                        alignment=widgets.ColAlignment.Center,
                        on_click=None,
                    ),
                    widgets.ColSpec(
                        attr_name="frequency",
                        display_name="Frequency",
                        display_fn=lambda c: str(c),
                        column_width=140,
                        hidden=False,
                        type=widgets.ColSpecType.Text,
                        alignment=widgets.ColAlignment.Center,
                        on_click=None
                    ),
                    widgets.ColSpec.int(attr_name="advance_days", display_name="Advance Days", column_width=140),
                    widgets.ColSpec.int(attr_name="expire_days", display_name="Expire Days", column_width=140),
                    widgets.ColSpec.rich_text(attr_name="note", display_name="Note", column_width=300),
                    widgets.ColSpec.date(attr_name="start_date", display_name="Start"),
                    widgets.ColSpec.timestamp(attr_name="date_added", display_name="Added"),
                    widgets.ColSpec.timestamp(attr_name="date_updated", display_name="Updated"),
                    widgets.ColSpec.button(button_text="Edit", on_click=self.edit_btn_clicked.emit, column_width=100),
                    widgets.ColSpec.button(button_text="Delete", on_click=self.delete_btn_clicked.emit, column_width=100),
                    widgets.ColSpec.button(button_text="Complete", on_click=self.mark_complete_btn_clicked.emit, column_width=100),
                ],
                key_attr="todo_id",
            )
        )

        layout = qtw.QVBoxLayout()
        layout.addLayout(button_layout)
        layout.addWidget(self._table)
        self.setLayout(layout)

        self.set_state(state=state)

    def get_state(self) -> TodoDashState:
        return TodoDashState(
            description_filter=self._description_filter_txt.text(),
            selected_todo_id=self._table.selected_row_key,
        )

    def set_state(self, *, state: TodoDashState) -> None:
        self._description_filter_txt.setText(state.description_filter)
        if state.selected_todo_id is None:
            self._table.clear_selection()
        else:
            self._table.select_row_by_key(key=state.selected_todo_id)
