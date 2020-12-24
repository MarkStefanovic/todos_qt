import dataclasses
import datetime
import typing

import src.domain.todo_unit_of_work
from src import domain

__all__ = ("TodoService",)


class TodoService:
    def __init__(self, /, uow: src.domain.todo_unit_of_work.TodoUnitOfWork):
        self._uow = uow

    def all(self) -> typing.List[domain.Todo]:
        with self._uow as uow:
            return uow.todo_repository.all()

    def add_todo(self, /, todo: domain.Todo) -> None:
        new_todo = dataclasses.replace(todo, date_added=datetime.date.today())
        with self._uow as uow:
            uow.todo_repository.add(new_todo)
            uow.save()

    def delete_todo(self, /, todo_id: int) -> None:
        with self._uow as uow:
            uow.todo_repository.remove(todo_id)
            uow.save()

    def get_by_id(self, todo_id: int) -> domain.Todo:
        assert todo_id > 0, f"Todo id values should be positive, but got {todo_id!r}."
        return next(todo for todo in self.all() if todo.todo_id == todo_id)

    def get_current_todos(
        self,
        *,
        category: str,
        today: datetime.date = datetime.date.today(),
    ) -> typing.List[domain.Todo]:
        return [
            todo
            for todo in self.all()
            if todo.display(today) and todo.category == category
        ]

    def get_todos_completed_today(
        self, /, today: datetime.date = datetime.date.today()
    ) -> typing.List[domain.Todo]:
        return [todo for todo in self.all() if todo.date_completed == today]

    def mark_complete(self, /, todo_id: int) -> None:
        with self._uow as uow:
            uow.todo_repository.mark_completed(todo_id)
            uow.save()

    def update_todo(self, /, todo: domain.Todo) -> None:
        with self._uow as uow:
            uow.todo_repository.update(todo)
            uow.save()
