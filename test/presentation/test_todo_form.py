from hypothesis import assume, given, HealthCheck, settings, strategies as st

from src import domain
from src.presentation.todo.form.state import TodoFormState
from src.presentation.todo.form.view import TodoForm


@given(todo=st.builds(domain.Todo.daily))
def test_daily_todo_form_round_trip(todo: domain.Todo):
    assume(todo.frequency.start_date.year > 1752)

    initial_state = TodoFormState.from_domain(todo=todo)
    todo_form = TodoForm(state=initial_state)
    assert todo_form.get_state() == initial_state


@settings(suppress_health_check=[HealthCheck.filter_too_much])
@given(todo=st.builds(domain.Todo.easter))
def test_easter_todo_form_round_trip(todo: domain.Todo):
    print(f"{todo.frequency.advance_display_days=}, {todo.frequency.expire_display_days=}")
    assume(0 <= todo.frequency.advance_display_days <= 364)  # enforced by spinbox
    assume(0 <= todo.frequency.expire_display_days <= 364)  # enforced by spinbox

    initial_state = TodoFormState.from_domain(todo=todo)
    todo_form = TodoForm(state=initial_state)
    assert todo_form.get_state() == initial_state

