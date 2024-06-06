import dataclasses
import datetime

import sqlalchemy as sa

from src import adapter, domain

TODO_1 = domain.Todo.daily(
    todo_id="1" * 32,
    category=domain.TODO_CATEGORY,
    description="Wash dishes",
    note="todo_1 note",
    start_date=datetime.date(2010, 1, 1),
    date_added=datetime.datetime(2011, 1, 2, 3, 4, 5, 6),
    date_updated=datetime.datetime(2011, 2, 3, 4, 5, 6, 7),
    last_completed=None,
    prior_completed=None,
    last_completed_by=None,
    prior_completed_by=None,
    template_todo_id=None,
    user=domain.DEFAULT_USER,
)

TODO_2 = domain.Todo.monthly(
    todo_id="2" * 32,
    advance_display_days=7,
    expire_display_days=30,
    category=domain.TODO_CATEGORY,
    description="Clean garage",
    month_day=10,
    note="todo_2 note",
    start_date=datetime.date(2010, 1, 1),
    date_added=datetime.datetime(2011, 1, 2, 3, 4, 5, 6),
    date_updated=datetime.datetime(2011, 2, 3, 4, 5, 6, 7),
    last_completed=datetime.date(2010, 1, 2),
    prior_completed=None,
    last_completed_by=None,
    prior_completed_by=None,
    template_todo_id=None,
    user=domain.DEFAULT_USER,
)

TODO_3 = domain.Todo.yearly(
    todo_id="3" * 32,
    advance_display_days=30,
    expire_display_days=90,
    category=domain.TODO_CATEGORY,
    description="Pay taxes",
    month=domain.Month.February,
    month_day=10,
    note="todo_3 note",
    start_date=datetime.date(2010, 1, 1),
    date_added=datetime.datetime(2011, 1, 2, 3, 4, 5, 6),
    date_updated=datetime.datetime(2011, 2, 3, 4, 5, 6, 7),
    last_completed=datetime.date(2012, 3, 4),
    prior_completed=datetime.date(2011, 2, 3),
    last_completed_by=None,
    prior_completed_by=None,
    template_todo_id=None,
    user=domain.DEFAULT_USER,
)


def test_round_trip(engine: sa.Engine) -> None:
    with engine.begin() as con:
        adapter.category_repo.add(schema=None, con=con, category=domain.TODO_CATEGORY)

        assert adapter.todo_repo.add(schema=None, con=con, todo=TODO_1) is None
        assert adapter.todo_repo.add(schema=None, con=con, todo=TODO_2) is None
        assert adapter.todo_repo.add(schema=None, con=con, todo=TODO_3) is None

        todos = adapter.todo_repo.where(
            schema=None,
            con=con,
            category_id=domain.Unspecified(),
            user_id=domain.Unspecified(),
            description_like=domain.Unspecified(),
            template_todo_id=domain.Unspecified(),
        )
        assert isinstance(todos, list)
        assert len(todos) == 3

        updated_todo_1 = dataclasses.replace(TODO_1, note="Updated note 1.")

        assert adapter.todo_repo.update(schema=None, con=con, todo=updated_todo_1) is None

        todo = adapter.todo_repo.get(schema=None, con=con, todo_id=TODO_1.todo_id)
        assert isinstance(todo, domain.Todo)
        assert todo.note == "Updated note 1."

        todos = adapter.todo_repo.where(
            schema=None,
            con=con,
            category_id=domain.Unspecified(),
            user_id=domain.Unspecified(),
            description_like=domain.Unspecified(),
            template_todo_id=domain.Unspecified(),
        )
        assert isinstance(todos, list)
        assert len(todos) == 3

        assert adapter.todo_repo.delete(schema=None, con=con, todo_id=TODO_2.todo_id) is None

        todos = adapter.todo_repo.where(
            schema=None,
            con=con,
            category_id=domain.Unspecified(),
            user_id=domain.Unspecified(),
            description_like=domain.Unspecified(),
            template_todo_id=domain.Unspecified(),
        )
        assert isinstance(todos, list)
        assert len(todos) == 2

    return None
