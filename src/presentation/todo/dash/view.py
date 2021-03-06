from __future__ import annotations

import datetime

from PyQt5 import QtCore as qtc, QtWidgets as qtw
import qtawesome as qta

from src import domain
from src.presentation.shared import fonts, icons, widgets
from src.presentation.shared.widgets import MapCBO, table
from src.presentation.todo.dash.state import ALL_CATEGORY, ALL_USER, TodoDashState

__all__ = ("TodoDash",)


class TodoDash(qtw.QWidget):
    delete_btn_clicked = qtc.pyqtSignal()
    edit_btn_clicked = qtc.pyqtSignal()
    complete_btn_clicked = qtc.pyqtSignal()
    incomplete_btn_clicked = qtc.pyqtSignal()

    def __init__(self, *, parent: qtw.QWidget | None = None):
        super().__init__(parent=parent)

        self._current_user = ALL_USER

        refresh_btn_icon = qta.icon(icons.refresh_btn_icon_name, color=self.parent().palette().text().color())
        self.refresh_btn = qtw.QPushButton(refresh_btn_icon, "Refresh")
        self.refresh_btn.setFont(fonts.bold)
        self.refresh_btn.setMaximumWidth(100)
        self.refresh_btn.setDefault(True)

        add_btn_icon = qta.icon(icons.add_btn_icon_name, color=self.parent().palette().text().color())
        self.add_btn = qtw.QPushButton(add_btn_icon, "Add")
        self.add_btn.setFont(fonts.bold)
        self.add_btn.setMaximumWidth(100)

        date_lbl = qtw.QLabel("Today")
        date_lbl.setFont(fonts.bold)
        self._date_edit = widgets.DateEditor()
        self._date_edit.set_value(datetime.date.today())
        self._date_edit.date_changed.connect(self.refresh_btn.click)

        due_lbl = qtw.QLabel("Due?")
        due_lbl.setFont(fonts.bold)
        self._due_chk = qtw.QCheckBox()
        self._due_chk.setChecked(True)
        self._due_chk.stateChanged.connect(self.refresh_btn.click)

        category_lbl = qtw.QLabel("Category")
        category_lbl.setFont(fonts.bold)
        self._category_cbo: MapCBO[domain.Category] = MapCBO(mapping={ALL_CATEGORY: "All"}, value=ALL_CATEGORY)
        self._category_cbo.setMaximumWidth(150)
        self._category_cbo.value_changed.connect(self.refresh_btn.click)

        user_lbl = qtw.QLabel("User")
        user_lbl.setFont(fonts.bold)
        self.user_cbo: MapCBO[domain.User] = MapCBO(mapping={ALL_USER: "All"}, value=ALL_USER)
        self.user_cbo.setMaximumWidth(150)
        self.user_cbo.value_changed.connect(self.refresh_btn.click)

        description_lbl = qtw.QLabel("Description")
        description_lbl.setFont(fonts.bold)
        self._description_filter_txt = qtw.QLineEdit("")
        self._description_filter_txt.setMaximumWidth(200)

        toolbar_layout = qtw.QHBoxLayout()
        toolbar_layout.addWidget(self.refresh_btn)
        toolbar_layout.addWidget(self.add_btn)
        toolbar_layout.addSpacerItem(qtw.QSpacerItem(10, 0, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Minimum))
        toolbar_layout.addWidget(date_lbl)
        toolbar_layout.addWidget(self._date_edit)
        toolbar_layout.addWidget(due_lbl)
        toolbar_layout.addWidget(self._due_chk)
        toolbar_layout.addWidget(user_lbl)
        toolbar_layout.addWidget(self.user_cbo)
        toolbar_layout.addWidget(category_lbl)
        toolbar_layout.addWidget(self._category_cbo)
        toolbar_layout.addWidget(description_lbl)
        toolbar_layout.addWidget(self._description_filter_txt)
        toolbar_layout.addSpacerItem(qtw.QSpacerItem(0, 0, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum))

        self._table: table.Table[domain.Todo, str] = table.Table(
            col_specs=[
                table.text_col(
                    attr_name="todo_id",
                    display_name="ID",
                    hidden=True,
                ),
                table.button_col(
                    button_text="Complete",
                    on_click=lambda _: self.complete_btn_clicked.emit(),  # noqa
                    alignment=table.ColAlignment.Center,
                ),
                table.text_col(
                    attr_name="description",
                    display_name="Description",
                    column_width=300,
                ),
                table.date_col(
                    selector=lambda todo: todo.due_date(today=self._date_edit.get_value() or datetime.date.today()),
                    display_name="Due Date",
                    alignment=table.ColAlignment.Center,
                    column_width=120,
                ),
                table.rich_text_col(
                    selector=lambda todo: render_days(
                        due_date=todo.due_date(today=self._date_edit.get_value() or datetime.date.today()),
                        today=self._date_edit.get_value() or datetime.date.today(),
                    ),
                    display_name="Days",
                    alignment=table.ColAlignment.Center,
                    column_width=60,
                ),
                table.text_col(
                    selector=lambda todo: todo.user.display_name,
                    display_name="User",
                    column_width=140,
                    hidden=False,
                    alignment=table.ColAlignment.Center,
                ),
                table.text_col(
                    selector=lambda todo: todo.category.name,
                    display_name="Category",
                    column_width=140,
                    hidden=False,
                    alignment=table.ColAlignment.Center,
                ),
                table.text_col(
                    selector=lambda todo: render_frequency(frequency=todo.frequency),
                    display_name="Frequency",
                    column_width=140,
                    hidden=False,
                    alignment=table.ColAlignment.Center,
                ),
                table.rich_text_col(
                    attr_name="note",
                    display_name="Note",
                    column_width=400,
                ),
                table.rich_text_col(
                    display_name="Last Completed",
                    selector=lambda todo: render_last_completed(
                        last_completed=todo.last_completed,
                        last_completed_by=todo.last_completed_by,
                    ),
                    alignment=table.ColAlignment.Center,
                    column_width=120,
                ),
                table.timestamp_col(
                    attr_name="date_added",
                    display_name="Added",
                    alignment=table.ColAlignment.Center,
                    display_format="%m/%d/%y",
                    # display_format="%m/%d/%Y %I:%M %p",
                    column_width=100,
                ),
                table.timestamp_col(
                    attr_name="date_updated",
                    display_name="Updated",
                    alignment=table.ColAlignment.Center,
                    display_format="%m/%d/%y",
                    # display_format="%m/%d/%Y %I:%M %p",
                    column_width=100,
                ),
                table.button_col(
                    button_text="Incomplete",
                    on_click=lambda _: self.incomplete_btn_clicked.emit(),  # noqa
                    enable_when=lambda todo: todo.last_completed is not None,
                ),
                table.button_col(
                    button_text="Edit",
                    on_click=lambda _: self.edit_btn_clicked.emit(),  # noqa
                    column_width=60,
                    enable_when=lambda todo: domain.permissions.user_can_edit_todo(user=self._current_user, todo=todo),
                ),
                table.button_col(
                    button_text="Delete",
                    on_click=lambda _: self.delete_btn_clicked.emit(),  # noqa
                    column_width=80,
                    enable_when=lambda todo: domain.permissions.user_can_edit_todo(user=self._current_user, todo=todo),
                ),
            ],
            key_attr="todo_id",
        )
        self._table.double_click.connect(
            lambda: self.edit_btn_clicked.emit() if domain.permissions.user_can_edit_todo(  # noqa
                user=self._current_user,
                todo=self._table.selected_item,
            ) else None
        )

        self._status_bar = qtw.QStatusBar()

        layout = qtw.QVBoxLayout()
        layout.addLayout(toolbar_layout)
        layout.addWidget(self._table)
        layout.addWidget(self._status_bar)
        self.setLayout(layout)

    def get_state(self) -> TodoDashState:
        return TodoDashState(
            date_filter=self._date_edit.get_value() or datetime.date.today(),
            due_filter=self._due_chk.isChecked(),
            description_filter=self._description_filter_txt.text(),
            category_filter=self._category_cbo.get_value(),
            user_filter=self.user_cbo.get_value(),
            selected_todo=self._table.selected_item,
            todos=self._table.items,
            category_options=self._category_cbo.get_values(),
            user_options=self.user_cbo.get_values(),
            status=self._status_bar.currentMessage(),
            current_user=self._current_user,
        )

    def set_state(self, *, state: TodoDashState) -> None:
        self._current_user = state.current_user

        self.user_cbo.set_values(
            mapping={ALL_USER: "All"} | {
                user: user.display_name
                for user in state.user_options
            }
        )
        if self.user_cbo.get_value() != state.user_filter:
            self.user_cbo.set_value(value=state.user_filter)

        self._category_cbo.set_values(
            mapping={ALL_CATEGORY: "All"} | {
                category: category.name
                for category in state.category_options
            }
        )
        if self._category_cbo.get_value() != state.category_filter:
            self._category_cbo.set_value(value=state.category_filter)

        # self._date_edit.set_value(state.date_filter)
        self._due_chk.setChecked(state.due_filter)
        self._description_filter_txt.setText(state.description_filter)
        self._table.set_all(state.todos)
        if state.selected_todo is None:
            self._table.clear_selection()
        else:
            self._table.select_item_by_key(key=state.selected_todo.todo_id)
        self._status_bar.showMessage(state.status)
        self.repaint()


def render_days(*, due_date: datetime.date, today: datetime.date) -> str:
    days = (due_date - today).days

    if days < 0:
        return f'<center><font color="red">{days}</font></center>'

    if days == 0:
        return f'<center><font color="yellow">{days}</font></center>'

    return f"<center>{days}</center>"


def render_frequency(*, frequency: domain.Frequency) -> str:
    return {
        domain.FrequencyType.Daily: lambda: "Daily",
        domain.FrequencyType.Easter: lambda: "Easter",
        domain.FrequencyType.MemorialDay: lambda: "Memorial Day",
        domain.FrequencyType.Irregular: lambda: "Irregular",
        domain.FrequencyType.Monthly: lambda: f"Monthly ({frequency.month_day})",
        domain.FrequencyType.Once: lambda: f"{frequency.due_date:%m/%d/%Y}",
        domain.FrequencyType.Weekly: lambda: f"Weekly ({frequency.week_day.short_name})",
        domain.FrequencyType.XDays: lambda: f"XDays ({frequency.days})",
        domain.FrequencyType.Yearly: lambda: f"Yearly ({frequency.month.to_int()}/{frequency.month_day})",
    }[frequency.name]()


def render_last_completed(
    *,
    last_completed: datetime.date | None,
    last_completed_by: domain.User | None,
) -> str:
    if last_completed:
        if last_completed_by:
            username = "<br>" + last_completed_by.display_name
        else:
            username = ""
        return f"<center>{last_completed:%m/%d/%y}{username}</center>"
    return ""
