import datetime
import typing

from src import domain
from src.adapter import db
from src.adapter.db_category_repository import DbCategoryRepository
from src.adapter.db_user_repository import DbUserRepository

import sqlalchemy as sa

__all__ = ("DbTodoRepository",)


FREQUENCY_LKP = {
    "daily": domain.FrequencyType.Daily,
    "easter": domain.FrequencyType.Easter,
    "irregular": domain.FrequencyType.Irregular,
    "memorial_day": domain.FrequencyType.MemorialDay,
    "monthly": domain.FrequencyType.Monthly,
    "once": domain.FrequencyType.Once,
    "weekly": domain.FrequencyType.Weekly,
    "xdays": domain.FrequencyType.XDays,
    "yearly": domain.FrequencyType.Yearly,
}

FREQUENCY_NAME_LKP = {
    domain.FrequencyType.Daily: "daily",
    domain.FrequencyType.Easter: "easter",
    domain.FrequencyType.Irregular: "irregular",
    domain.FrequencyType.MemorialDay: "memorial_day",
    domain.FrequencyType.Monthly: "monthly",
    domain.FrequencyType.Once: "once",
    domain.FrequencyType.Weekly: "weekly",
    domain.FrequencyType.XDays: "xdays",
    domain.FrequencyType.Yearly: "yearly",
}


# noinspection PyComparisonWithNone
class DbTodoRepository(domain.TodoRepository):
    def __init__(self, *, engine: sa.engine.Engine):
        self._engine = engine

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

        if todo.last_completed_by:
            last_completed_by_user_id = todo.last_completed_by.user_id
        else:
            last_completed_by_user_id = None

        if todo.prior_completed_by:
            prior_completed_by_user_id = todo.prior_completed_by.user_id
        else:
            prior_completed_by_user_id = None

        with self._engine.begin() as con:
            con.execute(
                sa.insert(db.todo)
                .values(
                    todo_id=todo.todo_id,
                    template_todo_id=todo.template_todo_id,
                    expire_days=todo.frequency.expire_display_days,
                    advance_days=todo.frequency.advance_display_days,
                    user_id=todo.user.user_id,
                    category_id=todo.category.category_id,
                    description=todo.description,
                    note=todo.note,
                    start_date=todo.frequency.start_date,
                    date_added=todo.date_added,
                    date_updated=todo.date_updated,
                    date_deleted=None,
                    frequency=FREQUENCY_NAME_LKP[todo.frequency.name],
                    week_day=week_day,
                    week_number=todo.frequency.week_number,
                    month=month,
                    month_day=todo.frequency.month_day,
                    days=todo.frequency.days,
                    due_date=todo.frequency.due_date,
                    last_completed=todo.last_completed,
                    prior_completed=todo.prior_completed,
                    last_completed_by=last_completed_by_user_id,
                    prior_completed_by=prior_completed_by_user_id,
                )
            )

    def all(self) -> list[domain.Todo]:
        category_repo = DbCategoryRepository(engine=self._engine)

        category_lkp = {
            category.category_id: category
            for category in category_repo.get_active()
        }

        user_repo = DbUserRepository(engine=self._engine)

        user_lkp = {
            user.user_id: user
            for user in user_repo.all()
        }

        with self._engine.begin() as con:
            result = con.execute(
                sa.select(db.todo)
                .where(db.todo.c.date_deleted == None)
            )

        return [
            domain.Todo(
                todo_id=row.todo_id,
                template_todo_id=row.template_todo_id,
                category=category_lkp[row.category_id],
                user=user_lkp.get(row.user_id, domain.DEFAULT_USER),
                description=row.description,
                frequency=_parse_frequency(
                    advance_display_days=row.advance_days,
                    days=row.days,
                    due_date=row.due_date,
                    expire_display_days=row.expire_days,
                    frequency=row.frequency,
                    month=row.month,
                    month_day=row.month_day,
                    start_date=row.start_date,
                    week_day=row.week_day,
                    week_number=row.week_number,
                ),
                note=row.note,
                last_completed=row.last_completed,
                last_completed_by=user_lkp.get(row.last_completed_by or ""),
                prior_completed=row.prior_completed,
                prior_completed_by=user_lkp.get(row.prior_completed_by or ""),
                date_added=row.date_added,
                date_updated=row.date_updated,
            )
            for row in result.fetchall()
        ]

    def delete(self, *, todo_id: str) -> None:
        with self._engine.begin() as con:
            con.execute(
                sa.update(db.todo)
                .where(db.todo.c.date_deleted == None)  # noqa
                .values(date_deleted=datetime.datetime.now())
            )

    def get(self, *, todo_id: str) -> domain.Todo | None:
        with self._engine.begin() as con:
            result = con.execute(
                sa.select(db.todo)
                .where(db.todo.c.todo_id == todo_id)
            )

            row = result.one_or_none()

        if row is None:
            return None

        category_repo = DbCategoryRepository(engine=self._engine)

        user_repo = DbUserRepository(engine=self._engine)

        user = user_repo.get(user_id=row.user_id) or domain.DEFAULT_USER

        if row.last_completed_by:
            last_completed_by = user_repo.get(user_id=row.last_completed_by)
        else:
            last_completed_by = None

        if row.prior_completed_by:
            prior_completed_by = user_repo.get(user_id=row.prior_completed_by)
        else:
            prior_completed_by = None

        if category := category_repo.get(category_id=row.category_id):
            return domain.Todo(
                todo_id=row.todo_id,
                template_todo_id=row.template_todo_id,
                category=category,
                user=user,
                description=row.description,
                frequency=_parse_frequency(
                    advance_display_days=row.advance_days,
                    days=row.days,
                    due_date=row.due_date,
                    expire_display_days=row.expire_days,
                    frequency=row.frequency,
                    month=row.month,
                    month_day=row.month_day,
                    start_date=row.start_date,
                    week_day=row.week_day,
                    week_number=row.week_number,
                ),
                note=row.note,
                last_completed=row.last_completed,
                last_completed_by=last_completed_by,
                prior_completed=row.prior_completed,
                prior_completed_by=prior_completed_by,
                date_added=row.date_added,
                date_updated=row.date_updated,
            )

        return None

    def update(self, *, todo: domain.Todo) -> None:
        if todo.frequency.week_day is None:
            week_day = None
        else:
            week_day = todo.frequency.week_day.to_int()

        if todo.frequency.month is None:
            month = None
        else:
            month = todo.frequency.month.to_int()

        with self._engine.begin() as con:
            con.execute(
                sa.update(db.todo)
                .where(db.todo.c.todo_id == todo.todo_id)
                .values(
                    template_todo_id=todo.template_todo_id,
                    user_id=todo.user.user_id,
                    expire_days=todo.frequency.expire_display_days,
                    advance_days=todo.frequency.advance_display_days,
                    category_id=todo.category.category_id,
                    description=todo.description,
                    note=todo.note,
                    start_date=todo.frequency.start_date,
                    date_added=todo.date_added,
                    date_updated=todo.date_updated,
                    frequency=FREQUENCY_NAME_LKP[todo.frequency.name],
                    week_day=week_day,
                    week_number=todo.frequency.week_number,
                    month=month,
                    month_day=todo.frequency.month_day,
                    days=todo.frequency.days,
                    due_date=domain.due_date(frequency=todo.frequency),
                    last_completed=todo.last_completed,
                    prior_completed=todo.prior_completed,
                    last_completed_by=None if todo.last_completed_by is None else todo.last_completed_by.user_id,
                    prior_completed_by=None if todo.prior_completed_by is None else todo.prior_completed_by.user_id,
                )
            )

    def where_category(self, *, category_id: str) -> list[domain.Todo]:
        category_repo = DbCategoryRepository(engine=self._engine)

        user_repo = DbUserRepository(engine=self._engine)

        user_lkp = {
            user.user_id: user
            for user in user_repo.all()
        }

        if category := category_repo.get(category_id=category_id):
            with self._engine.begin() as con:
                result = con.execute(
                    sa.select(db.todo)
                    .where(db.todo.c.date_deleted == None)  # noqa
                    .where(db.todo.c.category_id == category_id)
                )

                return [
                    domain.Todo(
                        todo_id=row.todo_id,
                        template_todo_id=row.template_todo_id,
                        category=category,
                        user=user_lkp[row.user_id],
                        description=row.description,
                        frequency=_parse_frequency(
                            advance_display_days=row.advance_days,
                            days=row.days,
                            due_date=row.due_date,
                            expire_display_days=row.expire_days,
                            frequency=row.frequency,
                            month=row.month,
                            month_day=row.month_day,
                            start_date=row.start_date,
                            week_day=row.week_day,
                            week_number=row.week_number,
                        ),
                        note=row.note,
                        last_completed=row.last_completed,
                        last_completed_by=user_lkp.get(row.last_completed_by or ""),
                        prior_completed=row.prior_completed,
                        prior_completed_by=user_lkp.get(row.prior_completed_by or ""),
                        date_added=row.date_added,
                        date_updated=row.date_updated,
                    )
                    for row in result.fetchall()
                ]

        return []


def _parse_frequency(
    *,
    advance_display_days: int,
    days: int | None,
    due_date: datetime.date | None,
    expire_display_days: int,
    frequency: str,
    month: int | None,
    month_day: int | None,
    start_date: datetime.date,
    week_day: int | None,
    week_number: int | None,
) -> domain.Frequency:
    if frequency == "daily":
        return domain.Frequency.daily(start_date=start_date)
    elif frequency == "easter":
        return domain.Frequency.easter(
            advance_display_days=advance_display_days,
            expire_display_days=expire_display_days,
            start_date=start_date,
        )
    elif frequency == "irregular":
        assert month is not None, "[month] is required for an irregular todo."
        assert week_day is not None, "[week_day] is required for an irregular todo."
        assert week_number is not None, "[week_number] is required for an irregular todo."

        return domain.Frequency.irregular(
            month=domain.Month.from_int(month),
            week_day=domain.Weekday.from_int(week_day),
            week_number=week_number,
            advance_display_days=advance_display_days,
            expire_display_days=expire_display_days,
            start_date=start_date,
        )
    elif frequency == "memorial_day":
        return domain.Frequency.memorial_day(
            advance_display_days=advance_display_days,
            expire_display_days=expire_display_days,
            start_date=start_date,
        )
    elif frequency == "monthly":
        assert month_day is not None, "[month_day] is required if the frequency is 'monthly'."

        return domain.Frequency.monthly(
            month_day=month_day,
            advance_display_days=advance_display_days,
            expire_display_days=expire_display_days,
            start_date=start_date,
        )
    elif frequency == "once":
        assert due_date is not None, "[due_date] is required if the frequency is 'once'."

        return domain.Frequency.once(
            due_date=due_date,
            advance_display_days=advance_display_days,
            expire_display_days=expire_display_days,
            start_date=start_date,
        )
    elif frequency == "weekly":
        assert week_day is not None, "[week_day] is required if the frequency is 'weekly'."

        return domain.Frequency.weekly(
            week_day=domain.Weekday.from_int(week_day),
            advance_display_days=advance_display_days,
            expire_display_days=expire_display_days,
            start_date=start_date,
        )
    elif frequency == "xdays":
        assert days is not None, "[days] is required if the frequency is 'xdays'."

        return domain.Frequency.xdays(
            days=days,
            advance_display_days=advance_display_days,
            expire_display_days=expire_display_days,
            start_date=start_date,
        )
    elif frequency == "yearly":
        assert month is not None, "[month] is required if the frequency is 'yearly'."
        assert month_day is not None, "[month_day] is required if the frequency is 'yearly'."

        return domain.Frequency.yearly(
            month=domain.Month.from_int(month),
            month_day=month_day,
            advance_display_days=advance_display_days,
            expire_display_days=expire_display_days,
            start_date=start_date,
        )
    else:
        raise ValueError(f"Unrecognized frequency, {frequency!r}.")


if __name__ == '__main__':
    eng = db.create_engine()
    repo = DbTodoRepository(engine=eng)
    for r in repo.all():
        print(r)