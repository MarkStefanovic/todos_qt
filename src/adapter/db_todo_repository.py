import sqlmodel as sm

from src import domain
from src.adapter import db
from src.domain import Todo

__all__ = ("DbTodoRepository",)


class DbTodoRepository(domain.TodoRepository):
    def __init__(self, *, session: sm.Session):
        self._session = session

    def add(self, *, todo: domain.Todo) -> None:
        if todo.todo_id == "":
            raise ValueError(f"Not a valid uuid: {todo.todo_id}")

        if todo.frequency.week_day is None:
            week_day = None
        else:
            week_day = todo.frequency.week_day.to_int()

        if todo.frequency.month is None:
            month = None
        else:
            month = todo.frequency.month.to_int()

        todo_orm = db.Todo(
            todo_id=todo.todo_id,
            expire_days=todo.expire_days,
            advance_days=todo.advance_days,
            category=todo.category.to_str(),
            description=todo.description,
            note=todo.note,
            start_date=todo.start_date,
            date_added=todo.date_added,
            date_updated=todo.date_updated,
            date_deleted=todo.date_deleted,
            frequency=todo.frequency.name,
            week_day=week_day,
            week_number=todo.frequency.week_number,
            month=month,
            month_day=todo.frequency.month_day,
            days=todo.frequency.days,
            due_date=todo.frequency.due_date,
        )

        self._session.add(todo_orm)

    def all(self) -> list[domain.Todo]:
        return [
            domain.Todo(
                todo_id=todo_orm.todo_id,
                expire_days=todo_orm.expire_days,
                advance_days=todo_orm.advance_days,
                category=domain.TodoCategory.from_str(todo_orm.category),
                description=todo_orm.description,
                frequency=_parse_frequency(row=todo_orm),
                note=todo_orm.note,
                start_date=todo_orm.start_date,
                date_added=todo_orm.date_added,
                date_updated=todo_orm.date_updated,
                date_deleted=todo_orm.date_deleted,
            )
            for todo_orm in self._session.exec(sm.select(db.Todo))
        ]

    def delete(self, *, todo_id: str) -> None:
        todo = self._get_orm(todo_id=todo_id)
        self._session.delete(todo)

    def get(self, *, todo_id: str) -> domain.Todo:
        todo_orm = self._get_orm(todo_id=todo_id)

        return domain.Todo(
            todo_id=todo_orm.todo_id,
            expire_days=todo_orm.expire_days,
            advance_days=todo_orm.advance_days,
            category=domain.TodoCategory.from_str(todo_orm.category),
            description=todo_orm.description,
            frequency=_parse_frequency(row=todo_orm),
            note=todo_orm.note,
            start_date=todo_orm.start_date,
            date_added=todo_orm.date_added,
            date_updated=todo_orm.date_updated,
            date_deleted=todo_orm.date_deleted,
        )

    def update(self, *, todo: Todo) -> None:
        todo_orm = self._get_orm(todo_id=todo.todo_id)

        if todo.frequency.week_day is None:
            week_day = None
        else:
            week_day = todo.frequency.week_day.to_int()

        if todo.frequency.month is None:
            month = None
        else:
            month = todo.frequency.month.to_int()

        todo_orm.expire_days = todo.expire_days
        todo_orm.advance_days = todo.advance_days
        todo_orm.category = todo.category.to_str()
        todo_orm.description = todo.description
        todo_orm.note = todo.note
        todo_orm.start_date = todo.start_date
        todo_orm.date_added = todo.date_added
        todo_orm.date_updated = todo.date_updated
        todo_orm.date_deleted = todo.date_deleted
        todo_orm.frequency = todo.frequency.name
        todo_orm.week_day = week_day
        todo_orm.week_number = todo.frequency.week_number
        todo_orm.month = month
        todo_orm.month_day = todo.frequency.month_day
        todo_orm.days = todo.frequency.days
        todo_orm.due_date = todo.frequency.due_date

        self._session.add(todo_orm)

    def _get_orm(self, *, todo_id: str) -> db.Todo:
        return self._session.exec(
            sm.select(db.Todo).where(db.Todo.todo_id == todo_id)
        ).one()


def _parse_frequency(*, row: db.Todo) -> domain.Frequency:
    if row.frequency == "daily":
        return domain.Frequency.daily()
    elif row.frequency == "easter":
        return domain.Frequency.easter()
    elif row.frequency == "irregular":
        assert row.month is not None, "[month] is required for an irregular todo."
        assert row.week_day is not None, "[week_day] is required for an irregular todo."
        assert row.week_number is not None, "[week_number] is required for an irregular todo."

        return domain.Frequency.irregular(
            month=domain.Month.from_int(row.month),
            week_day=domain.Weekday.from_int(row.week_day),
            week_number=row.week_number,
        )
    elif row.frequency == "monthly":
        assert row.month_day is not None, "[month_day] is required if the frequency is 'monthly'."

        return domain.Frequency.monthly(month_day=row.month_day)
    elif row.frequency == "once":
        assert row.due_date is not None, "[due_date] is required if the frequency is 'once'."

        return domain.Frequency.once(due_date=row.due_date)
    elif row.frequency == "weekly":
        assert row.week_day is not None, "[week_day] is required if the frequency is 'weekly'."

        return domain.Frequency.weekly(week_day=domain.Weekday.from_int(row.week_day))
    elif row.frequency == "xdays":
        assert row.days is not None, "[days] is required if the frequency is 'xdays'."

        return domain.Frequency.xdays(days=row.days)
    elif row.frequency == "yearly":
        assert row.month is not None, "[month] is required if the frequency is 'yearly'."
        assert row.month_day is not None, "[month_day] is required if the frequency is 'yearly'."

        return domain.Frequency.yearly(
            month=domain.Month.from_int(row.month),
            month_day=row.month_day,
        )
    else:
        raise ValueError(f"Unrecognized frequency, {row.frequency!r}.")
