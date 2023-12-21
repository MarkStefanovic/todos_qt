import dataclasses
import datetime
import typing

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


@dataclasses.dataclass(frozen=True, kw_only=True)
class ValidRow:
    todo_id: str
    user_id: str
    category_id: str
    description: str
    note: str
    template_todo_id: str | None
    last_completed: datetime.date | None
    last_completed_by_user_id: str | None
    prior_completed: datetime.date | None
    prior_completed_by_user_id: str | None
    date_added: datetime.datetime
    date_updated: datetime.datetime | None
    frequency: str
    month: int | None
    week_day: int | None
    week_number: int | None
    month_day: int | None
    days: int | None
    due_date: datetime.date | None
    advance_days: int
    expire_days: int
    start_date: datetime.date


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

        category_by_id: dict[str, domain.Category] = {category.category_id: category for category in categories}

        user_by_id: dict[str, domain.User] = {user.user_id: user for user in users}

        todos: list[domain.Todo] = []
        for row in con.execute(qry).fetchall():
            valid_row = _validate_row(row)
            if isinstance(valid_row, domain.Error):
                return valid_row

            category = category_by_id.get(valid_row.category_id, domain.TODO_CATEGORY)

            user = user_by_id.get(valid_row.user_id, domain.DEFAULT_USER)

            if valid_row.last_completed_by_user_id is None:
                last_completed_by: domain.User | None = None
            else:
                last_completed_by = user_by_id.get(valid_row.last_completed_by_user_id)

            if valid_row.prior_completed_by_user_id is None:
                prior_completed_by: domain.User | None = None
            else:
                prior_completed_by = user_by_id.get(valid_row.prior_completed_by_user_id)

            todo = domain.Todo(
                todo_id=valid_row.todo_id,
                template_todo_id=valid_row.template_todo_id,
                category=category,
                user=user,
                description=valid_row.description,
                frequency=_parse_frequency(
                    advance_display_days=valid_row.advance_days,
                    days=valid_row.days,
                    due_date=valid_row.due_date,
                    expire_display_days=valid_row.expire_days,
                    frequency=valid_row.frequency,
                    month=valid_row.month,
                    month_day=valid_row.month_day,
                    start_date=valid_row.start_date,
                    week_day=valid_row.week_day,
                    week_number=valid_row.week_number,
                ),
                note=valid_row.note,
                last_completed=valid_row.last_completed,
                last_completed_by=last_completed_by,
                prior_completed=valid_row.prior_completed,
                prior_completed_by=prior_completed_by,
                date_added=valid_row.date_added,
                date_updated=valid_row.date_updated,
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


def _validate_row(row: sa.Row[typing.Any], /) -> ValidRow | domain.Error:
    try:
        values: dict[str, typing.Any] = {}
        errors: list[str] = []

        if row.todo_id is None:
            errors.append("todo_id is None.")
        else:
            if isinstance(row.todo_id, str):
                values["todo_id"] = row.todo_id
            else:
                errors.append(f"todo_id, {row.todo_id!r}, is not a string.")

        if row.user_id is None:
            errors.append("user_id is None.")
        else:
            if isinstance(row.user_id, str):
                values["user_id"] = row.user_id
            else:
                errors.append(f"user_id, {row.user_id!r}, is not a string.")

        if row.category_id is None:
            errors.append("category_id is None.")
        else:
            if isinstance(row.category_id, str):
                values["category_id"] = row.category_id
            else:
                errors.append(f"category_id, {row.category_id!r}, is not a string.")

        if row.description is None:
            errors.append("description is None.")
        else:
            if isinstance(row.description, str):
                values["description"] = row.description
            else:
                errors.append(f"description, {row.description!r}, is not a string.")

        if row.frequency is None:
            errors.append("frequency is None.")
        else:
            if isinstance(row.frequency, str):
                values["frequency"] = row.frequency
            else:
                errors.append(f"frequency, {row.frequency!r}, is not a string.")

        if row.month is None:
            values["month"] = None
        else:
            if isinstance(row.month, int):
                values["month"] = row.month
            else:
                errors.append(f"month, {row.month!r}, is not an int.")

        if row.week_day is None:
            values["week_day"] = None
        else:
            if isinstance(row.week_day, int):
                values["week_day"] = row.week_day
            else:
                errors.append(f"week_day, {row.week_day!r}, is not an int.")

        if row.week_number is None:
            values["week_number"] = None
        else:
            if isinstance(row.week_number, int):
                values["week_number"] = row.week_number
            else:
                errors.append(f"week_number, {row.week_number!r}, is not an int.")

        if row.month_day is None:
            values["month_day"] = None
        else:
            if isinstance(row.month_day, int):
                values["month_day"] = row.month_day
            else:
                errors.append(f"month_day, {row.month_day!r}, is not an int.")

        if row.days is None:
            values["days"] = None
        else:
            if isinstance(row.days, int):
                values["days"] = row.days
            else:
                errors.append(f"days, {row.days!r}, is not an int.")

        if row.due_date is None:
            values["due_date"] = None
        else:
            if isinstance(row.due_date, datetime.date):
                values["due_date"] = row.due_date
            else:
                errors.append(f"due_date, {row.due_date!r}, is not a date.")

        if row.note is None:
            errors.append("note is None.")
        else:
            if isinstance(row.note, str):
                values["note"] = row.note
            else:
                errors.append(f"note, {row.note!r}, is not a string.")

        if row.template_todo_id is None:
            values["template_todo_id"] = None
        else:
            if isinstance(row.template_todo_id, str):
                values["template_todo_id"] = row.template_todo_id
            else:
                errors.append(f"template_todo_id, {row.template_todo_id!r}, is not a string.")

        if row.last_completed is None:
            values["last_completed"] = None
        else:
            if isinstance(row.last_completed, datetime.date):
                values["last_completed"] = row.last_completed
            else:
                errors.append(f"last_completed, {row.last_completed!r}, is not a date.")

        if row.prior_completed is None:
            values["prior_completed"] = None
        else:
            if isinstance(row.prior_completed, datetime.date):
                values["prior_completed"] = row.prior_completed
            else:
                errors.append(f"prior_completed, {row.prior_completed!r}, is not a date.")

        if row.last_completed_by_user_id is None:
            errors.append("last_completed_by_user_id is None.")
        else:
            if isinstance(row.last_completed_by_user_id, str):
                values["last_completed_by_user_id"] = row.last_completed_by_user_id
            else:
                errors.append(f"last_completed_by_user_id, {row.last_completed_by_user_id!r}, is not a string.")

        if row.prior_completed_by_user_id is None:
            errors.append("prior_completed_by_user_id is None.")
        else:
            if isinstance(row.prior_completed_by_user_id, str):
                values["prior_completed_by_user_id"] = row.prior_completed_by_user_id
            else:
                errors.append(f"prior_completed_by_user_id, {row.prior_completed_by_user_id!r}, is not a string.")

        if row.date_added is None:
            errors.append("date_added is None.")
        else:
            if isinstance(row.date_added, datetime.datetime):
                values["date_added"] = row.date_added
            else:
                errors.append(f"date_added, {row.date_added!r}, is not a datetime.")

        if row.date_updated is None:
            values["date_updated"] = None
        else:
            if isinstance(row.date_updated, datetime.datetime):
                values["date_updated"] = row.date_updated
            else:
                errors.append(f"date_updated, {row.date_updated!r}, is not a datetime.")

        if row.advance_days is None:
            errors.append("advance_days is None.")
        else:
            if isinstance(row.advance_days, int):
                values["advance_days"] = row.advance_days
            else:
                errors.append(f"advance_days, {row.advance_days!r}, is not an int.")

        if row.expire_days is None:
            errors.append("expire_days is None.")
        else:
            if isinstance(row.expire_days, int):
                values["expire_days"] = row.expire_days
            else:
                errors.append(f"expire_days, {row.expire_days!r}, is not an int.")

        if row.start_date is None:
            values["start_date"] = None
        else:
            if isinstance(row.start_date, datetime.date):
                values["start_date"] = row.start_date
            else:
                errors.append(f"start_date, {row.start_date!r}, is not a date.")

        return ValidRow(**values)
    except Exception as e:
        logger.error(f"{__file__}._validate_row({row=!r}) failed: {e!s}")

        return domain.Error.new(str(e), row=row)


if __name__ == "__main__":
    eng = db.create_engine()
    if isinstance(eng, domain.Error):
        raise Exception(str(eng))

    with eng.begin() as cn:
        cs = where(
            con=cn,
            category_id=domain.Unspecified(),
            user_id=domain.Unspecified(),
            description_starts_with=domain.Unspecified(),
            template_todo_id=domain.Unspecified(),
        )
        if isinstance(cs, domain.Error):
            raise Exception(str(cs))

        for c in cs:
            print(c)
