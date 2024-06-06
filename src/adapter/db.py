import functools

import sqlalchemy as sa
from loguru import logger

from src import domain

__all__ = (
    "category",
    "create_engine",
    "create_tables",
    "todo",
    "user",
)


meta = sa.MetaData()


@functools.lru_cache
def todo(*, schema: str | None) -> sa.Table:
    return sa.Table(
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
        schema=schema,
    )


@functools.lru_cache
def category(*, schema: str | None) -> sa.Table:
    return sa.Table(
        "category",
        meta,
        sa.Column("category_id", sa.Text, primary_key=True),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("note", sa.Text, nullable=False),
        sa.Column("date_added", sa.DateTime, nullable=False),
        sa.Column("date_updated", sa.DateTime, nullable=True),
        sa.Column("date_deleted", sa.DateTime, nullable=True),
        schema=schema,
    )


@functools.lru_cache
def user(*, schema: str | None) -> sa.Table:
    return sa.Table(
        "user",
        meta,
        sa.Column("user_id", sa.Text, primary_key=True),
        sa.Column("display_name", sa.Text, nullable=False),
        sa.Column("username", sa.Text, nullable=False),
        sa.Column("is_admin", sa.Boolean, nullable=False),
        sa.Column("date_added", sa.DateTime, nullable=False),
        sa.Column("date_updated", sa.DateTime, nullable=True),
        sa.Column("date_deleted", sa.DateTime, nullable=True),
        schema=schema,
    )


def create_tables(*, schema: str | None, engine: sa.engine.Engine) -> None | domain.Error:
    try:
        meta.create_all(
            bind=engine,
            tables=[
                todo(schema=schema),
                category(schema=schema),
                user(schema=schema),
            ],
            checkfirst=True,
        )
        return None
    except Exception as e:
        logger.error(f"{__file__}.create_tables({schema=!r}, ...): {e!s}")

        return domain.Error.new(str(e))


def create_engine(*, url: str) -> sa.engine.Engine | domain.Error:
    # noinspection PyBroadException
    try:
        return sa.create_engine(url=url)
    except:  # noqa: E722
        import traceback

        logger.error(traceback.format_exc())
        logger.error(f"{__file__}.create_engine(...) failed.")

        return domain.Error.new("An error occurred while creating engine.")
