import functools

import sqlalchemy as sa

from src import domain
from src.adapter import config

__all__ = (
    "category",
    "create_engine",
    "create_tables",
    "todo",
    "user",
)


@functools.lru_cache
def _db_schema() -> str | None:
    try:
        db_schema = config.db_schema()
        if isinstance(db_schema, domain.Error):
            raise Exception("An error occurred while looking up db_schema from config.json.")

        return db_schema
    except:  # noqa: E722
        raise Exception("An error occurred while looking up the the db schema.") from None


meta = sa.MetaData()

todo = sa.Table(
    "todo",
    meta,
    sa.Column("todo_id", sa.Text, primary_key=True),
    sa.Column("description", sa.Text, nullable=False),
    sa.Column("note", sa.Text, nullable=False),
    sa.Column("user_id", sa.Text, nullable=False),
    sa.Column("category_id", sa.Text, nullable=False),
    sa.Column("advance_days", sa.Integer, nullable=False),
    sa.Column("expire_days", sa.Integer, nullable=False),
    sa.Column("start_date", sa.Date, nullable=False),
    sa.Column("last_completed", sa.Date, nullable=True),
    sa.Column("last_completed_by", sa.Text, nullable=True),
    sa.Column("prior_completed", sa.Date, nullable=True),
    sa.Column("prior_completed_by", sa.Text, nullable=True),
    sa.Column("template_todo_id", sa.Text, nullable=True),
    sa.Column("date_added", sa.DateTime, nullable=False),
    sa.Column("date_updated", sa.DateTime, nullable=True),
    sa.Column("date_deleted", sa.DateTime, nullable=True),
    sa.Column("frequency", sa.Text, nullable=False),
    sa.Column("month", sa.Integer, nullable=True),
    sa.Column("week_day", sa.Integer, nullable=True),
    sa.Column("week_number", sa.Integer, nullable=True),
    sa.Column("month_day", sa.Integer, nullable=True),
    sa.Column("days", sa.Integer, nullable=True),
    sa.Column("due_date", sa.Date, nullable=True),
    schema=_db_schema(),
)

category = sa.Table(
    "category",
    meta,
    sa.Column("category_id", sa.Text, primary_key=True),
    sa.Column("name", sa.Text, nullable=False),
    sa.Column("note", sa.Text, nullable=False),
    sa.Column("date_added", sa.DateTime, nullable=False),
    sa.Column("date_updated", sa.DateTime, nullable=True),
    sa.Column("date_deleted", sa.DateTime, nullable=True),
    schema=_db_schema(),
)

user = sa.Table(
    "user",
    meta,
    sa.Column("user_id", sa.Text, primary_key=True),
    sa.Column("display_name", sa.Text, nullable=False),
    sa.Column("username", sa.Text, nullable=False),
    sa.Column("is_admin", sa.Boolean, nullable=False),
    sa.Column("date_added", sa.DateTime, nullable=False),
    sa.Column("date_updated", sa.DateTime, nullable=True),
    sa.Column("date_deleted", sa.DateTime, nullable=True),
    schema=_db_schema(),
)


def create_tables(*, engine: sa.engine.Engine) -> None | domain.Error:
    try:
        meta.create_all(
            bind=engine,
            tables=[todo, category, user],
            checkfirst=True,
        )
        return None
    except Exception as e:
        return domain.Error.new(str(e))


def create_engine(*, url: str) -> sa.engine.Engine | domain.Error:
    # noinspection PyBroadException
    try:
        return sa.create_engine(url=url)
    except:  # noqa: E722
        return domain.Error.new("An error occurred while creating engine.")
