import dataclasses
import datetime
import typing

import sqlalchemy as sa
from loguru import logger

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
            logger.error(f"{self.__class__.__name__}.add({todo=!r}) failed: {e!s}")

            return domain.Error.new(str(e), todo=todo)

    # def add_default_holidays_for_all_users(self) -> None | domain.Error:
    #     try:
    #         with self._engine.begin() as con:
    #             users = adapter.user_repo.where(con=con)
    #             if isinstance(users, domain.Error):
    #                 return users
    #
    #             for user in users:
    #                 for holiday in domain.HOLIDAYS:
    #                     todo = self.get_by_template_id_and_user_id(
    #                         template_id=holiday.todo_id,
    #                         user_id=user.user_id,
    #                     )
    #
    #                     if todo is None:
    #                         new_holiday = dataclasses.replace(
    #                             holiday,
    #                             todo_id=domain.create_uuid(),
    #                             template_todo_id=holiday.todo_id,
    #                             user=user,
    #                         )
    #
    #                         add_result = adapter.todo_repo.add(con=con, todo=new_holiday)
    #                         if isinstance(add_result, domain.Error):
    #                             return add_result
    #         return None
    #     except Exception as e:
    #         return domain.Error.new(str(e))

    # def cleanup(self) -> None | domain.Error:
    #     try:
    #         cutoff_date = datetime.date.today() - datetime.timedelta(days=5)
    #
    #         with self._engine.begin() as con:
    #             for todo_id, todo in copy.copy(self._todos).items():
    #                 if todo.frequency.name == domain.FrequencyType.Once:
    #                     if todo.last_completed and todo.last_completed < cutoff_date:
    #                         delete_result = adapter.todo_repo.delete(con=con, todo_id=todo_id)
    #                         if isinstance(delete_result, domain.Error):
    #                             return delete_result
    #
    #         return None
    #     except Exception as e:
    #         return domain.Error.new(str(e))

    def delete(self, *, todo_id: str) -> None | domain.Error:
        try:
            with self._engine.begin() as con:
                return adapter.todo_repo.delete(con=con, todo_id=todo_id)
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.delete({todo_id=!r}) failed: {e!s}")

            return domain.Error.new(str(e), todo_id=todo_id)

    def get(self, *, todo_id: str) -> domain.Todo | None | domain.Error:
        try:
            with self._engine.begin() as con:
                return adapter.todo_repo.get(con=con, todo_id=todo_id)
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.get({todo_id=!r}) failed: {e!s}")

            return domain.Error.new(str(e), todo_id=todo_id)

    def get_by_template_id_and_user_id(
        self,
        *,
        template_todo_id: str,
        user_id: str,
    ) -> domain.Todo | None | domain.Error:
        try:
            with self._engine.begin() as con:
                todos = adapter.todo_repo.where(
                    con=con,
                    category_id=domain.Unspecified(),
                    user_id=user_id,
                    description_starts_with=domain.Unspecified(),
                    template_todo_id=template_todo_id,
                )
                if isinstance(todos, domain.Error):
                    return todos

                return next(
                    (
                        todo
                        for todo in todos
                        if todo.template_todo_id == template_todo_id and todo.user.user_id == user_id
                    ),
                    None,
                )
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.get({template_todo_id=!r}, {user_id=!r}) failed: {e!s}")

            return domain.Error.new(
                str(e),
                template_todo_id=template_todo_id,
                user_id=user_id,
            )

    def mark_complete(
        self,
        *,
        todo_id: str,
        user: domain.User | None,
    ) -> None | domain.Error:
        try:
            with self._engine.begin() as con:
                todo = adapter.todo_repo.get(con=con, todo_id=todo_id)
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
            logger.error(f"{self.__class__.__name__}.mark_complete({todo_id=!r}, {user=!r}) failed: {e!s}")

            return domain.Error.new(str(e), todo_id=todo_id, user=user)

    def where(
        self,
        *,
        due_filter: bool | domain.Unspecified,
        description_like: str | domain.Unspecified,
        category_id_filter: str | domain.Unspecified,
        user_id_filter: str | domain.Unspecified,
    ) -> list[domain.Todo] | domain.Error:
        try:
            with self._engine.begin() as con:
                todos: typing.Iterable[domain.Todo] | domain.Error = adapter.todo_repo.where(
                    con=con,
                    category_id=category_id_filter,
                    user_id=user_id_filter,
                    description_starts_with=description_like,
                    template_todo_id=domain.Unspecified(),
                )
                if isinstance(todos, domain.Error):
                    return todos

            if due_filter:
                todos = (todo for todo in todos if todo.should_display())

            today = datetime.date.today()
            return sorted(
                todos,
                key=(
                    lambda todo: domain.date_calc.due_date(
                        frequency=todo.frequency,
                        ref_date=today,
                    )
                    or datetime.date(1900, 1, 1)
                ),
            )
        except Exception as e:
            logger.error(
                f"{self.__class__.__name__}.where({due_filter=!r}, {description_like=!r}, {category_id_filter=!r}, "
                f"{user_id_filter=!r}) failed: {e!s}"
            )

            return domain.Error.new(
                str(e),
                due_filter=due_filter,
                description_like=description_like,
                category_id_filter=category_id_filter,
                user_id_filter=user_id_filter,
            )

    def mark_incomplete(self, *, todo_id: str) -> None | domain.Error:
        try:
            with self._engine.begin() as con:
                todo = adapter.todo_repo.get(con=con, todo_id=todo_id)
                if isinstance(todo, domain.Error):
                    return todo

                if todo is None:
                    return None

                if todo.last_completed is not None:
                    if todo.prior_completed:
                        last_completed: datetime.date | None = todo.prior_completed
                    else:
                        last_completed = None

                    updated_todo = dataclasses.replace(
                        todo,
                        last_completed=last_completed,
                        prior_completed=None,
                    )

                    return adapter.todo_repo.update(con=con, todo=updated_todo)

            return None
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.mark_incomplete({todo_id=!r}) failed: {e!s}")

            return domain.Error.new(str(e), todo_id=todo_id)

    def update(self, *, todo: domain.Todo) -> None | domain.Error:
        try:
            with self._engine.begin() as con:
                updated_todo = dataclasses.replace(
                    todo,
                    date_updated=datetime.datetime.now(),
                )
                return adapter.todo_repo.update(
                    con=con,
                    todo=updated_todo,
                )
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.update({todo=!r}) failed: {e!s}")

            return domain.Error.new(str(e), todo=todo)
