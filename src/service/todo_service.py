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
    ):
        self._engine: typing.Final[sa.engine.Engine] = engine
        self._username: typing.Final[str] = username

    def add(self, *, todo: domain.Todo) -> None | domain.Error:
        try:
            with self._engine.begin() as con:
                return adapter.todo_repo.add(con=con, todo=todo)
        except Exception as e:
            return domain.Error.new(str(e), todo=todo)

    def add_default_holidays_for_all_users(self) -> None | domain.Error:
        try:
            with self._engine.begin() as con:
                users = adapter.user_repo.where(con=con)
                if isinstance(users, domain.Error):
                    return users

                for user in users:
                    for holiday in domain.HOLIDAYS:
                        todo = self.get_by_template_id_and_user_id(
                            template_id=holiday.todo_id,
                            user_id=user.user_id,
                        )

                        if todo is None:
                            new_holiday = dataclasses.replace(
                                holiday,
                                todo_id=domain.create_uuid(),
                                template_todo_id=holiday.todo_id,
                                user=user,
                            )

                            add_result = adapter.todo_repo.add(con=con, todo=new_holiday)
                            if isinstance(add_result, domain.Error):
                                return add_result
            return None
        except Exception as e:
            return domain.Error.new(str(e))

    def cleanup(self) -> None | domain.Error:
        try:
            cutoff_date = datetime.date.today() - datetime.timedelta(days=5)

            with self._engine.begin() as con:
                for todo_id, todo in copy.copy(self._todos).items():
                    if todo.frequency.name == domain.FrequencyType.Once:
                        if todo.last_completed and todo.last_completed < cutoff_date:
                            delete_result = adapter.todo_repo.delete(con=con, todo_id=todo_id)
                            if isinstance(delete_result, domain.Error):
                                return delete_result

            return None
        except Exception as e:
            return domain.Error.new(str(e))

    def delete(self, *, todo_id: str) -> None | domain.Error:
        try:
            with self._engine.begin() as con:
                return adapter.todo_repo.delete(con=con, todo_id=todo_id)
        except Exception as e:
            return domain.Error.new(str(e), todo_id=todo_id)

    def get(self, *, todo_id: str) -> domain.Todo | None | domain.Error:
        try:
            with self._engine.begin() as con:
                return adapter.todo_repo.get_by_id(con=con, todo_id=todo_id)
        except Exception as e:
            return domain.Error.new(str(e), todo_id=todo_id)

    def get_by_template_id_and_user_id(
        self,
        *,
        template_id: str,
        user_id: str,
    ) -> domain.Todo | None | domain.Error:
        try:
            with self._engine.begin() as con:
                todos = adapter.todo_repo.all_todos(con=con)
                if isinstance(todos, domain.Error):
                    return todos

                return next(
                    (todo for todo in todos if todo.template_todo_id == template_id and todo.user.user_id == user_id),
                    None,
                )
        except Exception as e:
            return domain.Error.new(str(e), template_id=template_id, user_id=user_id)

    def mark_complete(
        self,
        *,
        todo_id: str,
        user: domain.User | None,
    ) -> None | domain.Error:
        try:
            with self._engine.begin() as con:
                todo = adapter.todo_repo.get_by_id(con=con, todo_id=todo_id)
                if isinstance(todo, domain.Error):
                    return todo

                if todo is None:
                    return None

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

                adapter.todo_repo.update(con=con, todo=updated_todo)

            return None
        except Exception as e:
            return domain.Error.new(str(e), todo_id=todo_id, user=user)

    def where(
        self,
        *,
        due_filter: bool,
        description_like: str,
        category_id_filter: str | None,
        user_id_filter: str | None,
    ) -> list[domain.Todo] | domain.Error:
        try:
            with self._engine.begin() as con:
                todos = adapter.todo_repo.all_todos(con=con)
                if isinstance(todos, domain.Error):
                    return todos

            if description := description_like.strip().lower():
                todos = (todo for todo in todos if description in todo.description.lower())

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
        except Exception as e:
            return domain.Error.new(
                str(e),
                due_filter=due_filter,
                description_like=description_like,
                category_id_filter=category_id_filter,
                user_id_filter=user_id_filter,
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
