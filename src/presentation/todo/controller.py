import dataclasses
import datetime
import logging

from src import domain
from src.presentation.shared.widgets import popup
from src.presentation.todo import requests
from src.presentation.todo.view.view import TodoView

__all__ = ("TodoController",)

logger = logging.getLogger()


# noinspection DuplicatedCode
class TodoController:
    def __init__(
        self,
        *,
        category_service: domain.CategoryService,
        todo_service: domain.TodoService,
        user_service: domain.UserService,
        view: TodoView,
    ):
        self._todo_service = todo_service
        self._category_service = category_service
        self._user_service = user_service
        self._view = view

        self._view.dash.add_requests.connect(self._on_dash_add_btn_clicked)
        self._view.dash.toggle_completed_requests.connect(self._on_dash_toggle_completed)
        self._view.dash.delete_requests.connect(self._on_dash_delete_btn_clicked)
        self._view.dash.edit_requests.connect(self._on_dash_edit_btn_clicked)
        self._view.dash.refresh_requests.connect(self._on_dash_refresh_btn_clicked)

        self._view.form.back_requests.connect(self._on_form_back_btn_clicked)
        self._view.form.save_requests.connect(self._on_form_save_btn_clicked)

    def show_current_todos(self) -> None:
        try:
            categories = self._category_service.all()

            users = self._user_service.all()

            todos = self._todo_service.where(
                due_filter=True,
                description_like="",
                category_id_filter=None,
                user_id_filter=None,
            )

            self._view.dash.set_items(todos)
        except Exception as e:
            logger.exception(e)

            self._view.dash.set_status

    def show_current_user_todos(self) -> None:
        state = self._view.get_state()

        try:
            categories = self._category_service.all()

            users = self._user_service.all()

            current_user = self._user_service.current_user()

            todos = self._todo_service.where(
                due_filter=True,
                description_like="",
                category_id_filter=None,
                user_id_filter=current_user.user_id,
            )

            if current_user is None:
                status = "Showing ToDos for all users."
            else:
                status = f"Showing ToDos for {current_user.display_name}."

            new_state = dataclasses.replace(
                state,
                dash_state=dataclasses.replace(
                    state.dash_state,
                    todos=todos,
                    category_options=categories,
                    category_filter=ALL_CATEGORY,
                    user_options=users,
                    user_filter=current_user or ALL_USER,
                    description_filter="",
                    due_filter=True,
                    status=status,
                ),
                dash_active=True,
            )
        except Exception as e:
            logger.exception(e)
            new_state = dataclasses.replace(
                state,
                dash_state=dataclasses.replace(
                    state.dash_state,
                    status=_add_timestamp(message=str(e)),
                ),
                dash_active=True,
            )

        self._view.set_state(state=new_state)

    def _on_dash_add_btn_clicked(self) -> None:
        logger.debug(f"{self.__class__.__name__}._on_dash_add_btn_clicked()")

        state = self._view.get_state()

        try:
            categories = self._category_service.all()

            users = self._user_service.all()

            new_state = dataclasses.replace(
                state,
                form_state=TodoFormState.initial(
                    category_options=categories,
                    user_options=users,
                    current_user=self._user_service.current_user(),
                ),
                dash_active=False,
            )
        except Exception as e:
            logger.exception(e)
            new_state = dataclasses.replace(
                state,
                dash_state=dataclasses.replace(
                    state.dash_state,
                    status=_add_timestamp(message=str(e)),
                ),
            )

        self._view.set_state(state=new_state)

    def _on_dash_toggle_completed(self, /, event: requests.ToggleCompleted) -> None:
        logger.debug(f"{self.__class__.__name__}._on_dash_toggle_completed_btn_clicked()")

        state = self._view.get_state()

        try:
            current_user = self._user_service.current_user()

            if event.todo.should_display():
                self._todo_service.mark_complete(todo_id=event.todo.todo_id, user=current_user)
            else:
                self._todo_service.mark_incomplete(todo_id=event.todo.todo_id)

            if state.dash_state.category_filter == ALL_CATEGORY:
                category_id_filter = None
            else:
                category_id_filter = state.dash_state.category_filter.category_id

            if state.dash_state.user_filter == ALL_USER:
                user_id_filter = None
            else:
                user_id_filter = state.dash_state.user_filter.user_id

            todos = self._todo_service.where(
                description_like=state.dash_state.description_filter,
                due_filter=state.dash_state.due_filter,
                category_id_filter=category_id_filter,
                user_id_filter=user_id_filter,
            )

            new_state = dataclasses.replace(
                state,
                dash_state=dataclasses.replace(
                    state.dash_state,
                    todos=todos,
                    category_options=self._category_service.all(),
                    status=_add_timestamp(message=f"{event.todo.description} completed."),
                ),
            )

            self._view.set_state(state=new_state)
        except Exception as e:
            logger.exception(e)
            new_state = dataclasses.replace(
                state,
                dash_state=dataclasses.replace(
                    state.dash_state,
                    status=_add_timestamp(message=str(e)),
                ),
            )

            self._view.set_state(state=new_state)

    def _on_dash_delete_btn_clicked(self, /, event: requests.DeleteTodo) -> None:
        logger.debug(f"{self.__class__.__name__}._on_dash_delete_btn_clicked()")

        state = self._view.get_state()

        try:
            if popup.confirm(question=f"Are you sure you want to delete {event.todo.description}?"):
                self._todo_service.delete(todo_id=event.todo.todo_id)

                if state.dash_state.category_filter == ALL_CATEGORY:
                    category_id_filter = None
                else:
                    category_id_filter = state.dash_state.category_filter.category_id

                if state.dash_state.user_filter == ALL_USER:
                    user_id_filter = None
                else:
                    user_id_filter = state.dash_state.user_filter.user_id

                todos = self._todo_service.where(
                    description_like=state.dash_state.description_filter,
                    due_filter=state.dash_state.due_filter,
                    category_id_filter=category_id_filter,
                    user_id_filter=user_id_filter,
                )

                new_state = dataclasses.replace(
                    state,
                    dash_state=dataclasses.replace(
                        state.dash_state,
                        todos=todos,
                        selected_todo=None,
                        category_options=self._category_service.all(),
                        status=_add_timestamp(message=f"{event.todo.description} deleted."),
                    ),
                )

                self._view.set_state(state=new_state)
        except Exception as e:
            logger.exception(e)
            new_state = dataclasses.replace(
                state,
                dash_state=dataclasses.replace(
                    state.dash_state,
                    status=_add_timestamp(message=str(e)),
                ),
            )

            self._view.set_state(state=new_state)

    def _on_dash_edit_btn_clicked(self, /, event: requests.EditTodo) -> None:
        logger.debug(f"{self.__class__.__name__}._on_dash_edit_btn_clicked()")

        state = self._view.get_state()

        try:
            categories = self._category_service.all()

            users = self._user_service.all()

            new_state = dataclasses.replace(
                state,
                form_state=TodoFormState.from_domain(
                    todo=event.todo,
                    category_options=categories,
                    user_options=users,
                ),
                dash_active=False,
            )

            self._view.set_state(state=new_state)
        except Exception as e:
            logger.exception(e)
            new_state = dataclasses.replace(
                state,
                dash_state=dataclasses.replace(
                    state.dash_state,
                    status=str(e),
                ),
            )

            self._view.set_state(state=new_state)

    def _on_dash_refresh_btn_clicked(self) -> None:
        logger.debug(f"{self.__class__.__name__}._on_dash_refresh_btn_clicked()")

        state = self._view.get_state()

        try:
            if state.dash_state.category_filter == ALL_CATEGORY:
                category_id_filter = None
            else:
                category_id_filter = state.dash_state.category_filter.category_id

            if state.dash_state.user_filter == ALL_USER:
                user_id_filter = None
            else:
                user_id_filter = state.dash_state.user_filter.user_id

            todos = self._todo_service.where(
                description_like=state.dash_state.description_filter,
                due_filter=state.dash_state.due_filter,
                category_id_filter=category_id_filter,
                user_id_filter=user_id_filter,
            )

            categories = self._category_service.all()

            users = self._user_service.all()

            new_state = dataclasses.replace(
                state,
                dash_state=dataclasses.replace(
                    state.dash_state,
                    todos=todos,
                    category_options=categories,
                    user_options=users,
                    status=_add_timestamp(message="Refreshed."),
                    current_user=self._user_service.current_user(),
                ),
            )
        except Exception as e:
            logger.exception(e)
            new_state = dataclasses.replace(
                state,
                dash_state=dataclasses.replace(
                    state.dash_state,
                    status=_add_timestamp(message=str(e)),
                ),
            )

        self._view.set_state(state=new_state)

    def _on_form_back_btn_clicked(self) -> None:
        logger.debug(f"{self.__class__.__name__}._on_form_back_btn_clicked()")

        state = self._view.get_state()

        new_state = dataclasses.replace(state, dash_active=True)

        self._view.set_state(state=new_state)

    def _on_form_save_btn_clicked(self) -> None:
        logger.debug(f"{self.__class__.__name__}._on_form_save_btn_clicked()")

        state = self._view.get_state()
        try:
            todo = state.form_state.to_domain()

            error_messages: list[str] = []
            if todo.frequency.name == domain.FrequencyType.Daily:
                if todo.frequency.advance_display_days > 0:
                    error_messages.append("Advance display days must be 0.")
                if todo.frequency.expire_display_days > 1:
                    error_messages.append("Expire days must be less than 1.")
            elif todo.frequency.name == domain.FrequencyType.Irregular:
                if todo.frequency.advance_display_days > 363:
                    error_messages.append("Advance display days must be less than 364.")
                if todo.frequency.expire_display_days > 363:
                    error_messages.append("Expire days must be less than 364.")
            elif todo.frequency.name == domain.FrequencyType.Monthly:
                if todo.frequency.advance_display_days > 27:
                    error_messages.append("Advance display days must be less than 28.")
                if todo.frequency.expire_display_days > 27:
                    error_messages.append("Expire days must be less than 28.")
            elif todo.frequency.name == domain.FrequencyType.XDays:
                assert todo.frequency.days is not None
                if todo.frequency.advance_display_days > todo.frequency.days:
                    error_messages.append("Advance display days must be less than the number of days between.")
                if todo.frequency.expire_display_days > todo.frequency.days:
                    error_messages.append("Expire days must be less than the days between.")
            elif todo.frequency.name == domain.FrequencyType.Yearly:
                if todo.frequency.advance_display_days > 363:
                    error_messages.append("Advance display days must be less than 364.")
                if todo.frequency.expire_display_days > 363:
                    error_messages.append("Expire days must be less than 364.")

            if error_messages:
                popup.error_message(
                    message="\n".join(error_messages),
                    title="Invalid Entry",
                )
            else:
                if self._todo_service.get(todo_id=todo.todo_id):
                    self._todo_service.update(todo=todo)
                    status = f"{todo.description} updated."
                else:
                    self._todo_service.add(todo=todo)
                    status = f"{todo.description} added."

                if state.dash_state.category_filter == ALL_CATEGORY:
                    category_id_filter = None
                else:
                    category_id_filter = state.dash_state.category_filter.category_id

                if state.dash_state.user_filter == ALL_USER:
                    user_id_filter = None
                else:
                    user_id_filter = state.dash_state.user_filter.user_id

                todos = self._todo_service.where(
                    description_like=state.dash_state.description_filter,
                    due_filter=state.dash_state.due_filter,
                    category_id_filter=category_id_filter,
                    user_id_filter=user_id_filter,
                )

                new_state = dataclasses.replace(
                    state,
                    dash_state=dataclasses.replace(
                        state.dash_state,
                        todos=todos,
                        selected_todo=todo,
                        category_options=self._category_service.all(),
                        status=_add_timestamp(message=status),
                    ),
                    dash_active=True,
                )

                self._view.set_state(state=new_state)
        except Exception as e:
            logger.exception(e)

            new_state = dataclasses.replace(
                state,
                dash_state=dataclasses.replace(
                    state.dash_state,
                    status=str(e),
                ),
            )

            self._view.set_state(state=new_state)


def _add_timestamp(*, message: str) -> str:
    ts_str = datetime.datetime.now().strftime("%m/%d @ %I:%M %p")
    return f"{ts_str}: {message}"
