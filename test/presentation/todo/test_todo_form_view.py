import datetime
import string

import hypothesis
from hypothesis import strategies

from src import domain
from src.presentation.category_selector import CategorySelectorWidget
from src.presentation.todo.view.form.requests import TodoFormRequests
from src.presentation.todo.view.form.state import TodoFormState
from src.presentation.todo.view.form.view import TodoFormView
from src.presentation.user_selector import UserSelectorWidget
from test import fake


@hypothesis.settings(deadline=None)
@hypothesis.given(
    todo=strategies.builds(
        domain.Todo.daily,
        start_date=strategies.dates(min_value=datetime.date(2000, 1, 1)),
        note=strategies.text(alphabet=string.ascii_letters + string.digits),
    )
)
def test_daily_todo_form_state_round_trips(todo: domain.Todo) -> None:
    todo_form = _generate_todo_form(todo=todo)
    actual = todo_form.get_state()
    expected = TodoFormState().from_domain(todo=todo)
    assert actual == expected


@hypothesis.settings(deadline=None)
@hypothesis.given(
    todo=strategies.builds(
        domain.Todo.irregular,
        start_date=strategies.dates(min_value=datetime.date(2000, 1, 1)),
        advance_display_days=strategies.integers(min_value=0, max_value=363),  # enforced by ui
        expire_display_days=strategies.integers(min_value=1, max_value=363),  # enforced by ui
        week_number=strategies.integers(min_value=1, max_value=5),  # enforced by ui
        note=strategies.text(alphabet=string.ascii_letters + string.digits),
    )
)
def test_irregular_todo_form_state_round_trips(todo: domain.Todo) -> None:
    todo_form = _generate_todo_form(todo=todo)

    assert todo_form._advance_days_sb.minimum() == 0
    assert todo_form._advance_days_sb.maximum() == 363
    assert todo_form._expire_days_sb.minimum() == 1
    assert todo_form._expire_days_sb.maximum() == 363
    assert todo_form._irregular_frequency_form._week_number_sb.minimum() == 1
    assert todo_form._irregular_frequency_form._week_number_sb.maximum() == 5

    actual = todo_form.get_state()
    expected = TodoFormState().from_domain(todo=todo)

    assert actual == expected


@hypothesis.settings(deadline=None)
@hypothesis.given(
    todo=strategies.builds(
        domain.Todo.monthly,
        advance_display_days=strategies.integers(min_value=0, max_value=27),  # enforced by ui
        expire_display_days=strategies.integers(min_value=1, max_value=27),  # enforced by ui
        month_day=strategies.integers(min_value=1, max_value=28),  # enforced by ui
        start_date=strategies.dates(min_value=datetime.date(2000, 1, 1)),  # enforced by ui
        note=strategies.text(alphabet=string.ascii_letters + string.digits),
    )
)
def test_monthly_todo_form_state_round_trips(todo: domain.Todo) -> None:
    todo_form = _generate_todo_form(todo=todo)

    assert todo_form._advance_days_sb.minimum() == 0
    assert todo_form._advance_days_sb.maximum() == 27
    assert todo_form._expire_days_sb.minimum() == 1
    assert todo_form._expire_days_sb.maximum() == 27
    assert todo_form._monthly_frequency_form._month_day_sb.minimum() == 1
    assert todo_form._monthly_frequency_form._month_day_sb.maximum() == 28

    actual = todo_form.get_state()
    expected = TodoFormState().from_domain(todo=todo)

    assert actual == expected


@hypothesis.settings(deadline=None)
@hypothesis.given(
    todo=strategies.builds(
        domain.Todo.once,
        advance_display_days=strategies.integers(min_value=0, max_value=9999),  # enforced by ui
        expire_display_days=strategies.integers(min_value=1, max_value=9999),  # enforced by ui
        due_date=strategies.dates(min_value=datetime.date(2000, 1, 1)),  # enforced by ui
        start_date=strategies.dates(min_value=datetime.date(2000, 1, 1)),  # enforced by ui
        note=strategies.text(alphabet=string.ascii_letters + string.digits),
    )
)
def test_once_todo_form_state_round_trips(todo: domain.Todo) -> None:
    todo_form = _generate_todo_form(todo=todo)

    assert todo_form._advance_days_sb.minimum() == 0
    assert todo_form._advance_days_sb.maximum() == 9999
    assert todo_form._expire_days_sb.minimum() == 1
    assert todo_form._expire_days_sb.maximum() == 9999

    actual = todo_form.get_state()
    expected = TodoFormState().from_domain(todo=todo)

    assert actual == expected


@hypothesis.settings(deadline=None)
@hypothesis.given(
    todo=strategies.builds(
        domain.Todo.weekly,
        advance_display_days=strategies.integers(min_value=0, max_value=6),  # enforced by ui
        expire_display_days=strategies.integers(min_value=1, max_value=6),  # enforced by ui
        start_date=strategies.dates(min_value=datetime.date(2000, 1, 1)),  # enforced by ui
        note=strategies.text(alphabet=string.ascii_letters + string.digits),
    )
)
def test_weekly_todo_form_state_round_trips(todo: domain.Todo) -> None:
    todo_form = _generate_todo_form(todo=todo)

    assert todo_form._advance_days_sb.minimum() == 0
    assert todo_form._advance_days_sb.maximum() == 6
    assert todo_form._expire_days_sb.minimum() == 1
    assert todo_form._expire_days_sb.maximum() == 6

    actual = todo_form.get_state()
    expected = TodoFormState().from_domain(todo=todo)

    assert actual == expected


@hypothesis.settings(deadline=None)
@hypothesis.given(
    todo=strategies.builds(
        domain.Todo.xdays,
        advance_display_days=strategies.integers(min_value=0, max_value=9999),  # enforced by ui
        expire_display_days=strategies.integers(min_value=1, max_value=9999),  # enforced by ui
        start_date=strategies.dates(min_value=datetime.date(2000, 1, 1)),  # enforced by ui
        days=strategies.integers(min_value=1, max_value=9999),  # enforced by ui
        note=strategies.text(alphabet=string.ascii_letters + string.digits),
    )
)
def test_xdays_todo_form_state_round_trips(todo: domain.Todo) -> None:
    todo_form = _generate_todo_form(todo=todo)

    assert todo_form._advance_days_sb.minimum() == 0
    assert todo_form._advance_days_sb.maximum() == 9999
    assert todo_form._expire_days_sb.minimum() == 1
    assert todo_form._expire_days_sb.maximum() == 9999
    assert todo_form._xdays_frequency_form._days_sb.minimum() == 1
    assert todo_form._xdays_frequency_form._days_sb.maximum() == 9999

    actual = todo_form.get_state()
    expected = TodoFormState().from_domain(todo=todo)

    assert actual == expected


@hypothesis.settings(deadline=None)
@hypothesis.given(
    todo=strategies.builds(
        domain.Todo.yearly,
        advance_display_days=strategies.integers(min_value=0, max_value=363),  # enforced by ui
        expire_display_days=strategies.integers(min_value=1, max_value=363),  # enforced by ui
        start_date=strategies.dates(min_value=datetime.date(2000, 1, 1)),  # enforced by ui
        month_day=strategies.integers(min_value=1, max_value=28),  # enforced by ui
        note=strategies.text(alphabet=string.ascii_letters + string.digits),
    )
)
def test_yearly_todo_form_state_round_trips(todo: domain.Todo) -> None:
    todo_form = _generate_todo_form(todo=todo)

    assert todo_form._advance_days_sb.minimum() == 0
    assert todo_form._advance_days_sb.maximum() == 363
    assert todo_form._expire_days_sb.minimum() == 1
    assert todo_form._expire_days_sb.maximum() == 363
    assert todo_form._yearly_frequency_form._month_day_sb.minimum() == 1
    assert todo_form._yearly_frequency_form._month_day_sb.maximum() == 28

    actual = todo_form.get_state()
    expected = TodoFormState().from_domain(todo=todo)

    assert actual == expected


def _generate_todo_form(
    *,
    todo: domain.Todo,
    user_service: domain.UserService = fake.UserService(),
    category_service: domain.CategoryService = fake.CategoryService(),
) -> TodoFormView:
    form_requests = TodoFormRequests(parent=None)

    category_selector = CategorySelectorWidget(
        category_service=category_service,
        include_all_category=False,
        parent=None,
    )

    user_selector = UserSelectorWidget(
        user_service=user_service,
        include_all_user=False,
        parent=None,
    )

    todo_form = TodoFormView(
        form_requests=form_requests,
        category_selector=category_selector,
        user_selector=user_selector,
        parent=None,
    )

    todo_form.set_state(
        TodoFormState(
            categories=(todo.category,),
            users=(todo.user,),
        ),
    )
    new_state = TodoFormState.from_domain(todo=todo)
    todo_form.set_state(state=new_state)

    return todo_form
