import datetime

from src.domain.todo import Todo
from src.domain.create_uuid import create_uuid
from src.domain.month import Month
from src.domain.todo_category import TodoCategory
from src.domain.weekday import Weekday

__all__ = ("HOLIDAYS",)


HOLIDAYS = [
    Todo.irregular(
        todo_id=create_uuid(),
        advance_days=30,
        expire_days=30,
        category=TodoCategory.Reminder,
        description="Thanksgiving",
        month=Month.November,
        week_day=Weekday.Thursday,
        week_number=4,
        note="",
        start_date=datetime.date(1900, 1, 1),
        date_added=datetime.datetime(1900, 1, 1),
        date_deleted=None,
        date_updated=None,
    ),
    Todo.yearly(
        todo_id=create_uuid(),
        advance_days=30,
        expire_days=30,
        category=TodoCategory.Reminder,
        description="Christmas",
        month=Month.November,
        month_day=25,
        note="",
        start_date=datetime.date(1900, 1, 1),
        date_added=datetime.datetime(1900, 1, 1),
        date_deleted=None,
        date_updated=None,
    ),
    Todo.irregular(
        todo_id=create_uuid(),
        advance_days=30,
        expire_days=30,
        category=TodoCategory.Reminder,
        description="Fathers Day",
        month=Month.June,
        week_day=Weekday.Sunday,
        week_number=3,
        note="",
        start_date=datetime.date(1900, 1, 1),
        date_added=datetime.datetime(1900, 1, 1),
        date_deleted=None,
        date_updated=None,
    ),
    Todo.irregular(
        todo_id=create_uuid(),
        advance_days=30,
        expire_days=30,
        category=TodoCategory.Reminder,
        description="Mothers Day",
        month=Month.May,
        week_day=Weekday.Sunday,
        week_number=2,
        note="",
        start_date=datetime.date(1900, 1, 1),
        date_added=datetime.datetime(1900, 1, 1),
        date_deleted=None,
        date_updated=None,
    ),
    Todo.irregular(
        todo_id=create_uuid(),
        advance_days=30,
        expire_days=30,
        category=TodoCategory.Reminder,
        description="Labor Day",
        month=Month.September,
        week_day=Weekday.Monday,
        week_number=1,
        note="",
        start_date=datetime.date(1900, 1, 1),
        date_added=datetime.datetime(1900, 1, 1),
        date_deleted=None,
        date_updated=None,
    ),
    Todo.irregular(
        todo_id=create_uuid(),
        advance_days=30,
        expire_days=30,
        category=TodoCategory.Reminder,
        description="Martin Luther King Jr. Day",
        month=Month.January,
        week_day=Weekday.Monday,
        week_number=3,
        note="",
        start_date=datetime.date(1900, 1, 1),
        date_added=datetime.datetime(1900, 1, 1),
        date_deleted=None,
        date_updated=None,
    ),
    Todo.yearly(
        todo_id=create_uuid(),
        advance_days=30,
        expire_days=30,
        category=TodoCategory.Reminder,
        description="New Year's Day",
        month=Month.January,
        month_day=1,
        note="",
        start_date=datetime.date(1900, 1, 1),
        date_added=datetime.datetime(1900, 1, 1),
        date_deleted=None,
        date_updated=None,
    ),
    Todo.irregular(
        todo_id=create_uuid(),
        advance_days=30,
        expire_days=30,
        category=TodoCategory.Reminder,
        description="Presidents' Day",
        month=Month.February,
        week_day=Weekday.Monday,
        week_number=3,
        note="",
        start_date=datetime.date(1900, 1, 1),
        date_added=datetime.datetime(1900, 1, 1),
        date_deleted=None,
        date_updated=None,
    ),
    Todo.easter(todo_id=create_uuid()),
]
