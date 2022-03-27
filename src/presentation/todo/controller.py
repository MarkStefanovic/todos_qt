import dataclasses

from src import domain
from src.presentation.shared.widgets import popup
from src.presentation.todo.form.state import TodoFormState
from src.presentation.todo.view import TodoView

__all__ = ("TodoController",)


class TodoController:
    def __init__(self, *, todo_service: domain.TodoService, view: TodoView):
        self._todo_service = todo_service
        self._view = view

        self._view.dash.add_btn.clicked.connect(self._on_dash_add_btn_clicked)
        self._view.dash.complete_btn_clicked.connect(self._on_dash_complete_btn_clicked)
        self._view.dash.delete_btn_clicked.connect(self._on_dash_delete_btn_clicked)
        self._view.dash.edit_btn_clicked.connect(self._on_dash_edit_btn_clicked)
        self._view.dash.incomplete_btn_clicked.connect(self._on_dash_incomplete_btn_clicked)
        self._view.dash.refresh_btn.clicked.connect(self._on_dash_refresh_btn_clicked)

        self._view.form.back_btn.clicked.connect(self._on_form_back_btn_clicked)
        self._view.form.save_btn.clicked.connect(self._on_form_save_btn_clicked)

        self._on_dash_refresh_btn_clicked()

    def _on_dash_add_btn_clicked(self) -> None:
        state = self._view.get_state()

        new_state = dataclasses.replace(
            state,
            form_state=TodoFormState.initial(),
            dash_active=False,
        )

        self._view.set_state(state=new_state)

    def _on_dash_complete_btn_clicked(self) -> None:
        state = self._view.get_state()

        if todo := state.dash_state.selected_todo:
            self._todo_service.mark_complete(todo_id=todo.todo_id)

            todos = self._todo_service.get_where(
                description_like=state.dash_state.description_filter,
                date_filter=state.dash_state.date_filter,
                due_filter=state.dash_state.due_filter,
            )

            new_state = dataclasses.replace(
                state,
                dash_state=dataclasses.replace(state.dash_state, todos=todos),
            )

            self._view.set_state(state=new_state)

    def _on_dash_delete_btn_clicked(self) -> None:
        state = self._view.get_state()

        if todo := state.dash_state.selected_todo:
            if popup.confirm(question=f"Are you sure you want to delete {todo.description}?"):
                self._todo_service.delete(todo_id=todo.todo_id)

            todos = self._todo_service.get_where(
                description_like=state.dash_state.description_filter,
                date_filter=state.dash_state.date_filter,
                due_filter=state.dash_state.due_filter,
            )

            new_state = dataclasses.replace(
                state,
                dash_state=dataclasses.replace(
                    state.dash_state,
                    todos=todos,
                    selected_todo=None,
                ),
            )

            self._view.set_state(state=new_state)

    def _on_dash_edit_btn_clicked(self) -> None:
        state = self._view.get_state()

        if todo := state.dash_state.selected_todo:
            new_state = dataclasses.replace(
                state,
                form_state=TodoFormState.from_domain(todo=todo),
                dash_active=False,
            )

            self._view.set_state(state=new_state)

    def _on_dash_incomplete_btn_clicked(self) -> None:
        state = self._view.get_state()

        if todo := state.dash_state.selected_todo:
            self._todo_service.mark_incomplete(todo_id=todo.todo_id)

            todos = self._todo_service.get_where(
                description_like=state.dash_state.description_filter,
                date_filter=state.dash_state.date_filter,
                due_filter=state.dash_state.due_filter,
            )

            new_state = dataclasses.replace(
                state,
                dash_state=dataclasses.replace(state.dash_state, todos=todos),
            )

            self._view.set_state(state=new_state)

    def _on_dash_refresh_btn_clicked(self) -> None:
        state = self._view.get_state()

        todos = self._todo_service.get_where(
            description_like=state.dash_state.description_filter,
            date_filter=state.dash_state.date_filter,
            due_filter=state.dash_state.due_filter,
        )

        new_state = dataclasses.replace(
            state,
            dash_state=dataclasses.replace(
                state.dash_state,
                todos=todos,
            )
        )

        self._view.set_state(state=new_state)

    def _on_form_back_btn_clicked(self) -> None:
        state = self._view.get_state()

        new_state = dataclasses.replace(state, dash_active=True)

        self._view.set_state(state=new_state)

    def _on_form_save_btn_clicked(self) -> None:
        state = self._view.get_state()

        todo = state.form_state.to_domain()

        self._todo_service.upsert(todo=todo)

        todos = self._todo_service.get_where(
            description_like=state.dash_state.description_filter,
            date_filter=state.dash_state.date_filter,
            due_filter=state.dash_state.due_filter,
        )

        new_state = dataclasses.replace(
            state,
            dash_state=dataclasses.replace(
                state.dash_state,
                todos=todos,
                selected_todo=todo,
            ),
            dash_active=True,
        )

        self._view.set_state(state=new_state)
