from __future__ import annotations

import datetime

import sqlmodel as sm

from src import domain
from src.adapter import db
from src.adapter.db_category_repository import DbCategoryRepository
from src.adapter.db_user_repository import DbUserRepository

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

        if todo.last_completed_by:
            last_completed_by_user_id = todo.last_completed_by.user_id
        else:
            last_completed_by_user_id = None

        if todo.prior_completed_by:
            prior_completed_by_user_id = todo.prior_completed_by.user_id
        else:
            prior_completed_by_user_id = None

        todo_orm = db.Todo(
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

        self._session.add(todo_orm)

    def all(self) -> list[domain.Todo]:
        category_repo = DbCategoryRepository(session=self._session)

        category_lkp = {
            category.category_id: category
            for category in category_repo.get_active()
        }

        user_repo = DbUserRepository(session=self._session)

        user_lkp = {
            user.user_id: user
            for user in user_repo.all()
        }

        result = self._session.exec(
            sm.select(db.Todo)
            .where(db.Todo.date_deleted == None)
        )

        return [
            domain.Todo(
                todo_id=todo_orm.todo_id,
                template_todo_id=todo_orm.template_todo_id,
                category=category_lkp[todo_orm.category_id],
                user=user_lkp.get(todo_orm.user_id, domain.DEFAULT_USER),
                description=todo_orm.description,
                frequency=_parse_frequency(
                    row=todo_orm,
                    advance_display_days=todo_orm.advance_days,
                    expire_display_days=todo_orm.expire_days,
                    start_date=todo_orm.start_date,
                ),
                note=todo_orm.note,
                last_completed=todo_orm.last_completed,
                last_completed_by=user_lkp.get(todo_orm.last_completed_by or ""),
                prior_completed=todo_orm.prior_completed,
                prior_completed_by=user_lkp.get(todo_orm.prior_completed_by or ""),
                date_added=todo_orm.date_added,
                date_updated=todo_orm.date_updated,
            )
            for todo_orm in result
        ]

    def delete(self, *, todo_id: str) -> None:
        if orm := self._get_orm(todo_id=todo_id):
            # self._session.delete(orm)
            orm.date_deleted = datetime.datetime.now()
            self._session.add(orm)

    def get(self, *, todo_id: str) -> domain.Todo | None:
        todo_orm = self._get_orm(todo_id=todo_id)

        if todo_orm is None:
            return None

        category_repo = DbCategoryRepository(session=self._session)

        user_repo = DbUserRepository(session=self._session)

        user = user_repo.get(user_id=todo_orm.user_id) or domain.DEFAULT_USER

        if todo_orm.last_completed_by:
            last_completed_by = user_repo.get(user_id=todo_orm.last_completed_by)
        else:
            last_completed_by = None

        if todo_orm.prior_completed_by:
            prior_completed_by = user_repo.get(user_id=todo_orm.prior_completed_by)
        else:
            prior_completed_by = None

        if category := category_repo.get(category_id=todo_orm.category_id):
            return _orm_to_domain(
                todo_orm=todo_orm,
                category=category,
                user=user,
                last_completed_by=last_completed_by,
                prior_completed_by=prior_completed_by,
            )

        return None

    def update(self, *, todo: domain.Todo) -> None:
        todo_orm = self._get_orm(todo_id=todo.todo_id)

        assert todo_orm is not None

        if todo.frequency.week_day is None:
            week_day = None
        else:
            week_day = todo.frequency.week_day.to_int()

        if todo.frequency.month is None:
            month = None
        else:
            month = todo.frequency.month.to_int()

        todo_orm.template_todo_id = todo.template_todo_id
        todo_orm.user_id = todo.user.user_id
        todo_orm.expire_days = todo.frequency.expire_display_days
        todo_orm.advance_days = todo.frequency.advance_display_days
        todo_orm.category_id = todo.category.category_id
        todo_orm.description = todo.description
        todo_orm.note = todo.note
        todo_orm.start_date = todo.frequency.start_date
        todo_orm.date_added = todo.date_added
        todo_orm.date_updated = todo.date_updated
        todo_orm.frequency = FREQUENCY_NAME_LKP[todo.frequency.name]
        todo_orm.week_day = week_day
        todo_orm.week_number = todo.frequency.week_number
        todo_orm.month = month
        todo_orm.month_day = todo.frequency.month_day
        todo_orm.days = todo.frequency.days
        todo_orm.due_date = todo.frequency.due_date
        todo_orm.last_completed = todo.last_completed
        todo_orm.prior_completed = todo.prior_completed
        if todo.last_completed_by:
            last_completed_by_user_id: str | None = todo.last_completed_by.user_id
        else:
            last_completed_by_user_id = None
        todo_orm.last_completed_by = last_completed_by_user_id

        if todo.prior_completed_by:
            prior_completed_by_user_id: str | None = todo.prior_completed_by.user_id
        else:
            prior_completed_by_user_id = None
        todo_orm.prior_completed_by = prior_completed_by_user_id

        self._session.add(todo_orm)

    def where_category(self, *, category_id: str) -> list[domain.Todo]:
        category_repo = DbCategoryRepository(session=self._session)

        user_repo = DbUserRepository(session=self._session)

        user_lkp = {
            user.user_id: user
            for user in user_repo.all()
        }

        if category := category_repo.get(category_id=category_id):
            return [
                _orm_to_domain(
                    todo_orm=todo_orm,
                    category=category,
                    user=user_lkp.get(todo_orm.user_id, domain.DEFAULT_USER),
                    last_completed_by=user_lkp.get(todo_orm.last_completed_by or ""),
                    prior_completed_by=user_lkp.get(todo_orm.prior_completed_by or ""),
                )
                for todo_orm in self._session.exec(
                    sm.select(db.Todo)
                    .where(db.Todo.date_deleted == None)  # noqa
                    .where(db.Todo.category_id == category_id)
                )
            ]

        return []

    def _get_orm(self, *, todo_id: str) -> db.Todo | None:
        return self._session.exec(
            sm.select(db.Todo).where(db.Todo.todo_id == todo_id)
        ).one_or_none()


def _parse_frequency(
    *,
    row: db.Todo,
    advance_display_days: int,
    expire_display_days: int,
    start_date: datetime.date,
) -> domain.Frequency:
    if row.frequency == "daily":
        return domain.Frequency.daily(start_date=start_date)
    elif row.frequency == "easter":
        return domain.Frequency.easter(
            advance_display_days=advance_display_days,
            expire_display_days=expire_display_days,
            start_date=start_date,
        )
    elif row.frequency == "irregular":
        assert row.month is not None, "[month] is required for an irregular todo."
        assert row.week_day is not None, "[week_day] is required for an irregular todo."
        assert row.week_number is not None, "[week_number] is required for an irregular todo."

        return domain.Frequency.irregular(
            month=domain.Month.from_int(row.month),
            week_day=domain.Weekday.from_int(row.week_day),
            week_number=row.week_number,
            advance_display_days=advance_display_days,
            expire_display_days=expire_display_days,
            start_date=start_date,
        )
    elif row.frequency == "memorial_day":
        return domain.Frequency.memorial_day(
            advance_display_days=advance_display_days,
            expire_display_days=expire_display_days,
            start_date=start_date,
        )
    elif row.frequency == "monthly":
        assert row.month_day is not None, "[month_day] is required if the frequency is 'monthly'."

        return domain.Frequency.monthly(
            month_day=row.month_day,
            advance_display_days=advance_display_days,
            expire_display_days=expire_display_days,
            start_date=start_date,
        )
    elif row.frequency == "once":
        assert row.due_date is not None, "[due_date] is required if the frequency is 'once'."

        return domain.Frequency.once(
            due_date=row.due_date,
            advance_display_days=advance_display_days,
            expire_display_days=expire_display_days,
            start_date=start_date,
        )
    elif row.frequency == "weekly":
        assert row.week_day is not None, "[week_day] is required if the frequency is 'weekly'."

        return domain.Frequency.weekly(
            week_day=domain.Weekday.from_int(row.week_day),
            advance_display_days=advance_display_days,
            expire_display_days=expire_display_days,
            start_date=start_date,
        )
    elif row.frequency == "xdays":
        assert row.days is not None, "[days] is required if the frequency is 'xdays'."

        return domain.Frequency.xdays(
            days=row.days,
            advance_display_days=advance_display_days,
            expire_display_days=expire_display_days,
            start_date=start_date,
        )
    elif row.frequency == "yearly":
        assert row.month is not None, "[month] is required if the frequency is 'yearly'."
        assert row.month_day is not None, "[month_day] is required if the frequency is 'yearly'."

        return domain.Frequency.yearly(
            month=domain.Month.from_int(row.month),
            month_day=row.month_day,
            advance_display_days=advance_display_days,
            expire_display_days=expire_display_days,
            start_date=start_date,
        )
    else:
        raise ValueError(f"Unrecognized frequency, {row.frequency!r}.")


def _orm_to_domain(
    *,
    todo_orm: db.Todo,
    category: domain.Category,
    user: domain.User,
    last_completed_by: domain.User | None,
    prior_completed_by: domain.User | None,
) -> domain.Todo:
    return domain.Todo(
        todo_id=todo_orm.todo_id,
        template_todo_id=todo_orm.template_todo_id,
        user=user,
        category=category,
        description=todo_orm.description,
        frequency=_parse_frequency(
            row=todo_orm,
            advance_display_days=todo_orm.advance_days,
            expire_display_days=todo_orm.expire_days,
            start_date=todo_orm.start_date,
        ),
        note=todo_orm.note,
        last_completed=todo_orm.last_completed,
        prior_completed=todo_orm.prior_completed,
        last_completed_by=last_completed_by,
        prior_completed_by=prior_completed_by,
        date_added=todo_orm.date_added,
        date_updated=todo_orm.date_updated,
    )
