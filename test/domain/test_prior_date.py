import datetime

from src import domain
from src.domain.prior_date import prior_date


def test_yearly_prior_date():
    christmas = domain.Frequency.yearly(
        month=domain.Month.December,
        month_day=25,
        advance_display_days=30,
        expire_display_days=30,
        start_date=datetime.date(1900, 1, 1),
    )
    prior_due_date = prior_date(frequency=christmas, today=datetime.date(2022, 3, 27))
    assert prior_due_date == datetime.date(2021, 12, 25)
