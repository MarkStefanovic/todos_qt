import dataclasses
import datetime

from src import adapter, domain

import sqlmodel as sm

TODO_1 = domain.Todo.daily(
    todo_id="1" * 32,
    category=domain.TodoCategory.Todo,
    description="Wash dishes",
    note="todo_1 note",
    start_date=datetime.date(2010, 1, 1),
    date_added=datetime.datetime(2011, 1, 2, 3, 4, 5, 6),
    date_updated=datetime.datetime(2011, 2, 3, 4, 5, 6, 7),
    date_deleted=None,
)

TODO_2 = domain.Todo.monthly(
    todo_id="2" * 32,
    advance_days=7,
    expire_days=30,
    category=domain.TodoCategory.Todo,
    description="Clean garage",
    month_day=10,
    note="todo_2 note",
    start_date=datetime.date(2010, 1, 1),
    date_added=datetime.datetime(2011, 1, 2, 3, 4, 5, 6),
    date_updated=datetime.datetime(2011, 2, 3, 4, 5, 6, 7),
    date_deleted=None,
)

TODO_3 = domain.Todo.yearly(
    todo_id="3" * 32,
    advance_days=30,
    expire_days=90,
    category=domain.TodoCategory.Todo,
    description="Pay taxes",
    month=domain.Month.February,
    month_day=10,
    note="todo_3 note",
    start_date=datetime.date(2010, 1, 1),
    date_added=datetime.datetime(2011, 1, 2, 3, 4, 5, 6),
    date_updated=datetime.datetime(2011, 2, 3, 4, 5, 6, 7),
    date_deleted=None,
)


def test_round_trip(session: sm.Session):
    repo = adapter.DbTodoRepository(session=session)

    repo.add(todo=TODO_1)
    repo.add(todo=TODO_2)
    repo.add(todo=TODO_3)

    session.commit()

    assert len(repo.all()) == 3

    updated_todo_1 = dataclasses.replace(
        TODO_1,
        note="Updated note 1."
    )

    repo.update(todo=updated_todo_1)

    session.commit()

    assert repo.get(todo_id=TODO_1.todo_id).note == "Updated note 1."

    assert len(repo.all()) == 3

    repo.delete(todo_id=TODO_2.todo_id)

    session.commit()

    assert len(repo.all()) == 2

