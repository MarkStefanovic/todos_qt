import typing

from src import service, domain
from src.presentation import widgets
from src.presentation.todo import todo_edit_form

__all__ = ("TodoListViewModel",)


class TodoListViewModel(widgets.ListViewModel):
    def __init__(
        self, todo_service: service.TodoService, category: domain.TodoCategory
    ):
        super().__init__([
            "id",
            "Description",
            "Frequency",
            "Days",
            "Day",
            "Due",
            "Completed",
        ])

        self._todo_service = todo_service
        self._category = category

    def fetch_data(self) -> typing.List[typing.List[typing.Any]]:
        return [
            [
                row.todo_id,
                row.description,
                str(row.frequency),
                str(row.days_until()),
                row.current_date().strftime("%a"),
                row.current_date().strftime("%Y-%m-%d"),
                row.date_completed.strftime("%Y-%m-%d") if row.date_completed else "",
            ]
            for row in self._todo_service.get_current_todos(category=self._category)
        ]

    def delete(self, /, todo_id: int) -> None:
        self._todo_service.delete_todo(todo_id)
        super().delete(todo_id)

    def mark_complete(self, /, todo_id: int) -> None:
        if row_num := self.get_row_number(todo_id=todo_id):
            self._todo_service.mark_complete(todo_id)
            self.removeRows(row_num, 1)

    def get_todo(self, /, todo_id: int) -> domain.Todo:
        return self._todo_service.get_id(todo_id)

    def create_add_todo_form_model(self) -> todo_edit_form.TodoEditFormModel:
        return todo_edit_form.TodoEditFormModel(
            edit_mode=domain.EditMode.ADD,
            todo_service=self._todo_service,
            todo_id=None,
        )

    def create_edit_todo_form_model(
        self, todo_id: int
    ) -> todo_edit_form.TodoEditFormModel:
        return todo_edit_form.TodoEditFormModel(
            edit_mode=domain.EditMode.EDIT,
            todo_service=self._todo_service,
            todo_id=todo_id,
        )
