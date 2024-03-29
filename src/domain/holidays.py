import datetime

from src.domain.user import DEFAULT_USER
from src.domain.category import Category
from src.domain.frequency import Frequency
from src.domain.month import Month
from src.domain.todo import Todo
from src.domain.weekday import Weekday

__all__ = ("HOLIDAY_CATEGORY", "HOLIDAYS")


HOLIDAY_CATEGORY = Category(
    category_id="f68df6c9efb64ecea58cbd87e859942c",
    name="Holiday",
    note="",
    date_added=datetime.datetime(1900, 1, 1),
    date_updated=None,
    date_deleted=None,
)

# TODO add Veteran's day
HOLIDAYS = [
    Todo.irregular(
        todo_id="f89904629ba24d5c8ed4b2525a8253d9",
        template_todo_id="f89904629ba24d5c8ed4b2525a8253d9",
        advance_display_days=30,
        expire_display_days=30,
        user=DEFAULT_USER,
        category=HOLIDAY_CATEGORY,
        description="Thanksgiving",
        month=Month.November,
        week_day=Weekday.Thursday,
        week_number=4,
        note="",
        start_date=datetime.date(1900, 1, 1),
        last_completed=None,
        prior_completed=None,
        last_completed_by=None,
        prior_completed_by=None,
        date_added=datetime.datetime(1900, 1, 1),
        date_updated=None,
    ),
    Todo.yearly(
        todo_id="73e68c07f0cf4b2e804f17be617b9623",
        template_todo_id="73e68c07f0cf4b2e804f17be617b9623",
        advance_display_days=30,
        expire_display_days=30,
        user=DEFAULT_USER,
        category=HOLIDAY_CATEGORY,
        description="Christmas",
        month=Month.December,
        month_day=25,
        note="",
        start_date=datetime.date(1900, 1, 1),
        last_completed=None,
        prior_completed=None,
        last_completed_by=None,
        prior_completed_by=None,
        date_added=datetime.datetime(1900, 1, 1),
        date_updated=None,
    ),
    Todo.irregular(
        todo_id="5e08036c15934b50a22b750453bc5511",
        template_todo_id="5e08036c15934b50a22b750453bc5511",
        advance_display_days=30,
        expire_display_days=30,
        user=DEFAULT_USER,
        category=HOLIDAY_CATEGORY,
        description="Fathers Day",
        month=Month.June,
        week_day=Weekday.Sunday,
        week_number=3,
        note="",
        start_date=datetime.date(1900, 1, 1),
        last_completed=None,
        prior_completed=None,
        last_completed_by=None,
        prior_completed_by=None,
        date_added=datetime.datetime(1900, 1, 1),
        date_updated=None,
    ),
    Todo.irregular(
        todo_id="4c83c2b0d66e44a899305f47994e31fc",
        template_todo_id="4c83c2b0d66e44a899305f47994e31fc",
        advance_display_days=30,
        expire_display_days=30,
        user=DEFAULT_USER,
        category=HOLIDAY_CATEGORY,
        description="Mothers Day",
        month=Month.May,
        week_day=Weekday.Sunday,
        week_number=2,
        note="",
        start_date=datetime.date(1900, 1, 1),
        last_completed=None,
        prior_completed=None,
        last_completed_by=None,
        prior_completed_by=None,
        date_added=datetime.datetime(1900, 1, 1),
        date_updated=None,
    ),
    Todo.irregular(
        todo_id="8eff18d02d014435ab5d24ade713e9f3",
        template_todo_id="8eff18d02d014435ab5d24ade713e9f3",
        advance_display_days=30,
        expire_display_days=30,
        user=DEFAULT_USER,
        category=HOLIDAY_CATEGORY,
        description="Labor Day",
        month=Month.September,
        week_day=Weekday.Monday,
        week_number=1,
        note="",
        start_date=datetime.date(1900, 1, 1),
        last_completed=None,
        prior_completed=None,
        last_completed_by=None,
        prior_completed_by=None,
        date_added=datetime.datetime(1900, 1, 1),
        date_updated=None,
    ),
    Todo.irregular(
        todo_id="e8bf37dc16014b55a139d2b5a8331b2b",
        template_todo_id="e8bf37dc16014b55a139d2b5a8331b2b",
        advance_display_days=30,
        expire_display_days=30,
        user=DEFAULT_USER,
        category=HOLIDAY_CATEGORY,
        description="Martin Luther King Jr. Day",
        month=Month.January,
        week_day=Weekday.Monday,
        week_number=3,
        note="",
        start_date=datetime.date(1900, 1, 1),
        last_completed=None,
        prior_completed=None,
        last_completed_by=None,
        prior_completed_by=None,
        date_added=datetime.datetime(1900, 1, 1),
        date_updated=None,
    ),
    Todo.yearly(
        todo_id="a16d843d8a1f4544aa647f69920f9c3a",
        template_todo_id="a16d843d8a1f4544aa647f69920f9c3a",
        advance_display_days=30,
        expire_display_days=30,
        user=DEFAULT_USER,
        category=HOLIDAY_CATEGORY,
        description="New Year's Day",
        month=Month.January,
        month_day=1,
        note="",
        start_date=datetime.date(1900, 1, 1),
        last_completed=None,
        prior_completed=None,
        last_completed_by=None,
        prior_completed_by=None,
        date_added=datetime.datetime(1900, 1, 1),
        date_updated=None,
    ),
    Todo.irregular(
        todo_id="349cc855a19b407fb3c5f2f09acd32b0",
        template_todo_id="349cc855a19b407fb3c5f2f09acd32b0",
        advance_display_days=30,
        expire_display_days=30,
        user=DEFAULT_USER,
        category=HOLIDAY_CATEGORY,
        description="Indigenous People's Day",
        month=Month.October,
        week_day=Weekday.Monday,
        week_number=2,
        note="",
        start_date=datetime.date(1900, 1, 1),
        last_completed=None,
        prior_completed=None,
        last_completed_by=None,
        prior_completed_by=None,
        date_added=datetime.datetime(1900, 1, 1),
        date_updated=None,
    ),
    Todo.irregular(
        todo_id="9942876cd4fa433fbd780f2e5d6fac8d",
        template_todo_id="9942876cd4fa433fbd780f2e5d6fac8d",
        advance_display_days=30,
        expire_display_days=30,
        user=DEFAULT_USER,
        category=HOLIDAY_CATEGORY,
        description="Presidents' Day",
        month=Month.February,
        week_day=Weekday.Monday,
        week_number=3,
        note="",
        start_date=datetime.date(1900, 1, 1),
        last_completed=None,
        prior_completed=None,
        last_completed_by=None,
        prior_completed_by=None,
        date_added=datetime.datetime(1900, 1, 1),
        date_updated=None,
    ),
    Todo(
        todo_id="374bf962521c411f830259fc6a2096c3",
        template_todo_id="374bf962521c411f830259fc6a2096c3",
        description="Easter",
        note="",
        user=DEFAULT_USER,
        category=HOLIDAY_CATEGORY,
        frequency=Frequency.easter(
            advance_display_days=30,
            expire_display_days=30,
            start_date=datetime.date(1900, 1, 1),
        ),
        last_completed=None,
        prior_completed=None,
        last_completed_by=None,
        prior_completed_by=None,
        date_added=datetime.datetime(1900, 1, 1),
        date_updated=None,
    ),
    Todo(
        todo_id="68216e9666094d17ad194cf3f9986556",
        template_todo_id="68216e9666094d17ad194cf3f9986556",
        description="Memorial Day",
        note="",
        user=DEFAULT_USER,
        category=HOLIDAY_CATEGORY,
        frequency=Frequency.memorial_day(
            advance_display_days=30,
            expire_display_days=30,
            start_date=datetime.date(1900, 1, 1),
        ),
        last_completed=None,
        prior_completed=None,
        last_completed_by=None,
        prior_completed_by=None,
        date_added=datetime.datetime(1900, 1, 1),
        date_updated=None,
    ),
    Todo(
        todo_id="72ac7442456e45b0a9feb2fe0877fa35",
        template_todo_id="72ac7442456e45b0a9feb2fe0877fa35",
        description="Independence Day",
        note="",
        user=DEFAULT_USER,
        category=HOLIDAY_CATEGORY,
        frequency=Frequency.yearly(
            month=Month.July,
            month_day=4,
            advance_display_days=30,
            expire_display_days=30,
            start_date=datetime.date(1900, 1, 1),
        ),
        last_completed=None,
        prior_completed=None,
        last_completed_by=None,
        prior_completed_by=None,
        date_added=datetime.datetime(1900, 1, 1),
        date_updated=None,
    ),
]
