import typing

import qtawesome as qta
from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa
from loguru import logger

from src import domain
from src.presentation.shared import fonts, icons
from src.presentation.shared.widgets import MapCBO, table_view
from src.presentation.todo.dash.state import ALL_CATEGORY, ALL_USER, TodoDashState
from src.presentation.todo import requests

__all__ = ("TodoDash",)


class TodoDash(qtw.QWidget):
    delete_requests = qtc.pyqtSignal(requests.DeleteTodo)
    edit_requests = qtc.pyqtSignal(requests.EditTodo)
    toggle_completed_requests = qtc.pyqtSignal(requests.ToggleCompleted)

    def __init__(self, *, parent: qtw.QWidget | None = None):
        super().__init__(parent=parent)

        self._current_user = ALL_USER

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

        due_lbl = qtw.QLabel("Due?")
        due_lbl.setFont(fonts.BOLD)
        self._due_chk = qtw.QCheckBox()
        self._due_chk.setChecked(True)
        self._due_chk.stateChanged.connect(self.refresh_btn.click)  # noqa

        category_lbl = qtw.QLabel("Category")
        category_lbl.setFont(fonts.BOLD)
        self._category_cbo: MapCBO[domain.Category] = MapCBO(
            mapping={ALL_CATEGORY: "All"},
            value=ALL_CATEGORY,
        )
        self._category_cbo.setMaximumWidth(150)
        self._category_cbo.value_changed.connect(self.refresh_btn.click)

        user_lbl = qtw.QLabel("User")
        user_lbl.setFont(fonts.BOLD)
        self.user_cbo: MapCBO[domain.User] = MapCBO(
            mapping={ALL_USER: "All"},
            value=ALL_USER,
        )
        self.user_cbo.setMaximumWidth(150)
        self.user_cbo.value_changed.connect(self.refresh_btn.click)

        description_lbl = qtw.QLabel("Description")
        description_lbl.setFont(fonts.BOLD)
        self._description_filter_txt = qtw.QLineEdit("")
        self._description_filter_txt.setMaximumWidth(200)

        toolbar_layout = qtw.QHBoxLayout()
        toolbar_layout.addWidget(self.refresh_btn)
        toolbar_layout.addWidget(self.add_btn)
        toolbar_layout.addSpacerItem(qtw.QSpacerItem(10, 0, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Minimum))
        toolbar_layout.addWidget(due_lbl)
        toolbar_layout.addWidget(self._due_chk)
        toolbar_layout.addWidget(user_lbl)
        toolbar_layout.addWidget(self.user_cbo)
        toolbar_layout.addWidget(category_lbl)
        toolbar_layout.addWidget(self._category_cbo)
        toolbar_layout.addWidget(description_lbl)
        toolbar_layout.addWidget(self._description_filter_txt)
        toolbar_layout.addSpacerItem(qtw.QSpacerItem(0, 0, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum))

        fm = qtg.QFontMetrics(fonts.BOLD)

        self._table: table_view.TableView[domain.Todo, str] = table_view.TableView(
            attrs=(
                table_view.integer(
                    name="todo_id",
                    display_name="ID",
                    key=True,
                ),
                table_view.button(
                    name="complete",
                    button_text="Complete",
                    text_selector=lambda todo: "Complete" if todo.should_display() else "Incomplete",
                    width=fm.width(" Incomplete "),
                ),
                table_view.text(
                    name="description",
                    display_name="Description",
                    width=300,
                ),
                table_view.date(
                    name="due_date",
                    display_name="Due Date",
                    value_selector=lambda todo: todo.due_date(),
                ),
                table_view.text(
                    name="days",
                    display_name="Days",
                    value_selector=lambda todo: _render_days(todo.days()),
                    rich_text=True,
                ),
                table_view.text(
                    name="user",
                    display_name="User",
                    value_selector=lambda todo: todo.user.display_name,
                    width=140,
                    alignment="center",
                ),
                table_view.text(
                    name="category",
                    display_name="Category",
                    value_selector=lambda todo: todo.category.name,
                    alignment="center",
                ),
                table_view.text(
                    name="frequency",
                    display_name="Frequency",
                    value_selector=lambda todo: _render_frequency(frequency=todo.frequency),
                    alignment="center",
                ),
                table_view.text(
                    name="note",
                    display_name="Note",
                    width=400,
                    rich_text=True,
                ),
                table_view.date(
                    name="last_completed",
                    display_name="Last Completed",
                ),
                table_view.text(
                    name="last_completed_by",
                    display_name="Last Completed By",
                    value_selector=(
                        lambda todo: todo.last_completed_by.display_name if todo.last_completed_by is not None else ""
                    ),
                    alignment="center",
                    width=120,
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
                    # enable_when=lambda todo: domain.permissions.user_can_edit_todo(user=self._current_user, todo=todo),
                ),
                table_view.button(
                    name="delete",
                    button_text="Delete",
                    width=80,
                    # enable_when=lambda todo: domain.permissions.user_can_edit_todo(user=self._current_user, todo=todo),
                ),
            ),
            parent=self,
        )
        #     col_specs=[
        #         table.rich_text_col(
        #             display_name="Last Completed",
        #             selector=lambda todo: _render_last_completed(
        #                 last_completed=todo.last_completed,
        #                 last_completed_by=todo.last_completed_by,
        #             ),
        #             alignment=table.ColAlignment.Center,
        #             column_width=120,
        #         ),
        #         table.timestamp_col(
        #             attr_name="date_added",
        #             display_name="Added",
        #             alignment=table.ColAlignment.Center,
        #             display_format="%m/%d/%y",
        #             # display_format="%m/%d/%Y %I:%M %p",
        #             column_width=100,
        #         ),
        #         table.timestamp_col(
        #             attr_name="date_updated",
        #             display_name="Updated",
        #             alignment=table.ColAlignment.Center,
        #             display_format="%m/%d/%y",
        #             # display_format="%m/%d/%Y %I:%M %p",
        #             column_width=100,
        #         ),
        #         table.button_col(
        #             button_text="Edit",
        #             on_click=lambda _: self.edit_btn_clicked.emit(),  # noqa
        #             column_width=60,
        #             enable_when=lambda todo: domain.permissions.user_can_edit_todo(user=self._current_user, todo=todo),
        #         ),
        #         table.button_col(
        #             button_text="Delete",
        #             on_click=lambda _: self.delete_btn_clicked.emit(),  # noqa
        #             column_width=80,
        #             enable_when=lambda todo: domain.permissions.user_can_edit_todo(user=self._current_user, todo=todo),
        #         ),
        #     ],
        #     key_attr="todo_id",
        # )
        # self._table.double_click.connect(
        #     lambda: self.edit_btn_clicked.emit() if domain.permissions.user_can_edit_todo(  # noqa
        #         user=self._current_user,
        #         todo=self._table.selected_item,
        #     ) else None
        # )

        self._table.button_clicked.connect(self._on_button_clicked)

        self._table.double_click.connect(self._on_double_click)

        self._status_bar = qtw.QStatusBar()

        layout = qtw.QVBoxLayout()
        layout.addLayout(toolbar_layout)
        layout.addWidget(self._table)
        layout.addWidget(self._status_bar)
        self.setLayout(layout)

    def get_state(self) -> TodoDashState:
        return TodoDashState(
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

        self.user_cbo.set_values(mapping={ALL_USER: "All"} | {user: user.display_name for user in state.user_options})
        if self.user_cbo.get_value() != state.user_filter:
            self.user_cbo.set_value(value=state.user_filter)

        self._category_cbo.set_values(
            mapping={ALL_CATEGORY: "All"} | {category: category.name for category in state.category_options}
        )
        if self._category_cbo.get_value() != state.category_filter:
            self._category_cbo.set_value(value=state.category_filter)

        # self._date_edit.set_value(state.date_filter)
        self._due_chk.setChecked(state.due_filter)
        self._description_filter_txt.setText(state.description_filter)
        self._table.set_items(state.todos)
        if state.selected_todo is None:
            self._table.clear_selection()
        else:
            self._table.select_item_by_key(key=state.selected_todo.todo_id)
        self._status_bar.showMessage(state.status)
        self.repaint()

    def _on_button_clicked(self, /, event: table_view.ButtonClickedEvent[domain.Todo, typing.Any]) -> None:
        logger.debug(f"{self.__class__.__name__}._on_button_clicked({event=!r})")

        match event.attr.name:
            case "delete":
                if domain.permissions.user_can_edit_todo(
                    user=self._current_user,
                    todo=event.item,
                ):
                    request = requests.DeleteTodo(todo=event.item)

                    self.delete_requests.emit(request)
            case "edit":
                if domain.permissions.user_can_edit_todo(
                    user=self._current_user,
                    todo=event.item,
                ):
                    request = requests.EditTodo(todo=event.item)

                    self.edit_requests.emit(request)
            case "complete":
                request = requests.ToggleCompleted(todo=event.item)

                self.toggle_completed_requests.emit(request)
            case _:
                logger.error(f"attr name, {event.attr.name!r}, not recognized.")

    def _on_double_click(self, /, event: table_view.DoubleClickEvent[domain.Todo, typing.Any]) -> None:
        logger.debug(f"{self.__class__.__name__}._on_button_clicked({event=!r})")

        if domain.permissions.user_can_edit_todo(
            user=self._current_user,
            todo=event.item,
        ):
            edit_request = requests.EditTodo(todo=event.item)

            self.edit_requests.emit(edit_request)


def _render_days(days: int | None, /) -> str:
    if days is None:
        return ""

    if days < 0:
        return f'<center><font color="red">{days}</font></center>'

    if days == 0:
        return f'<center><font color="yellow">{days}</font></center>'

    return f"<center>{days}</center>"


def _render_frequency(*, frequency: domain.Frequency) -> str:
    return {
        domain.FrequencyType.Daily: lambda: "Daily",
        domain.FrequencyType.Easter: lambda: "Easter",
        domain.FrequencyType.MemorialDay: lambda: "Memorial Day",
        domain.FrequencyType.Irregular: lambda: "Irregular",
        domain.FrequencyType.Monthly: lambda: f"Monthly ({frequency.month_day})",
        domain.FrequencyType.Once: lambda: f"{frequency.due_date:%m/%d/%Y}",
        domain.FrequencyType.Weekly: lambda: f"Weekly ({frequency.week_day.short_name})",  # type: ignore
        domain.FrequencyType.XDays: lambda: f"XDays ({frequency.days})",
        domain.FrequencyType.Yearly: (
            lambda: f"Yearly ({frequency.month.to_int()}/{frequency.month_day})"  # type: ignore
        ),
    }[frequency.name]()


# def _render_last_completed(
#     *,
#     last_completed: datetime.date | None,
#     last_completed_by: domain.User | None,
# ) -> str:
#     if last_completed:
#         if last_completed_by:
#             username = "<br>" + last_completed_by.display_name
#         else:
#             username = ""
#         return f"<center>{last_completed:%m/%d/%y}{username}</center>"
#     return ""
