import datetime

from src import domain
from src.domain import date_calc


def test_memorial_day_due_date() -> None:
    due_date = date_calc.due_date(
        frequency=domain.Frequency.memorial_day(
            advance_display_days=30,
            expire_display_days=30,
            start_date=datetime.date(1900, 1, 1),
        ),
        ref_date=datetime.date(2024, 1, 1),
    )

    assert due_date == datetime.date(2023, 5, 29)
