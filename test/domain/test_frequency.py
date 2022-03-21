import datetime

import pytest

from src import domain


@pytest.mark.parametrize(
    "weekday,today,expected,description",
    [
        (
            domain.Weekday.Monday,
            datetime.date(2020, 11, 16),
            datetime.date(2020, 11, 16),
            "On Monday a Monday todo should return today.",
        ),
        (
            domain.Weekday.Tuesday,
            datetime.date(2020, 11, 16),
            datetime.date(2020, 11, 10),
            "On Monday, a Tuesday todo with no advance notice should return the previous Tuesday.",
        ),
        (
            domain.Weekday.Sunday,
            datetime.date(2020, 11, 16),
            datetime.date(2020, 11, 15),
            "On Monday, a Sunday todo with no advance notice should return the previous Sunday.",
        ),
    ],
)
def test_weekday(
    weekday: domain.Weekday,
    today: datetime.date,
    expected: datetime.date,
    description: str,
) -> None:
    todo = domain.Weekly(weekday)
    actual = todo.current_date(advance_days=0, today=today)
    assert actual == expected, description
