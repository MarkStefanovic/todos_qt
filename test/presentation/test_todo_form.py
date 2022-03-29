import datetime

from hypothesis import assume, given, strategies as st
from hypothesis.strategies import dates, integers

from src import domain
from src.presentation.todo.form.state import TodoFormState
from src.presentation.todo.form.view import TodoForm


@given(
    todo=st.builds(
        domain.Todo.daily,
        start_date=dates(min_value=datetime.date(1900, 1, 1)),  # enforced by ui
    )
)
def test_daily_todo_form_round_trip(todo: domain.Todo):
    assume(todo.frequency.start_date.year > 1752)

    initial_state = TodoFormState.from_domain(todo=todo)
    todo_form = TodoForm(state=initial_state)
    assert todo_form.get_state() == initial_state


# @settings(suppress_health_check=[HealthCheck.filter_too_much, HealthCheck.too_slow])
@given(
    todo=st.builds(
        domain.Todo.irregular,
        advance_display_days=integers(min_value=0, max_value=364),  # enforced by ui
        expire_display_days=integers(min_value=1, max_value=364),  # enforced by ui
        start_date=dates(min_value=datetime.date(1900, 1, 1)),  # enforced by ui
        week_number=integers(min_value=1, max_value=5),  # enforced by ui
    )
)
def test_irregular_todo_form_round_trip(todo: domain.Todo):
    initial_state = TodoFormState.from_domain(todo=todo)
    todo_form = TodoForm(state=initial_state)
    assert todo_form.get_state() == initial_state


@given(
    todo=st.builds(
        domain.Todo.monthly,
        advance_display_days=integers(min_value=0, max_value=364),  # enforced by ui
        expire_display_days=integers(min_value=1, max_value=364),  # enforced by ui
        start_date=dates(min_value=datetime.date(1900, 1, 1)),  # enforced by ui
        month_day=integers(min_value=1, max_value=28),  # enforced by ui
    )
)
def test_monthly_todo_form_round_trip(todo: domain.Todo):
    initial_state = TodoFormState.from_domain(todo=todo)
    todo_form = TodoForm(state=initial_state)
    assert todo_form.get_state() == initial_state


@given(
    todo=st.builds(
        domain.Todo.once,
        advance_display_days=integers(min_value=0, max_value=364),  # enforced by ui
        expire_display_days=integers(min_value=1, max_value=364),  # enforced by ui
        start_date=dates(min_value=datetime.date(1900, 1, 1)),  # enforced by ui
        due_date=dates(min_value=datetime.date(1900, 1, 1)),  # enforced by ui
    )
)
def test_once_todo_form_round_trip(todo: domain.Todo):
    initial_state = TodoFormState.from_domain(todo=todo)
    todo_form = TodoForm(state=initial_state)
    assert todo_form.get_state() == initial_state


@given(
    todo=st.builds(
        domain.Todo.weekly,
        advance_display_days=integers(min_value=0, max_value=364),  # enforced by ui
        expire_display_days=integers(min_value=1, max_value=364),  # enforced by ui
        start_date=dates(min_value=datetime.date(1900, 1, 1)),  # enforced by ui
    )
)
def test_weekly_todo_form_round_trip(todo: domain.Todo):
    initial_state = TodoFormState.from_domain(todo=todo)
    todo_form = TodoForm(state=initial_state)
    assert todo_form.get_state() == initial_state


@given(
    todo=st.builds(
        domain.Todo.xdays,
        advance_display_days=integers(min_value=0, max_value=364),  # enforced by ui
        expire_display_days=integers(min_value=1, max_value=364),  # enforced by ui
        start_date=dates(min_value=datetime.date(1900, 1, 1)),  # enforced by ui
        days=integers(min_value=1, max_value=364),  # enforced by ui
    )
)
def test_xdays_todo_form_round_trip(todo: domain.Todo):
    initial_state = TodoFormState.from_domain(todo=todo)
    todo_form = TodoForm(state=initial_state)
    assert todo_form.get_state() == initial_state


@given(
    todo=st.builds(
        domain.Todo.yearly,
        advance_display_days=integers(min_value=0, max_value=364),  # enforced by ui
        expire_display_days=integers(min_value=1, max_value=364),  # enforced by ui
        start_date=dates(min_value=datetime.date(1900, 1, 1)),  # enforced by ui
        month_day=integers(min_value=1, max_value=28),  # enforced by ui
    )
)
def test_yearly_todo_form_round_trip(todo: domain.Todo):
    initial_state = TodoFormState.from_domain(todo=todo)
    todo_form = TodoForm(state=initial_state)
    assert todo_form.get_state() == initial_state
