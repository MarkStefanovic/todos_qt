import typing

import qtawesome as qta
from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa
from loguru import logger

from src import domain
from src.presentation.category_selector import CategorySelectorWidget
from src.presentation.shared import fonts, icons
from src.presentation.shared.widgets import table_view, StatusBar
from src.presentation.todo import requests

__all__ = ("TodoDash",)

from src.presentation.todo.view.dash.state import TodoDashState

from src.presentation.user_selector import UserSelectorWidget


class TodoDash(qtw.QWidget):
    add_requests = qtc.pyqtSignal()
    delete_requests = qtc.pyqtSignal(requests.DeleteTodo)
    edit_requests = qtc.pyqtSignal(requests.EditTodo)
    refresh_requests = qtc.pyqtSignal()
    toggle_completed_requests = qtc.pyqtSignal(requests.ToggleCompleted)

    def __init__(
        self,
        *,
        category_selector: CategorySelectorWidget,
        user_selector: UserSelectorWidget,
        current_user: domain.User,
        parent: qtw.QWidget | None = None,
    ):
        super().__init__(parent=parent)

        self._category_selector: typing.Final[CategorySelectorWidget] = category_selector
        self._user_selector: typing.Final[UserSelectorWidget] = user_selector
        self._current_user: typing.Final[domain.User] = current_user

        refresh_btn_icon = qta.icon(
            icons.refresh_btn_icon_name,
            color=self.parent().palette().text().color(),  # type: ignore
        )
        self._refresh_btn = qtw.QPushButton(refresh_btn_icon, "Refresh")
        self._refresh_btn.setFont(fonts.BOLD)
        self._refresh_btn.setMaximumWidth(100)
        self._refresh_btn.setDefault(True)

        add_btn_icon = qta.icon(
            icons.add_btn_icon_name,
            color=self.parent().palette().text().color(),  # type: ignore
        )
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
                    width=fm.width(" Edit "),
                    enabled_selector=lambda todo: domain.permissions.user_can_edit_todo(
                        user=current_user,
                        todo=todo,
                    ),
                ),
                table_view.button(
                    name="delete",
                    button_text="Delete",
                    width=fm.width(" Delete "),
                    enabled_selector=lambda todo: domain.permissions.user_can_edit_todo(
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
        layout.addWidget(self._table)
        layout.addWidget(self._status_bar)
        self.setLayout(layout)

        self._table.button_clicked.connect(self._on_button_clicked)
        self._table.double_click.connect(self._on_double_click)
        # noinspection PyUnresolvedReferences
        self._add_btn.clicked.connect(lambda _: self.add_requests.emit())
        # noinspection PyUnresolvedReferences
        self._refresh_btn.clicked.connect(self._on_refresh_btn_clicked)
        self._category_selector.item_selected.connect(self._refresh_btn.click)
        self._user_selector.item_selected.connect(self._refresh_btn.click)

    def get_state(self) -> TodoDashState:
        return TodoDashState(
            due_filter=self._due_chk.isChecked(),
            description_filter=self._description_filter_txt.text(),
            category_filter=self._category_selector.get_selected_item(),
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

    def set_state(
        self,
        *,
        added_todo: domain.Todo | None = None,
        category_filter: domain.Category | domain.Unspecified = domain.Unspecified,
        categories_stale: bool | domain.Unspecified = domain.Unspecified,
        deleted_todo: domain.Todo | None = None,
        description_filter: str | domain.Unspecified = domain.Unspecified,
        due_filter: bool | domain.Unspecified = domain.Unspecified,
        selected_todo: domain.Todo | domain.Unspecified = domain.Unspecified,
        todos: tuple[domain.Todo, ...] | domain.Unspecified = domain.Unspecified,
        updated_todo: domain.Todo | None = None,
        user_filter: domain.User | domain.Unspecified = domain.Unspecified,
        users_stale: bool | domain.Unspecified = domain.Unspecified,
        status: str | domain.Unspecified = domain.Unspecified,
    ) -> None | domain.Error:
        try:
            if not isinstance(added_todo, domain.Unspecified):
                self._table.add_item(added_todo)

            if not isinstance(user_filter, domain.Unspecified):
                self._user_selector.select_item(user_filter)

            if not isinstance(users_stale, domain.Unspecified):
                self._user_selector.refresh()

            if not isinstance(category_filter, domain.Unspecified):
                self._category_selector.select_item(category_filter)

            if not isinstance(categories_stale, domain.Unspecified):
                if categories_stale:
                    self._category_selector.refresh()

            if not isinstance(due_filter, domain.Unspecified):
                self._due_chk.setChecked(due_filter)

            if not isinstance(description_filter, domain.Unspecified):
                self._description_filter_txt.setText(description_filter)

            if not isinstance(deleted_todo, domain.Unspecified):
                self._table.delete_item(key=deleted_todo.todo_id)

            if not isinstance(todos, domain.Unspecified):
                self._table.set_items(todos)

            if not isinstance(updated_todo, domain.Unspecified):
                self._table.update_item(updated_todo)

            if not isinstance(selected_todo, domain.Unspecified):
                selected_todo = selected_todo

                if selected_todo is None:
                    self._table.clear_selection()
                else:
                    self._table.select_item_by_key(key=selected_todo.todo_id)

            if not isinstance(status, domain.Unspecified):
                self._status_bar.showMessage(status)

            self.repaint()
        except Exception as e:
            return domain.Error.new(
                str(e),
                args={
                    "added_todo": added_todo,
                    "category_filter": category_filter,
                    "categories_stale": categories_stale,
                    "deleted_todo": deleted_todo,
                    "description_filter": description_filter,
                    "due_filter": due_filter,
                    "selected_todo": selected_todo,
                    "todos": todos,
                    "updated_todo": updated_todo,
                    "user_filter": user_filter,
                    "users_stale": users_stale,
                    "status": status,
                },
            )

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

    def _on_refresh_btn_clicked(self, /, _: bool) -> None:
        logger.debug(f"{self.__class__.__name__}._on_refresh_btn_clicked()")

        request = requests.RefreshRequest(
            is_due=self._due_chk.isChecked(),
            description=self._description_filter_txt.text(),
            category=self._category_selector.get_selected_item(),
            user=self._user_selector.get_selected_item(),
        )

        self.refresh_requests.emit(request)


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
