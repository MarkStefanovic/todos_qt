import datetime

import hypothesis
from hypothesis import strategies

from src.presentation.shared.widgets.date_picker import DatePicker


@hypothesis.settings(deadline=None)
@hypothesis.given(value=strategies.dates(min_value=datetime.date(1900, 1, 1)))
def test_irregular_todo_form_state_round_trips(value: datetime.date) -> None:
    date_picker = DatePicker(parent=None)
    date_picker.set_value(value)
    assert date_picker.get_value() == value
