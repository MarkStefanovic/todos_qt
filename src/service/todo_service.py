import copy
import dataclasses
import datetime
import typing

import sqlalchemy as sa

from src import adapter, domain

__all__ = ("TodoService",)


class TodoService(domain.TodoService):
    def __init__(
        self,
        *,
        engine: sa.engine.Engine,
        username: str,
        min_seconds_between_refreshes: int = 300,
    ):
        self._engine: typing.Final[sa.engine.Engine] = engine
        self._username: typing.Final[str] = username
        self._min_seconds_between_refreshes: typing.Final[int] = min_seconds_between_refreshes

        self._todos: dict[str, domain.Todo] = {}
        self._last_refresh: datetime.datetime | None = None

    def add(self, *, todo: domain.Todo) -> None:
        repo = adapter.DbTodoRepository(engine=self._engine)
        repo.add(todo=todo)
        if self._todos is not None:
            self._todos[todo.todo_id] = todo

    def add_default_holidays_for_all_users(self) -> None:
        user_repo = adapter.DbUserRepository(engine=self._engine)
        users = user_repo.all_todos()

        for user in users:
            for holiday in domain.HOLIDAYS:
                if (
                    self.get_by_template_id_and_user_id(
                        template_id=holiday.todo_id,
                        user_id=user.user_id,
                    )
                    is None
                ):
                    new_holiday = dataclasses.replace(
                        holiday,
                        todo_id=domain.create_uuid(),
                        template_todo_id=holiday.todo_id,
                        user=user,
                    )
                    self.add(todo=new_holiday)

    def cleanup(self) -> None:
        self._refresh()

        cutoff_date = datetime.date.today() - datetime.timedelta(days=5)

        for todo_id, todo in copy.copy(self._todos).items():
            if todo.frequency.name == domain.FrequencyType.Once:
                if todo.last_completed and todo.last_completed < cutoff_date:
                    self.delete(todo_id=todo_id)

    def delete(self, *, todo_id: str) -> None:
        self._refresh()

        repo = adapter.DbTodoRepository(engine=self._engine)
        repo.delete(todo_id=todo_id)

        if self._todos is not None:
            del self._todos[todo_id]

    def get(self, *, todo_id: str) -> domain.Todo | None:
        self._refresh()

        return self._todos.get(todo_id)

    def get_by_template_id_and_user_id(self, *, template_id: str, user_id: str) -> domain.Todo | None:
        self._refresh()

        return next(
            (
                todo
                for todo in self._todos.values()
                if todo.template_todo_id == template_id and todo.user.user_id == user_id
            ),
            None,
        )

    def mark_complete(self, *, todo_id: str, user: domain.User | None) -> None:
        repo = adapter.DbTodoRepository(engine=self._engine)

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

            if self._todos is not None:
                self._todos[todo_id] = updated_todo

    def where(
        self,
        *,
        due_filter: bool,
        description_like: str,
        category_id_filter: str | None,
        user_id_filter: str | None,
    ) -> list[domain.Todo]:
        self._refresh()

        todos = (todo for todo in self._todos.values())

        if description := description_like.strip().lower():
            todos = (todo for todo in self._todos.values() if description in todo.description.lower())

        if due_filter:
            todos = (todo for todo in todos if todo.should_display())

        if user_id_filter:
            assert not isinstance(user_id_filter, domain.User)
            todos = (todo for todo in todos if todo.user.user_id == user_id_filter)

        if category_id_filter:
            todos = (todo for todo in todos if todo.category.category_id == category_id_filter)

        today = datetime.date.today()
        return sorted(
            todos,
            key=(
                lambda todo: domain.date_calc.due_date(frequency=todo.frequency, ref_date=today)
                or datetime.date(1900, 1, 1)
            ),
        )

    def mark_incomplete(self, *, todo_id: str) -> None:
        repo = adapter.DbTodoRepository(engine=self._engine)

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

                if self._todos is not None:
                    self._todos[todo_id] = updated_todo

    def refresh(self) -> None:
        repo = adapter.DbTodoRepository(engine=self._engine)
        self._todos = {todo.todo_id: todo for todo in repo.all_todos()}
        self._last_refresh = datetime.datetime.now()

    def update(self, *, todo: domain.Todo) -> None:
        repo = adapter.DbTodoRepository(engine=self._engine)
        updated_todo = dataclasses.replace(todo, date_updated=datetime.datetime.now())
        repo.update(todo=updated_todo)
        if self._todos is not None:
            self._todos[todo.todo_id] = updated_todo

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


if __name__ == "__main__":
    eng = adapter.db.create_engine()
    svc = TodoService(engine=eng, username="test")
    for r in svc.where(
        due_filter=True,
        description_like="",
        category_id_filter=None,
        user_id_filter=None,
    ):
        print(r)
