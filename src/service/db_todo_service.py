import dataclasses
import datetime

from src import adapter, domain
from src.domain import Todo

import sqlmodel as sm

__all__ = ("DbTodoService",)


class DbTodoService(domain.TodoService):
    def __init__(self, *, session: sm.Session, min_seconds_between_refreshes: int = 300):
        self._session = session
        self._min_seconds_between_refreshes = min_seconds_between_refreshes

        self._todos: dict[str, domain.Todo] | None = None
        self._last_refresh: datetime.datetime | None = None

    def delete(self, *, todo_id: str) -> None:
        repo = adapter.DbTodoRepository(session=self._session)
        repo.delete(todo_id=todo_id)
        self._session.commit()

        if self._todos is not None:
            del self._todos[todo_id]

    def get(self, *, todo_id: str) -> domain.Todo | None:
        if self._todos is None:
            self.refresh()

        return self._todos.get(todo_id)  # type: ignore

    def get_all(self) -> list[Todo]:
        if self._last_refresh is None or self._todos is None:
            self.refresh()
        else:
            seconds_since_last_refresh = (datetime.datetime.now() - self._last_refresh).total_seconds()
            if seconds_since_last_refresh >= self._min_seconds_between_refreshes:
                self.refresh()

        return list(self._todos.values())  # type: ignore

    def get_where(
        self,
        *,
        date_filter: datetime.date,
        due_filter: bool,
        description_like: str,
    ) -> list[Todo]:
        if due_filter:
            return [
                todo for todo in self.get_all()
                if description_like.strip().lower() in todo.description.lower()
                and todo.should_display(today=date_filter)
            ]

        return [
            todo for todo in self.get_all()
            if description_like.strip().lower() in todo.description.lower()
        ]

    def mark_complete(self, *, todo_id: str) -> None:
        repo = adapter.DbTodoRepository(session=self._session)

        if todo := repo.get(todo_id=todo_id):
            if todo.last_completed:
                prior_completed = todo.last_completed
            else:
                prior_completed = None

            updated_todo = dataclasses.replace(
                todo,
                last_completed=datetime.date.today(),
                prior_completed=prior_completed,
            )

            repo.update(todo=updated_todo)

            self._session.commit()

            if self._todos is not None:
                self._todos[todo_id] = updated_todo

    def mark_incomplete(self, *, todo_id: str) -> None:
        repo = adapter.DbTodoRepository(session=self._session)

        if todo := repo.get(todo_id=todo_id):
            if todo.last_completed is not None:
                if todo.prior_completed:
                    last_completed = todo.prior_completed
                else:
                    last_completed = None

                updated_todo = dataclasses.replace(
                    todo,
                    last_completed=last_completed,
                    prior_completed=None,
                )

                repo.update(todo=updated_todo)

                self._session.commit()

                if self._todos is not None:
                    self._todos[todo_id] = updated_todo

    def refresh(self) -> None:
        repo = adapter.DbTodoRepository(session=self._session)
        self._todos = {
            todo.todo_id: todo
            for todo in repo.all()
        }
        self._last_refresh = datetime.datetime.now()

    def upsert(self, *, todo: Todo) -> None:
        repo = adapter.DbTodoRepository(session=self._session)

        if repo.get(todo_id=todo.todo_id) is not None:
            updated_todo = dataclasses.replace(todo, date_updated=datetime.datetime.now())
            repo.update(todo=updated_todo)
            if self._todos is not None:
                self._todos[todo.todo_id] = updated_todo
        else:
            repo.add(todo=todo)
            if self._todos is not None:
                self._todos[todo.todo_id] = todo

        self._session.commit()
