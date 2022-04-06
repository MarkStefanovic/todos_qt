import dataclasses
import logging

from src import domain
from src.presentation.shared.widgets import popup
from src.presentation.todo.form.state import TodoFormState
from src.presentation.todo.view import TodoView

__all__ = ("TodoController",)

logger = logging.getLogger()


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

        self._view.dash.add_btn.clicked.connect(self._on_dash_add_btn_clicked)
        self._view.dash.complete_btn_clicked.connect(self._on_dash_complete_btn_clicked)
        self._view.dash.delete_btn_clicked.connect(self._on_dash_delete_btn_clicked)
        self._view.dash.edit_btn_clicked.connect(self._on_dash_edit_btn_clicked)
        self._view.dash.incomplete_btn_clicked.connect(self._on_dash_incomplete_btn_clicked)
        self._view.dash.refresh_btn.clicked.connect(self._on_dash_refresh_btn_clicked)

        self._view.form.back_btn.clicked.connect(self._on_form_back_btn_clicked)
        self._view.form.save_btn.clicked.connect(self._on_form_save_btn_clicked)

    def _on_dash_add_btn_clicked(self) -> None:
        state = self._view.get_state()

        try:
            categories = self._category_service.all()

            users = self._user_service.all()

            new_state = dataclasses.replace(
                state,
                form_state=TodoFormState.initial(
                    category_options=categories,
                    user_options=users,
                ),
                dash_active=False,
            )
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

    def _on_dash_complete_btn_clicked(self) -> None:
        state = self._view.get_state()

        try:
            if todo := state.dash_state.selected_todo:
                self._todo_service.mark_complete(todo_id=todo.todo_id)

                todos = self._todo_service.get_where(
                    description_like=state.dash_state.description_filter,
                    date_filter=state.dash_state.date_filter,
                    due_filter=state.dash_state.due_filter,
                    category_filter=state.dash_state.category_filter,
                )

                new_state = dataclasses.replace(
                    state,
                    dash_state=dataclasses.replace(
                        state.dash_state,
                        todos=todos,
                        category_options=self._category_service.all(),
                        status=f"{todo.description} completed.",
                    ),
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

    def _on_dash_delete_btn_clicked(self) -> None:
        state = self._view.get_state()

        try:
            if todo := state.dash_state.selected_todo:
                if popup.confirm(question=f"Are you sure you want to delete {todo.description}?"):
                    self._todo_service.delete(todo_id=todo.todo_id)

                    todos = self._todo_service.get_where(
                        description_like=state.dash_state.description_filter,
                        date_filter=state.dash_state.date_filter,
                        due_filter=state.dash_state.due_filter,
                        category_filter=state.dash_state.category_filter,
                    )

                    new_state = dataclasses.replace(
                        state,
                        dash_state=dataclasses.replace(
                            state.dash_state,
                            todos=todos,
                            selected_todo=None,
                            category_options=self._category_service.all(),
                            status=f"{todo.description} deleted.",
                        ),
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

    def _on_dash_edit_btn_clicked(self) -> None:
        state = self._view.get_state()

        try:
            categories = self._category_service.all()

            users = self._user_service.all()

            if todo := state.dash_state.selected_todo:
                new_state = dataclasses.replace(
                    state,
                    form_state=TodoFormState.from_domain(
                        todo=todo,
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

    def _on_dash_incomplete_btn_clicked(self) -> None:
        state = self._view.get_state()

        try:
            if todo := state.dash_state.selected_todo:
                self._todo_service.mark_incomplete(todo_id=todo.todo_id)

                todos = self._todo_service.get_where(
                    description_like=state.dash_state.description_filter,
                    date_filter=state.dash_state.date_filter,
                    due_filter=state.dash_state.due_filter,
                    category_filter=state.dash_state.category_filter,
                )

                new_state = dataclasses.replace(
                    state,
                    dash_state=dataclasses.replace(
                        state.dash_state,
                        todos=todos,
                        category_options=self._category_service.all(),
                        status=f"{todo.description} set to incomplete.",
                    ),
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
        state = self._view.get_state()

        try:
            todos = self._todo_service.get_where(
                description_like=state.dash_state.description_filter,
                date_filter=state.dash_state.date_filter,
                due_filter=state.dash_state.due_filter,
                category_filter=state.dash_state.category_filter,
            )

            categories = self._category_service.all()

            new_state = dataclasses.replace(
                state,
                dash_state=dataclasses.replace(
                    state.dash_state,
                    todos=todos,
                    category_options=categories,
                    status="Refreshed.",
                )
            )
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

    def _on_form_back_btn_clicked(self) -> None:
        state = self._view.get_state()

        new_state = dataclasses.replace(state, dash_active=True)

        self._view.set_state(state=new_state)

    def _on_form_save_btn_clicked(self) -> None:
        state = self._view.get_state()
        try:
            todo = state.form_state.to_domain()

            self._todo_service.upsert(todo=todo)

            todos = self._todo_service.get_where(
                description_like=state.dash_state.description_filter,
                date_filter=state.dash_state.date_filter,
                due_filter=state.dash_state.due_filter,
                category_filter=state.dash_state.category_filter,
            )

            new_state = dataclasses.replace(
                state,
                dash_state=dataclasses.replace(
                    state.dash_state,
                    todos=todos,
                    selected_todo=todo,
                    category_options=self._category_service.all(),
                    status=f"{todo.description} added.",
                ),
                dash_active=True,
            )
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
