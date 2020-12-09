import datetime

import pytest

from src.domain.frequencies import easter


@pytest.mark.parametrize(
    "year, expected",
    [
        (2017, datetime.date(2017, 4, 16)),
        (2018, datetime.date(2018, 4, 1)),
        (2019, datetime.date(2019, 4, 21)),
        (2020, datetime.date(2020, 4, 12)),
        (2021, datetime.date(2021, 4, 4)),
        (2022, datetime.date(2022, 4, 17)),
        (2023, datetime.date(2023, 4, 9)),
        (2024, datetime.date(2024, 3, 31)),
        (2025, datetime.date(2025, 4, 20)),
    ],
)
def test_calculate_easter(year: int, expected: datetime.date) -> None:
    actual = easter.calculate_easter(year)
    assert actual == expected
