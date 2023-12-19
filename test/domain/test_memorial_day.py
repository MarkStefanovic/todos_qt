import datetime

from src.domain.memorial_day import calculate_memorial_day


def test_memorial_day() -> None:
    memorial_day = calculate_memorial_day(year=2022)
    assert memorial_day == datetime.date(2022, 5, 30)

    memorial_day = calculate_memorial_day(year=2030)
    assert memorial_day == datetime.date(2030, 5, 27)

    return None
