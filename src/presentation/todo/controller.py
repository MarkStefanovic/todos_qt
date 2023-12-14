import logging
import typing

from src import domain, service
from src.presentation.shared.widgets import popup
from src.presentation.todo import requests
from src.presentation.todo.state import TodoState
from src.presentation.todo.view.form.state import TodoFormState

# noinspection PyPep8Naming
from PyQt5 import QtCore as qtc

__all__ = ("TodoController",)

logger = logging.getLogger()


# noinspection DuplicatedCode
class TodoController:
    states = qtc.pyqtSignal(TodoState)

    def __init__(
        self,
        *,
        todo_requests: requests.TodoRequests,
        todo_service: domain.TodoService,
        current_user: domain.User,
    ):
        self._todo_service: typing.Final[service.TodoService] = todo_service
        self._current_user: typing.Final[domain.User] = current_user
        self._todo_requests: typing.Final[requests.TodoRequests] = todo_requests

        self._todo_requests.add.connect(self._on_add_request)
        self._todo_requests.toggle_completed.connect(self._on_toggle_completed_request)
        self._todo_requests.delete.connect(self._on_delete_request)
        self._todo_requests.edit.connect(self._on_edit_request)
        self._todo_requests.refresh.connect(self._on_refresh_request)
        self._todo_requests.back.connect(self._on_back_request)
        self._todo_requests.save.connect(self._on_save_request)

    def _on_add_request(self) -> None:
        logger.debug(f"{self.__class__.__name__}._on_add_request()")

        try:
            state = TodoState(
                dash_active=False,
                form_state=TodoFormState.initial(current_user=self._current_user),
            )
        except Exception as e:
            logger.error(f"{self.__class__.__name__}._on_add_request() failed: {e!s}")

            state = TodoState.set_status(str(e))

        self.states.emit(state)

    def _on_toggle_completed_request(self, /, event: requests.ToggleCompleted) -> None:
        logger.debug(f"{self.__class__.__name__}._on_toggle_completed_request({event=!r})")

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
                logger.error(f"{self.__class__.__name__}._on_toggle_completed_request({event=!r}) failed: {todo!s}")
                self._view.dash.set_state(status=str(todo))
                return None

            self._view.dash.set_state(
                updated_todo=todo,
                status=f"{event.todo.description} marked {status}.",
            )
        except Exception as e:
            logger.debug(f"{self.__class__.__name__}._on_toggle_completed_request({event=!r}) failed: {e!s}")

            self._view.dash.set_state(status=str(e))

    def _on_delete_request(self, /, event: requests.DeleteTodo) -> None:
        logger.debug(f"{self.__class__.__name__}._on_delete_request({event=!r})")

        try:
            if popup.confirm(question=f"Are you sure you want to delete {event.todo.description}?"):
                self._todo_service.delete(todo_id=event.todo.todo_id)

                self._view.dash.set_state(
                    deleted_todo=event.todo,
                    status=f"{event.todo.description} deleted.",
                )
        except Exception as e:
            logger.error(f"{self.__class__.__name__}._on_delete_request({event=!r}) failed: {e!s}")

            self._view.dash.set_state(status=str(e))

    def _on_edit_request(self, /, event: requests.EditTodo) -> None:
        logger.debug(f"{self.__class__.__name__}._on_edit_request()")

        try:
            form_state = TodoFormState.from_domain(todo=event.todo)

            self._view.set_state(
                form_state=form_state,
                dash_active=False,
            )
        except Exception as e:
            logger.error(f"{self.__class__.__name__}._on_edit_request() failed: {e!s}")

            self._view.dash.set_state(status=str(e))

    def _on_refresh_request(self, /, event: requests.RefreshRequest) -> None:
        logger.debug(f"{self.__class__.__name__}._on_refresh_request({event=!r})")

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
            logger.error(f"{self.__class__.__name__}._on_refresh_request({event=!r}) failed: {e!s}")

            self._view.dash.set_state(status=str(e))

    def _on_back_request(self) -> None:
        logger.debug(f"{self.__class__.__name__}._on_back_request()")

        self._view.set_state(dash_active=True)

    def _on_save_request(self, /, event: requests.SaveRequest) -> None:
        logger.debug(f"{self.__class__.__name__}._on_save_request({event=!r})")

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
            logger.error(f"{self.__class__.__name__}._on_save_request({event=!r}) failed: {e!s}")

            popup.error_message(message=str(e))
