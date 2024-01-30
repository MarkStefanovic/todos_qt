import typing

# noinspection PyPep8Naming
from PyQt6 import QtCore as qtc
from loguru import logger

from src import domain
from src.presentation.shared.widgets import popup
from src.presentation.todo.state import TodoState
from src.presentation.todo.view import dash, form
from src.presentation.todo.view.form.state import TodoFormState

__all__ = ("TodoController",)


# noinspection DuplicatedCode
class TodoController(qtc.QObject):
    states = qtc.pyqtSignal(TodoState)

    def __init__(
        self,
        *,
        dash_requests: dash.requests.TodoDashRequests,
        form_requests: form.requests.TodoFormRequests,
        todo_service: domain.TodoService,
        current_user: domain.User,
    ):
        super().__init__()

        self._todo_service: typing.Final[domain.TodoService] = todo_service
        self._current_user: typing.Final[domain.User] = current_user
        self._dash_requests: typing.Final[dash.requests.TodoDashRequests] = dash_requests
        self._form_requests: typing.Final[form.requests.TodoFormRequests] = form_requests

        self._dash_requests.add.connect(self._on_add_request)
        self._dash_requests.toggle_completed.connect(self._on_toggle_completed_request)
        self._dash_requests.delete.connect(self._on_delete_request)
        self._dash_requests.edit.connect(self._on_edit_request)
        self._dash_requests.refresh.connect(self._on_refresh_request)
        self._form_requests.back.connect(self._on_back_request)
        self._form_requests.save.connect(self._on_save_request)

    def _on_add_request(self) -> None:
        logger.debug(f"{self.__class__.__name__}._on_add_request()")

        try:
            self.states.emit(
                TodoState(
                    dash_active=False,
                    form_state=TodoFormState.initial(current_user=self._current_user),
                )
            )
        except Exception as e:
            logger.error(f"{self.__class__.__name__}._on_add_request() failed: {e!s}")

            self._set_status(str(e))

    def _on_toggle_completed_request(self, /, request: dash.requests.ToggleCompleted) -> None:
        logger.debug(f"{self.__class__.__name__}._on_toggle_completed_request({request=!r})")

        try:
            if request.todo.should_display():
                self._todo_service.mark_complete(
                    todo_id=request.todo.todo_id,
                    user=self._current_user,
                )
                status = "complete"
            else:
                self._todo_service.mark_incomplete(todo_id=request.todo.todo_id)
                status = "incomplete"

            todo = self._todo_service.get(todo_id=request.todo.todo_id)
            if isinstance(todo, domain.Error):
                logger.error(f"{self.__class__.__name__}._on_toggle_completed_request({request=!r}) failed: {todo!s}")
                self._set_status(str(todo))
                return None

            if todo is None:
                return None

            self.states.emit(
                TodoState(
                    dash.TodoDashState(
                        updated_todo=todo,
                        status=f"{request.todo.description} marked {status}.",
                    )
                )
            )
        except Exception as e:
            logger.debug(f"{self.__class__.__name__}._on_toggle_completed_request({request=!r}) failed: {e!s}")

            self._set_status(str(e))

    def _on_delete_request(self, /, request: dash.requests.DeleteTodo) -> None:
        logger.debug(f"{self.__class__.__name__}._on_delete_request({request=!r})")

        try:
            delete_result = self._todo_service.delete(todo_id=request.todo.todo_id)
            if isinstance(delete_result, domain.Error):
                logger.error(f"{self.__class__.__name__}._on_delete_request({request=!r}): {delete_result!s}")
                self._set_status(delete_result.error_message)
                return None

            self.states.emit(
                TodoState(
                    dash_state=dash.TodoDashState(
                        deleted_todo=request.todo,
                        status=f"{request.todo.description} deleted.",
                    )
                )
            )
        except Exception as e:
            logger.error(f"{self.__class__.__name__}._on_delete_request({request=!r}) failed: {e!s}")

            self._set_status(str(e))

    def _on_edit_request(self, /, request: dash.requests.EditTodo) -> None:
        logger.debug(f"{self.__class__.__name__}._on_edit_request()")

        try:
            self.states.emit(
                TodoState(
                    form_state=TodoFormState.from_domain(todo=request.todo),
                    dash_active=False,
                )
            )
        except Exception as e:
            logger.error(f"{self.__class__.__name__}._on_edit_request({request=!r}) failed: {e!s}")

            self._set_status(str(e))

    def _on_refresh_request(self, /, request: dash.requests.RefreshRequest) -> None:
        logger.debug(f"{self.__class__.__name__}._on_refresh_request({request=!r})")

        try:
            self._set_status("Refreshing Todos...")

            if request.category:
                category_id: str | domain.Unspecified = request.category.category_id
            else:
                category_id = domain.Unspecified()

            if request.user:
                user_id: str | domain.Unspecified = request.user.user_id
            else:
                user_id = domain.Unspecified()

            todos = self._todo_service.where(
                description_like=request.description,
                due_filter=request.is_due,
                category_id_filter=category_id,
                user_id_filter=user_id,
            )
            # logger.info(f"{todos=!r}")
            if isinstance(todos, domain.Error):
                logger.error(f"{self.__class__.__name__}._on_refresh_request({request=!r}): {todos!s}")
                self._set_status(todos.error_message)
                return None

            self.states.emit(
                TodoState(
                    dash_state=dash.TodoDashState(
                        todos=tuple(todos),
                        status="Todos refreshed.",
                    )
                )
            )
        except Exception as e:
            logger.error(f"{self.__class__.__name__}._on_refresh_request({request=!r}) failed: {e!s}")

            self._set_status(str(e))

    def _on_back_request(self) -> None:
        logger.debug(f"{self.__class__.__name__}._on_back_request()")

        self.states.emit(TodoState(dash_active=True))

    def _on_save_request(self, /, request: form.requests.SaveRequest) -> None:
        logger.debug(f"{self.__class__.__name__}._on_save_request({request=!r})")

        try:
            validation_errors = request.todo.validation_errors()
            if validation_errors:
                popup.error_message(
                    message="\n".join(validation_errors),
                    title="Invalid Entry",
                )
                return None

            preexisting_todo = self._todo_service.get(todo_id=request.todo.todo_id)
            if isinstance(preexisting_todo, domain.Error):
                self._set_status(preexisting_todo.error_message)
                return None

            if preexisting_todo:
                update_result = self._todo_service.update(todo=request.todo)
                if isinstance(update_result, domain.Error):
                    self._set_status(update_result.error_message)
                    return None

                updated_todo = self._todo_service.get(todo_id=request.todo.todo_id)
                if isinstance(updated_todo, domain.Error):
                    self._set_status(updated_todo.error_message)
                    return None

                if updated_todo is None:
                    logger.error(
                        f"{self.__class__.__name__}._on_save_request({request=!r}): after update todo was not found "
                        f"in the database."
                    )
                    return None

                self.states.emit(
                    TodoState(
                        dash_state=dash.TodoDashState(
                            updated_todo=updated_todo,
                            status=f"Updated {request.todo.description}.",
                        ),
                        dash_active=True,
                    )
                )
            else:
                add_result = self._todo_service.add(todo=request.todo)
                if isinstance(add_result, domain.Error):
                    return None

                todo = self._todo_service.get(todo_id=request.todo.todo_id)
                if isinstance(todo, domain.Error):
                    return None

                if todo is None:
                    logger.error(
                        f"{self.__class__.__name__}._on_save_request({request=!r}): after adding todo it was not found "
                        f"in the database."
                    )
                    return None

                self.states.emit(
                    TodoState(
                        dash_state=dash.TodoDashState(
                            added_todo=todo,
                            status=f"Added {request.todo.description}.",
                        ),
                        dash_active=True,
                    )
                )
        except Exception as e:
            logger.error(f"{self.__class__.__name__}._on_save_request({request=!r}) failed: {e!s}")

            popup.error_message(message=str(e))

    def _set_status(self, /, status: str) -> None:
        self.states.emit(TodoState.set_status(status))
