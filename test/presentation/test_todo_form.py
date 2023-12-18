import datetime

# noinspection PyPep8Naming
from PyQt5 import QtCore as qtc
from hypothesis import given, strategies as st
from hypothesis.strategies import dates, integers

from src.presentation.category_selector import CategorySelectorWidget
from src.presentation.todo.view.form.requests import TodoFormRequests
from src.presentation.todo.view.form.state import TodoFormState

from src import domain, service
from src.presentation.todo.view.form.view import TodoForm
from src.presentation.user_selector import UserSelectorWidget
import sqlalchemy as sa


@given(
    todo=st.builds(
        domain.Todo.daily,
        start_date=dates(min_value=datetime.date(1900, 1, 1)),  # enforced by ui
    )
)
def test_daily_todo_form_round_trip(todo: domain.Todo, engine: sa.Engine):
    todo_form = _create_todo_form(engine=engine)

    assert todo_form._start_date_edit.minimumDate() == qtc.QDate(1900, 1, 1)

    new_state = TodoFormState.from_domain(todo=todo)
    todo_form.set_state(state=new_state)
    assert todo_form.get_state() == new_state


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
    initial_state = TodoFormState.initial(
        category_options=[domain.TODO_CATEGORY, todo.category],
        user_options=[],
    )
    todo_form = TodoForm()
    assert todo_form._advance_days_sb.maximum() == 364
    assert todo_form._expire_days_sb.maximum() == 364
    assert todo_form._start_date_edit.minimumDate() == qtc.QDate(1900, 1, 1)
    assert todo_form._irregular_frequency_form._week_number_sb.minimum() == 1
    assert todo_form._irregular_frequency_form._week_number_sb.maximum() == 5
    assert todo_form.get_state() == initial_state

    new_state = TodoFormState.from_domain(todo=todo)
    todo_form.set_state(state=new_state)
    assert todo_form.get_state() == new_state


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
    initial_state = TodoFormState.initial(
        category_options=[domain.TODO_CATEGORY, todo.category],
        user_options=[],
    )
    todo_form = TodoForm()
    assert todo_form._advance_days_sb.maximum() == 364
    assert todo_form._expire_days_sb.maximum() == 364
    assert todo_form._start_date_edit.minimumDate() == qtc.QDate(1900, 1, 1)
    assert todo_form._monthly_frequency_form._month_day_sb.minimum() == 1
    assert todo_form._monthly_frequency_form._month_day_sb.maximum() == 28
    assert todo_form.get_state() == initial_state

    new_state = TodoFormState.from_domain(
        todo=todo,
        category_options=[domain.TODO_CATEGORY, todo.category],
        user_options=[],
    )
    todo_form.set_state(state=new_state)
    assert todo_form.get_state() == new_state


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
    initial_state = TodoFormState.initial(
        category_options=[domain.TODO_CATEGORY, todo.category],
        user_options=[],
    )
    todo_form = TodoForm()
    assert todo_form._advance_days_sb.maximum() == 364
    assert todo_form._expire_days_sb.maximum() == 364
    assert todo_form._start_date_edit.minimumDate() == qtc.QDate(1900, 1, 1)
    assert todo_form._one_off_frequency_form._due_date_edit.minimumDate() == qtc.QDate(1900, 1, 1)
    assert todo_form.get_state() == initial_state

    new_state = TodoFormState.from_domain(
        todo=todo,
        category_options=[domain.TODO_CATEGORY, todo.category],
        user_options=[],
    )
    todo_form.set_state(state=new_state)
    assert todo_form.get_state() == new_state


@given(
    todo=st.builds(
        domain.Todo.weekly,
        advance_display_days=integers(min_value=0, max_value=364),  # enforced by ui
        expire_display_days=integers(min_value=1, max_value=364),  # enforced by ui
        start_date=dates(min_value=datetime.date(1900, 1, 1)),  # enforced by ui
    )
)
def test_weekly_todo_form_round_trip(todo: domain.Todo):
    initial_state = TodoFormState.initial(
        category_options=[domain.TODO_CATEGORY, todo.category],
        user_options=[],
    )
    todo_form = TodoForm()
    assert todo_form._advance_days_sb.maximum() == 364
    assert todo_form._expire_days_sb.maximum() == 364
    assert todo_form._start_date_edit.minimumDate() == qtc.QDate(1900, 1, 1)
    assert todo_form.get_state() == initial_state

    new_state = TodoFormState.from_domain(
        todo=todo,
        category_options=[domain.TODO_CATEGORY, todo.category],
        user_options=[],
    )
    todo_form.set_state(state=new_state)
    assert todo_form.get_state() == new_state


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
    initial_state = TodoFormState.initial(
        category_options=[domain.TODO_CATEGORY, todo.category],
        user_options=[],
    )
    todo_form = TodoForm()
    assert todo_form._advance_days_sb.maximum() == 364
    assert todo_form._expire_days_sb.maximum() == 364
    assert todo_form._start_date_edit.minimumDate() == qtc.QDate(1900, 1, 1)
    assert todo_form._xdays_frequency_form._days_sb.minimum() == 1
    assert todo_form._xdays_frequency_form._days_sb.maximum() == 364
    assert todo_form.get_state() == initial_state

    new_state = TodoFormState.from_domain(
        todo=todo,
        category_options=[domain.TODO_CATEGORY, todo.category],
        user_options=[],
    )
    todo_form.set_state(state=new_state)
    assert todo_form.get_state() == new_state


# noinspection DuplicatedCode
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
    initial_state = TodoFormState.initial(
        category_options=[domain.TODO_CATEGORY, todo.category],
        user_options=[],
    )

    todo_form = TodoForm(
        form_requests=form_requests,
        category_selector=category_selector,
        user_selector=user_selector,
        parent=None,
    )
    assert todo_form._advance_days_sb.maximum() == 364
    assert todo_form._expire_days_sb.maximum() == 364
    assert todo_form._start_date_edit.minimumDate() == qtc.QDate(1900, 1, 1)
    assert todo_form._yearly_frequency_form._month_day_sb.minimum() == 1
    assert todo_form._yearly_frequency_form._month_day_sb.maximum() == 28
    assert todo_form.get_state() == initial_state

    new_state = TodoFormState.from_domain(
        todo=todo,
        category_options=[domain.TODO_CATEGORY, todo.category],
        user_options=[],
    )
    todo_form.set_state(state=new_state)
    assert todo_form.get_state() == new_state


def _create_todo_form(*, engine: sa.Engine) -> TodoForm:
    form_requests = TodoFormRequests(parent=None)

    category_service = service.CategoryService(engine=engine)

    user_service = service.UserService(engine=engine, username="test")

    category_selector = CategorySelectorWidget(
        category_service=category_service,
        include_all_category=True,
        parent=None,
    )

    user_selector = UserSelectorWidget(
        user_service=user_service,
        include_all_user=True,
        parent=None,
    )

    return TodoForm(
        form_requests=form_requests,
        category_selector=category_selector,
        user_selector=user_selector,
    )
