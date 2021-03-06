import dataclasses
import datetime

from src import adapter, domain

import sqlmodel as sm

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


def test_round_trip(session: sm.Session):
    category_repo = adapter.DbCategoryRepository(session=session)

    category_repo.add(category=domain.TODO_CATEGORY)

    session.commit()

    todo_repo = adapter.DbTodoRepository(session=session)

    todo_repo.add(todo=TODO_1)
    todo_repo.add(todo=TODO_2)
    todo_repo.add(todo=TODO_3)

    session.commit()

    assert len(todo_repo.all()) == 3

    updated_todo_1 = dataclasses.replace(
        TODO_1,
        note="Updated note 1."
    )

    todo_repo.update(todo=updated_todo_1)

    session.commit()

    assert todo_repo.get(todo_id=TODO_1.todo_id).note == "Updated note 1."

    assert len(todo_repo.all()) == 3

    todo_repo.delete(todo_id=TODO_2.todo_id)

    session.commit()

    assert len(todo_repo.all()) == 2
