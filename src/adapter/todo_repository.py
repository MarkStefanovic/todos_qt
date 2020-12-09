import datetime
import typing

from src import domain
from src.adapter import sqlite_db

__all__ = ("SqliteTodoRepository",)


class SqliteTodoRepository(domain.TodoRepository):
    def __init__(self, sqlite_db: sqlite_db.SqliteDb):
        super().__init__()
        self._db = sqlite_db

    def add(self, /, item: domain.Todo) -> None:
        dto = item.to_dto()
        self._db.execute(
            sql="""
                INSERT INTO todo ( 
                    description,
                    frequency,
                    month,
                    week_day,
                    month_day,
                    year,
                    week_number,
                    date_added,
                    date_completed,
                    advance_days,
                    start_date,
                    days,
                    note,
                    category
                ) VALUES (
                    :description,
                    :frequency,
                    :month,
                    :week_day,
                    :month_day,
                    :year,
                    :week_number,
                    :date_added,
                    :date_completed,
                    :advance_days,
                    :start_date,
                    :days,
                    :note,
                    :category
                )
            """,
            params=[
                {
                    "description": dto.description,
                    "frequency": dto.frequency,
                    "month": dto.month,
                    "week_day": dto.week_day,
                    "month_day": dto.month_day,
                    "year": dto.year,
                    "week_number": dto.week_number,
                    "date_added": dto.date_added,
                    "date_completed": dto.date_completed,
                    "advance_days": dto.advance_days,
                    "start_date": dto.start_date,
                    "days": dto.days,
                    "note": dto.note,
                    "category": dto.category,
                }
            ],
        )

    def all(self) -> typing.List[domain.Todo]:
        rows = self._db.execute("SELECT * FROM todo")
        dtos = rows.as_dtos(domain.TodoDTO)
        return sorted(
            (row.to_domain() for row in dtos),
            key=lambda todo: todo.date_completed or datetime.date(1970, 1, 1),
        )

    def get_id(self, /, todo_id: int) -> domain.Todo:
        result = self._db.execute(
            sql="SELECT * FROM todo WHERE id = :id",
            params=[{"id": todo_id}],
        )
        if result:
            dto = result.as_dtos(domain.TodoDTO)[0]
            return dto.to_domain()
        else:
            raise domain.exceptions.DeveloperError(
                f"Todo id that does not exist, {todo_id!r}."
            )

    def mark_completed(
        self, item_id: int, today: datetime.date = datetime.date.today()
    ) -> None:
        self._db.execute(
            sql="UPDATE todo SET date_completed = :date_completed WHERE id = :id",
            params=[{"date_completed": datetime.date.today(), "id": item_id}],
        )

    def remove(self, /, item_id: int) -> None:
        self._db.execute(
            sql="DELETE FROM todo WHERE id = :id",
            params=[{"id": item_id}],
        )

    def update(self, /, item: domain.Todo) -> None:
        dto = item.to_dto()
        self._db.execute(
            sql="""
                UPDATE todo 
                SET description = :description,
                    frequency = :frequency,
                    month = :month,
                    week_day = :week_day,
                    month_day = :month_day,
                    year = :year,
                    week_number = :week_number,
                    date_added = :date_added,
                    date_completed = :date_completed,
                    advance_days = :advance_days,
                    start_date = :start_date,
                    days = :days,
                    note = :note,
                    category = :category
                WHERE id = :id
            """,
            params=[
                {
                    "description": dto.description,
                    "frequency": dto.frequency,
                    "month": dto.month,
                    "week_day": dto.week_day,
                    "month_day": dto.month_day,
                    "year": dto.year,
                    "week_number": dto.week_number,
                    "date_added": dto.date_added,
                    "date_completed": dto.date_completed,
                    "advance_days": dto.advance_days,
                    "start_date": dto.start_date,
                    "days": dto.days,
                    "note": dto.note,
                    "category": dto.category,
                    "id": dto.id,
                }
            ],
        )
