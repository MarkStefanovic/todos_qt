import typing

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa
from loguru import logger

from src import domain
from src.presentation.category_selector import CategorySelectorWidget
from src.presentation.shared import fonts, icons
from src.presentation.shared.widgets import table_view, StatusBar
from src.presentation.todo.view.dash import requests
from src.presentation.todo.view.dash.state import TodoDashState
from src.presentation.user_selector import UserSelectorWidget

__all__ = ("TodoDashView",)


class TodoDashView(qtw.QWidget):
    def __init__(
        self,
        *,
        todo_dash_requests: requests.TodoDashRequests,
        category_selector: CategorySelectorWidget,
        user_selector: UserSelectorWidget,
        current_user: domain.User,
        parent: qtw.QWidget | None = None,
    ):
        super().__init__(parent=parent)

        self._requests: typing.Final[requests.TodoDashRequests] = todo_dash_requests
        self._category_selector: typing.Final[CategorySelectorWidget] = category_selector
        self._user_selector: typing.Final[UserSelectorWidget] = user_selector
        self._current_user: typing.Final[domain.User] = current_user

        refresh_btn_icon = icons.refresh_btn_icon(parent=self)
        self._refresh_btn = qtw.QPushButton(refresh_btn_icon, "Refresh")
        self._refresh_btn.setFont(fonts.BOLD)
        self._refresh_btn.setMaximumWidth(100)
        self._refresh_btn.setDefault(True)

        add_btn_icon = icons.add_btn_icon(parent=self)
        self._add_btn = qtw.QPushButton(add_btn_icon, "Add")
        self._add_btn.setFont(fonts.BOLD)
        self._add_btn.setMaximumWidth(100)

        due_lbl = qtw.QLabel("Due?")
        due_lbl.setFont(fonts.BOLD)
        self._due_chk = qtw.QCheckBox()
        self._due_chk.setChecked(True)
        self._due_chk.stateChanged.connect(self._refresh_btn.click)  # noqa

        category_lbl = qtw.QLabel("Category")
        category_lbl.setFont(fonts.BOLD)

        user_lbl = qtw.QLabel("User")
        user_lbl.setFont(fonts.BOLD)

        description_lbl = qtw.QLabel("Description")
        description_lbl.setFont(fonts.BOLD)
        self._description_filter_txt = qtw.QLineEdit("")
        self._description_filter_txt.setMaximumWidth(200)

        toolbar_layout = qtw.QHBoxLayout()
        toolbar_layout.addWidget(self._refresh_btn)
        toolbar_layout.addWidget(self._add_btn)
        toolbar_layout.addSpacerItem(qtw.QSpacerItem(10, 0, qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Minimum))
        toolbar_layout.addWidget(due_lbl)
        toolbar_layout.addWidget(self._due_chk)
        toolbar_layout.addWidget(user_lbl)
        toolbar_layout.addWidget(self._user_selector)
        toolbar_layout.addWidget(category_lbl)
        toolbar_layout.addWidget(self._category_selector)
        toolbar_layout.addWidget(description_lbl)
        toolbar_layout.addWidget(self._description_filter_txt)
        toolbar_layout.addStretch()

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
                    width=200,
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
                    width=fm.width(" Edit "),
                    enabled_when=lambda todo: domain.permissions.user_can_edit_todo(
                        user=current_user,
                        todo=todo,
                    ),
                ),
                table_view.button(
                    name="delete",
                    button_text="Delete",
                    width=fm.width(" Delete "),
                    enabled_when=lambda todo: domain.permissions.user_can_edit_todo(
                        user=current_user,
                        todo=todo,
                    ),
                ),
            ),
            parent=self,
        )

        self._status_bar: typing.Final[StatusBar] = StatusBar(parent=self)

        layout = qtw.QVBoxLayout()
        layout.addLayout(toolbar_layout)
        layout.addWidget(self._table, stretch=2)
        layout.addWidget(self._status_bar)
        self.setLayout(layout)

        self._table.button_clicked.connect(self._on_button_clicked)
        self._table.double_click.connect(self._on_double_click)
        # noinspection PyUnresolvedReferences
        self._add_btn.clicked.connect(self._on_add_btn_clicked)
        # noinspection PyUnresolvedReferences
        self._refresh_btn.clicked.connect(self._on_refresh_btn_clicked)
        self._category_selector.item_selected.connect(self._refresh_btn.click)
        self._user_selector.item_selected.connect(self._refresh_btn.click)

    def get_state(self) -> TodoDashState:
        return TodoDashState(
            due_filter=self._due_chk.isChecked(),
            description_filter=self._description_filter_txt.text(),
            category_filter=self._category_selector.selected_item(),
            user_filter=self._user_selector.get_selected_item(),
            selected_todo=self._table.selected_item,
            todos=tuple(self._table.items),
            added_todo=None,
            updated_todo=None,
            deleted_todo=None,
            status=self._status_bar.message,
            categories_stale=False,
            users_stale=False,
        )

    def refresh(self) -> None:
        self._refresh_btn.click()

    def set_state(self, /, state: TodoDashState) -> None:
        try:
            if state.added_todo:
                self._table.add_item(state.added_todo)

            if isinstance(state.user_filter, domain.User):
                self._user_selector.select_item(state.user_filter)

            if state.users_stale is True:
                self._user_selector.refresh()

            if state.categories_stale is True:
                self._category_selector.refresh()

            if isinstance(state.category_filter, domain.Category):
                self._category_selector.select_item(state.category_filter)

            if state.categories_stale is True:
                self._category_selector.refresh()

            if isinstance(state.due_filter, bool):
                self._due_chk.setChecked(state.due_filter)

            if isinstance(state.description_filter, str):
                self._description_filter_txt.setText(state.description_filter)

            if state.deleted_todo:
                self._table.delete_item(key=state.deleted_todo.todo_id)

            if not isinstance(state.todos, domain.Unspecified):
                self._table.set_items(state.todos)

            if state.updated_todo:
                self._table.update_item(state.updated_todo)

            if isinstance(state.selected_todo, domain.Todo):
                self._table.select_item_by_key(key=state.selected_todo.todo_id)
            else:
                if state.selected_todo is None:
                    self._table.clear_selection()

            if isinstance(state.status, str):
                self._status_bar.set_status(state.status)

            self.repaint()
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.set_state(...) failed: {e}")

            self._status_bar.set_status(str(e))

    def _on_add_btn_clicked(self, /, _: bool) -> None:
        logger.debug(f"{self.__class__.__name__}.on_add_btn_clicked()")
        self._requests.add.emit()

    def _on_button_clicked(self, /, event: table_view.ButtonClickedEvent[domain.Todo, typing.Any]) -> None:
        logger.debug(f"{self.__class__.__name__}._on_button_clicked({event=!r})")

        match event.attr.name:
            case "delete":
                if domain.permissions.user_can_edit_todo(
                    user=self._current_user,
                    todo=event.item,
                ):
                    request = requests.DeleteTodo(todo=event.item)

                    self._requests.delete.emit(request)
            case "edit":
                if domain.permissions.user_can_edit_todo(
                    user=self._current_user,
                    todo=event.item,
                ):
                    self._requests.edit.emit(requests.EditTodo(todo=event.item))
            case "complete":
                self._requests.toggle_completed.emit(requests.ToggleCompleted(todo=event.item))
            case _:
                logger.error(f"attr name, {event.attr.name!r}, not recognized.")

    def _on_double_click(self, /, event: table_view.DoubleClickEvent[domain.Todo, typing.Any]) -> None:
        logger.debug(f"{self.__class__.__name__}._on_button_clicked({event=!r})")

        if domain.permissions.user_can_edit_todo(
            user=self._current_user,
            todo=event.item,
        ):
            edit_request = requests.EditTodo(todo=event.item)

            self._requests.edit.emit(edit_request)

    def _on_refresh_btn_clicked(self, /, _: bool) -> None:
        logger.debug(f"{self.__class__.__name__}._on_refresh_btn_clicked()")

        request = requests.RefreshRequest(
            is_due=self._due_chk.isChecked(),
            description=self._description_filter_txt.text(),
            category=self._category_selector.selected_item(),
            user=self._user_selector.get_selected_item(),
        )

        self._requests.refresh.emit(request)


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
