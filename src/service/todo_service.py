import datetime
import typing

from src import domain

from src.service import unit_of_work

__all__ = ("TodoService",)


class TodoService:
    def __init__(self, /, uow: unit_of_work.TodoUnitOfWork):
        self._uow = uow

    def add_todo(self, /, todo: domain.Todo) -> None:
        with self._uow as uow:
            uow.todo_repository.add(todo)
            uow.save()

    def current_todos(
        self, /, today: datetime.date = datetime.date.today()
    ) -> typing.List[domain.Todo]:
        with self._uow as uow:
            return get_todos(uow=uow, today=today, category="todo")

    def current_reminders(
        self, /, today: datetime.date = datetime.date.today()
    ) -> typing.List[domain.Todo]:
        with self._uow as uow:
            return get_todos(uow=uow, today=today, category="reminder")

    def delete_todo(self, /, todo_id: int) -> None:
        with self._uow as uow:
            uow.todo_repository.remove(todo_id)
            uow.save()

    def get_id(self, todo_id: int) -> domain.Todo:
        assert todo_id > 0, f"Todo id values should be positive, but got {todo_id!r}."
        with self._uow as uow:
            return uow.todo_repository.get_id(todo_id)

    def mark_complete(self, /, todo_id: int) -> None:
        with self._uow as uow:
            uow.todo_repository.mark_completed(todo_id)
            uow.save()

    def update_todo(self, /, todo: domain.Todo) -> None:
        with self._uow as uow:
            uow.todo_repository.update(todo)
            uow.save()


def get_todos(
    *,
    uow: unit_of_work.TodoUnitOfWork,
    category: str,
    today: datetime.date = datetime.date.today(),
) -> typing.List[domain.Todo]:
    return [
        todo
        for todo in uow.todo_repository.all()
        if todo.display(today) and todo.category == category
    ]
