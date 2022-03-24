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

        if self._todos is not None:
            del self._todos[todo_id]

    def get(self, *, todo_id: str) -> domain.Todo | None:
        if self._todos is None:
            self.refresh()

        return self._todos.get(todo_id)

    def get_all(self) -> list[Todo]:
        if self._last_refresh is None or self._todos is None:
            self.refresh()
        else:
            seconds_since_last_refresh = (datetime.datetime.now() - self._last_refresh).total_seconds()
            if seconds_since_last_refresh >= self._min_seconds_between_refreshes:
                self.refresh()
        return list(self._todos.values())

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
            repo.update(todo=todo)
        else:
            repo.add(todo=todo)

        if self._todos is not None:
            self._todos[todo.todo_id] = todo
