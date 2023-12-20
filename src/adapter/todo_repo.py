import datetime

import sqlalchemy as sa
from loguru import logger

from src import domain
from src.adapter import db, category_repo, user_repo

__all__ = (
    "add",
    "delete",
    "get",
    "update",
    "where",
)


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
def add(*, con: sa.Connection, todo: domain.Todo) -> None | domain.Error:
    try:
        if todo.todo_id == "":
            return domain.Error.new(f"Not a valid uuid: {todo.todo_id}", todo=todo)

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

        con.execute(
            sa.insert(db.todo).values(
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

        return None
    except Exception as e:
        logger.error(f"{__file__}.add({todo=!r}) failed: {e}")

        return domain.Error.new(str(e), todo=todo)


def delete(*, con: sa.Connection, todo_id: str) -> None | domain.Error:
    try:
        con.execute(sa.update(db.todo).where(db.todo.c.todo_id == todo_id).values(date_deleted=datetime.datetime.now()))

        return None
    except Exception as e:
        logger.error(f"{__file__}.delete({todo_id=!r}) failed: {e}")

        return domain.Error.new(str(e), todo_id=todo_id)


def get(*, con: sa.Connection, todo_id: str) -> domain.Todo | None | domain.Error:
    try:
        result = con.execute(sa.select(db.todo).where(db.todo.c.todo_id == todo_id))

        row = result.one_or_none()

        if row is None:
            return None

        user = user_repo.get(
            con=con,
            user_id=row.user_id,
        )
        if isinstance(user, domain.Error):
            return user

        if row.last_completed_by:
            last_completed_by = user_repo.get(
                con=con,
                user_id=row.last_completed_by,
            )
            if isinstance(last_completed_by, domain.Error):
                return last_completed_by
        else:
            last_completed_by = None

        if row.prior_completed_by:
            prior_completed_by = user_repo.get(
                con=con,
                user_id=row.prior_completed_by,
            )
            if isinstance(prior_completed_by, domain.Error):
                return prior_completed_by
        else:
            prior_completed_by = None

        category = category_repo.get(
            con=con,
            category_id=row.category_id,
        )
        if isinstance(category, domain.Error):
            return category

        if category is None:
            return domain.Error.new(f"category_id, {row.category_id}, not found.")

        return domain.Todo(
            todo_id=row.todo_id,
            template_todo_id=row.template_todo_id,
            category=category,
            user=user or domain.DEFAULT_USER,
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
    except Exception as e:
        logger.error(f"{__file__}.get({todo_id=!r}) failed: {e}")

        return domain.Error.new(str(e), todo_id=todo_id)


def update(*, con: sa.Connection, todo: domain.Todo) -> None | domain.Error:
    try:
        if todo.frequency.week_day is None:
            week_day = None
        else:
            week_day = todo.frequency.week_day.to_int()

        if todo.frequency.month is None:
            month = None
        else:
            month = todo.frequency.month.to_int()

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
                date_deleted=None,
                frequency=FREQUENCY_NAME_LKP[todo.frequency.name],
                week_day=week_day,
                week_number=todo.frequency.week_number,
                month=month,
                month_day=todo.frequency.month_day,
                days=todo.frequency.days,
                due_date=domain.due_date(frequency=todo.frequency, ref_date=datetime.date.today()),
                last_completed=todo.last_completed,
                prior_completed=todo.prior_completed,
                last_completed_by=None if todo.last_completed_by is None else todo.last_completed_by.user_id,
                prior_completed_by=None if todo.prior_completed_by is None else todo.prior_completed_by.user_id,
            )
        )

        return None
    except Exception as e:
        logger.error(f"{__file__}.update({todo=!r}) failed: {e}")

        return domain.Error.new(str(e), todo=todo)


def where(
    *,
    con: sa.Connection,
    category_id: str | domain.Unspecified,
    user_id: str | domain.Unspecified,
    description_starts_with: str | domain.Unspecified,
    template_todo_id: str | domain.Unspecified,
) -> list[domain.Todo] | domain.Error:
    try:
        categories = category_repo.where(con=con, active=False)
        if isinstance(categories, domain.Error):
            return categories

        users = user_repo.where(con=con, active=False)
        if isinstance(users, domain.Error):
            return users

        qry = sa.select(db.todo).where(db.todo.c.date_deleted == None)  # noqa

        if isinstance(category_id, str):
            if category_id:
                qry = qry.where(db.todo.c.category_id == category_id)

        if isinstance(user_id, str):
            if user_id:
                qry = qry.where(db.todo.c.user_id == user_id)

        if isinstance(description_starts_with, str):
            qry = qry.where(db.todo.c.description.ilike(description_starts_with + "%"))

        if isinstance(template_todo_id, str):
            qry = qry.where(db.todo.c.template_todo_id == template_todo_id)

        category_by_id = {category.category_id: category for category in categories}

        user_by_id = {user.user_id: user for user in users}

        todos: list[domain.Todo] = []
        for row in con.execute(qry).fetchall():
            category = category_by_id.get(row.category_id, domain.TODO_CATEGORY)

            user = user_by_id.get(row.user_id, domain.DEFAULT_USER)

            last_completed_by = user_by_id.get(row.last_completed_by)

            prior_completed_by = user_by_id.get(row.prior_completed_by)

            todo = domain.Todo(
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

            todos.append(todo)

        return todos
    except Exception as e:
        logger.error(f"{__file__}.where({category_id=!r}, {user_id=!r}, {description_starts_with=!r}) failed: {e}")

        return domain.Error.new(
            str(e),
            category_id=category_id,
            user_id=user_id,
            description_starts_with=description_starts_with,
        )


# def where_category(*, con: sa.Connection, category_id: str) -> list[domain.Todo] | domain.Error:
#     user_lkp = {user.user_id: user for user in user_repo.all_users(con=con)}
#
#     if category := category_repo.get(con=con, category_id=category_id):
#         result = con.execute(
#             sa.select(db.todo)
#             .where(db.todo.c.date_deleted == None)  # noqa
#             .where(db.todo.c.category_id == category_id)
#         )
#
#         return [
#             domain.Todo(
#                 todo_id=row.todo_id,
#                 template_todo_id=row.template_todo_id,
#                 category=category,
#                 user=user_lkp[row.user_id],
#                 description=row.description,
#                 frequency=_parse_frequency(
#                     advance_display_days=row.advance_days,
#                     days=row.days,
#                     due_date=row.due_date,
#                     expire_display_days=row.expire_days,
#                     frequency=row.frequency,
#                     month=row.month,
#                     month_day=row.month_day,
#                     start_date=row.start_date,
#                     week_day=row.week_day,
#                     week_number=row.week_number,
#                 ),
#                 note=row.note,
#                 last_completed=row.last_completed,
#                 last_completed_by=user_lkp.get(row.last_completed_by or ""),
#                 prior_completed=row.prior_completed,
#                 prior_completed_by=user_lkp.get(row.prior_completed_by or ""),
#                 date_added=row.date_added,
#                 date_updated=row.date_updated,
#             )
#             for row in result.fetchall()
#         ]
#
#     return []


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
