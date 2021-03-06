from __future__ import annotations

import copy
import dataclasses
import datetime

import sqlalchemy as sa
import sqlmodel as sm

from src import adapter, domain
from src.domain import Todo

__all__ = ("DbTodoService",)


class DbTodoService(domain.TodoService):
    def __init__(
        self,
        *,
        engine: sa.engine.Engine,
        username: str,
        min_seconds_between_refreshes: int = 300,
    ):
        self._engine = engine
        self._username = username
        self._min_seconds_between_refreshes = min_seconds_between_refreshes

        self._todos: dict[str, domain.Todo] = {}
        self._last_refresh: datetime.datetime | None = None

    def add(self, *, todo: Todo) -> None:
        with sm.Session(self._engine) as session:
            repo = adapter.DbTodoRepository(session=session)
            repo.add(todo=todo)
            if self._todos is not None:
                self._todos[todo.todo_id] = todo
            session.commit()

    def cleanup(self) -> None:
        self._refresh()

        cutoff_date = datetime.date.today() - datetime.timedelta(days=7)

        for todo_id, todo in copy.copy(self._todos).items():
            if todo.frequency.name == domain.FrequencyType.Once:
                if todo.last_completed and todo.last_completed < cutoff_date:
                    self.delete(todo_id=todo_id)

    def delete(self, *, todo_id: str) -> None:
        self._refresh()

        with sm.Session(self._engine) as session:
            repo = adapter.DbTodoRepository(session=session)
            repo.delete(todo_id=todo_id)
            session.commit()

        if self._todos is not None:
            del self._todos[todo_id]

    def get(self, *, todo_id: str) -> domain.Todo | None:
        self._refresh()

        return self._todos.get(todo_id)

    def get_by_template_id_and_user_id(self, *, template_id: str, user_id: str) -> domain.Todo | None:
        self._refresh()

        return next(
            (
                todo for todo in self._todos.values()
                if todo.template_todo_id == template_id
                and todo.user.user_id == user_id
            ),
            None
        )

    def mark_complete(self, *, todo_id: str, user: domain.User | None) -> None:
        with sm.Session(self._engine) as session:
            repo = adapter.DbTodoRepository(session=session)

            if todo := repo.get(todo_id=todo_id):
                if todo.last_completed:
                    prior_completed = todo.last_completed
                    prior_completed_by = todo.last_completed_by
                else:
                    prior_completed = None
                    prior_completed_by = None

                updated_todo = dataclasses.replace(
                    todo,
                    last_completed=datetime.date.today(),
                    prior_completed=prior_completed,
                    last_completed_by=user,
                    prior_completed_by=prior_completed_by,
                )

                repo.update(todo=updated_todo)

                session.commit()

                if self._todos is not None:
                    self._todos[todo_id] = updated_todo

    def where(
        self,
        *,
        date_filter: datetime.date,
        due_filter: bool,
        description_like: str,
        category_id_filter: str | None,
        user_id_filter: str | None,
    ) -> list[Todo]:
        self._refresh()

        todos = (todo for todo in self._todos.values())

        if description := description_like.strip().lower():
            todos = (
                todo for todo in self._todos.values() if
                description in todo.description.lower()
            )

        if due_filter:
            todos = (
                todo for todo in todos
                if todo.should_display(today=date_filter)
            )

        if user_id_filter:
            assert not isinstance(user_id_filter, domain.User)
            todos = (todo for todo in todos if todo.user.user_id == user_id_filter)

        if category_id_filter:
            todos = (todo for todo in todos if todo.category.category_id == category_id_filter)

        return sorted(todos, key=lambda todo: todo.due_date(today=date_filter))

    def mark_incomplete(self, *, todo_id: str) -> None:
        with sm.Session(self._engine) as session:
            repo = adapter.DbTodoRepository(session=session)

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

                    session.commit()

                    if self._todos is not None:
                        self._todos[todo_id] = updated_todo

    def refresh(self) -> None:
        with sm.Session(self._engine) as session:
            repo = adapter.DbTodoRepository(session=session)
            self._todos = {
                todo.todo_id: todo
                for todo in repo.all()
            }
            self._last_refresh = datetime.datetime.now()

    def update(self, *, todo: Todo) -> None:
        with sm.Session(self._engine) as session:
            repo = adapter.DbTodoRepository(session=session)
            updated_todo = dataclasses.replace(todo, date_updated=datetime.datetime.now())
            repo.update(todo=updated_todo)
            if self._todos is not None:
                self._todos[todo.todo_id] = updated_todo
            session.commit()

    def _refresh(self) -> None:
        if self._last_refresh is None or self._todos is None:
            time_to_refresh = True
        else:
            seconds_since_last_refresh = (datetime.datetime.now() - self._last_refresh).total_seconds()
            if seconds_since_last_refresh >= self._min_seconds_between_refreshes:
                time_to_refresh = True
            else:
                time_to_refresh = False

        if time_to_refresh:
            self.refresh()
