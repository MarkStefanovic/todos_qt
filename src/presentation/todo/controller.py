import logging
import typing

from src import domain, service
from src.presentation.shared.widgets import popup
from src.presentation.todo import requests
from src.presentation.todo.view.form.state import TodoFormState
from src.presentation.todo.view.view import TodoView

__all__ = ("TodoController",)

logger = logging.getLogger()


# noinspection DuplicatedCode
class TodoController:
    def __init__(
        self,
        *,
        todo_service: domain.TodoService,
        current_user: domain.User,
        view: TodoView,
    ):
        self._todo_service: typing.Final[service.TodoService] = todo_service
        self._current_user: typing.Final[domain.User] = current_user
        self._view: typing.Final[TodoView] = view

        self._view.dash.add_requests.connect(self._on_dash_add_btn_clicked)
        self._view.dash.toggle_completed_requests.connect(self._on_dash_toggle_completed)
        self._view.dash.delete_requests.connect(self._on_dash_delete_btn_clicked)
        self._view.dash.edit_requests.connect(self._on_dash_edit_btn_clicked)
        self._view.dash.refresh_requests.connect(self._on_dash_refresh_btn_clicked)

        self._view.form.back_requests.connect(self._on_form_back_btn_clicked)
        self._view.form.save_requests.connect(self._on_form_save_btn_clicked)

    def _on_dash_add_btn_clicked(self) -> None:
        logger.debug(f"{self.__class__.__name__}._on_dash_add_btn_clicked()")

        try:
            self._view.set_state(
                dash_active=False,
                form_state=TodoFormState.initial(current_user=self._current_user),
            )
        except Exception as e:
            logger.exception(e)

            self._view.dash.set_state(status=str(e))

    def _on_dash_toggle_completed(self, /, event: requests.ToggleCompleted) -> None:
        logger.debug(f"{self.__class__.__name__}._on_dash_toggle_completed({event=!r})")

        try:
            if event.todo.should_display():
                self._todo_service.mark_complete(
                    todo_id=event.todo.todo_id,
                    user=self._current_user,
                )
                status = "complete"
            else:
                self._todo_service.mark_incomplete(todo_id=event.todo.todo_id)
                status = "incomplete"

            todo = self._todo_service.get(todo_id=event.todo.todo_id)
            if isinstance(todo, domain.Error):
                logger.error(f"{self.__class__.__name__}._on_dash_toggle_completed({event=!r}) failed: {todo!s}")
                self._view.dash.set_state(status=str(todo))
                return None

            self._view.dash.set_state(
                updated_todo=todo,
                status=f"{event.todo.description} marked {status}.",
            )
        except Exception as e:
            logger.exception(e)
            self._view.dash.set_state(status=str(e))

    def _on_dash_delete_btn_clicked(self, /, event: requests.DeleteTodo) -> None:
        logger.debug(f"{self.__class__.__name__}._on_dash_delete_btn_clicked({event=!r})")

        try:
            if popup.confirm(question=f"Are you sure you want to delete {event.todo.description}?"):
                self._todo_service.delete(todo_id=event.todo.todo_id)

                self._view.dash.set_state(
                    deleted_todo=event.todo,
                    status=f"{event.todo.description} deleted.",
                )
        except Exception as e:
            logger.exception(e)
            self._view.dash.set_state(status=str(e))

    def _on_dash_edit_btn_clicked(self, /, event: requests.EditTodo) -> None:
        logger.debug(f"{self.__class__.__name__}._on_dash_edit_btn_clicked()")

        try:
            form_state = TodoFormState.from_domain(todo=event.todo)

            self._view.set_state(
                form_state=form_state,
                dash_active=False,
            )
        except Exception as e:
            logger.exception(e)

            self._view.dash.set_state(status=str(e))

    def _on_dash_refresh_btn_clicked(self, /, event: requests.RefreshRequest) -> None:
        logger.debug(f"{self.__class__.__name__}._on_dash_refresh_btn_clicked({event=!r})")

        try:
            todos = self._todo_service.where(
                description_like=event.description,
                due_filter=event.is_due,
                category_id_filter=event.category.category_id,
                user_id_filter=event.user.user_id,
            )

            self._view.dash.set_state(
                todos=tuple(todos),
                categories_stale=True,
                users_stale=True,
                status="Todos refreshed.",
            )
        except Exception as e:
            logger.error(f"{self.__class__.__name__}._on_dash_refresh_btn_clicked({event=!r}) failed: {e!s}")

            self._view.dash.set_state(status=str(e))

    def _on_form_back_btn_clicked(self) -> None:
        logger.debug(f"{self.__class__.__name__}._on_form_back_btn_clicked()")

        self._view.set_state(dash_active=True)

    def _on_form_save_btn_clicked(self, /, event: requests.SaveRequest) -> None:
        logger.debug(f"{self.__class__.__name__}._on_form_save_btn_clicked({event=!r})")

        try:
            error_messages: list[str] = []
            if event.todo.frequency.name == domain.FrequencyType.Daily:
                if event.todo.frequency.advance_display_days > 0:
                    error_messages.append("Advance display days must be 0.")
                if event.todo.frequency.expire_display_days > 1:
                    error_messages.append("Expire days must be less than 1.")
            elif event.todo.frequency.name == domain.FrequencyType.Irregular:
                if event.todo.frequency.advance_display_days > 363:
                    error_messages.append("Advance display days must be less than 364.")
                if event.todo.frequency.expire_display_days > 363:
                    error_messages.append("Expire days must be less than 364.")
            elif event.todo.frequency.name == domain.FrequencyType.Monthly:
                if event.todo.frequency.advance_display_days > 27:
                    error_messages.append("Advance display days must be less than 28.")
                if event.todo.frequency.expire_display_days > 27:
                    error_messages.append("Expire days must be less than 28.")
            elif event.todo.frequency.name == domain.FrequencyType.XDays:
                assert event.todo.frequency.days is not None
                if event.todo.frequency.advance_display_days > event.todo.frequency.days:
                    error_messages.append("Advance display days must be less than the number of days between.")
                if event.todo.frequency.expire_display_days > event.todo.frequency.days:
                    error_messages.append("Expire days must be less than the days between.")
            elif event.todo.frequency.name == domain.FrequencyType.Yearly:
                if event.todo.frequency.advance_display_days > 363:
                    error_messages.append("Advance display days must be less than 364.")
                if event.todo.frequency.expire_display_days > 363:
                    error_messages.append("Expire days must be less than 364.")

            if error_messages:
                popup.error_message(
                    message="\n".join(error_messages),
                    title="Invalid Entry",
                )
            else:
                if updated_todo := self._todo_service.get(todo_id=event.todo.todo_id):
                    self._todo_service.update(todo=event.todo)
                    self._view.dash.set_state(
                        updated_todo=updated_todo,
                        status=f"{event.todo.description} updated.",
                    )
                else:
                    self._todo_service.add(todo=event.todo)
                    todo = self._todo_service.get(todo_id=event.todo.todo_id)

                    self._view.dash.set_state(
                        todo_added=todo,
                        status=f"{event.todo.description} added.",
                    )

                self._view.set_state(dash_active=True)
        except Exception as e:
            logger.error(f"{self.__class__.__name__}._on_form_save_btn_clicked({event=!r}) failed: {e!s}")

            popup.error_message(message=str(e))
