import datetime


# noinspection PyPep8Naming
from hypothesis import given, strategies as st
from hypothesis.strategies import dates, integers

from src import domain
from src.presentation.category_selector import CategorySelectorWidget
from src.presentation.todo.view.form.requests import TodoFormRequests
from src.presentation.todo.view.form.state import TodoFormState
from src.presentation.todo.view.form.view import TodoFormView
from src.presentation.user_selector import UserSelectorWidget
from test import fake


@given(
    todo=st.builds(
        domain.Todo.daily,
        start_date=dates(min_value=datetime.date(1900, 1, 1)),  # enforced by ui
    )
)
def test_daily_todo_form_round_trip(todo: domain.Todo) -> None:
    todo_form = _generate_todo_form()

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
def test_irregular_todo_form_round_trip(todo: domain.Todo) -> None:
    form_requests = TodoFormRequests(parent=None)

    category_service = fake.CategoryService()
    user_service = fake.UserService()

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
    assert todo_form._advance_days_sb.maximum() == 364
    assert todo_form._expire_days_sb.maximum() == 364
    assert todo_form._irregular_frequency_form._week_number_sb.minimum() == 1
    assert todo_form._irregular_frequency_form._week_number_sb.maximum() == 5

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
def test_monthly_todo_form_round_trip(todo: domain.Todo) -> None:
    todo_form = _generate_todo_form()
    assert todo_form._advance_days_sb.maximum() == 364
    assert todo_form._expire_days_sb.maximum() == 364
    assert todo_form._monthly_frequency_form._month_day_sb.minimum() == 1
    assert todo_form._monthly_frequency_form._month_day_sb.maximum() == 28

    new_state = TodoFormState.from_domain(todo=todo)
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
def test_once_todo_form_round_trip(todo: domain.Todo) -> None:
    todo_form = _generate_todo_form()
    assert todo_form._advance_days_sb.maximum() == 364
    assert todo_form._expire_days_sb.maximum() == 364

    new_state = TodoFormState.from_domain(todo=todo)
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
def test_weekly_todo_form_round_trip(todo: domain.Todo) -> None:
    todo_form = _generate_todo_form()
    assert todo_form._advance_days_sb.maximum() == 364
    assert todo_form._expire_days_sb.maximum() == 364

    new_state = TodoFormState.from_domain(todo=todo)
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
def test_xdays_todo_form_round_trip(todo: domain.Todo) -> None:
    todo_form = _generate_todo_form()
    assert todo_form._advance_days_sb.maximum() == 364
    assert todo_form._expire_days_sb.maximum() == 364
    assert todo_form._xdays_frequency_form._days_sb.minimum() == 1
    assert todo_form._xdays_frequency_form._days_sb.maximum() == 364

    new_state = TodoFormState.from_domain(todo=todo)
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
def test_yearly_todo_form_round_trip(todo: domain.Todo) -> None:
    todo_form = _generate_todo_form()
    assert todo_form._advance_days_sb.maximum() == 364
    assert todo_form._expire_days_sb.maximum() == 364
    assert todo_form._yearly_frequency_form._month_day_sb.minimum() == 1
    assert todo_form._yearly_frequency_form._month_day_sb.maximum() == 28

    new_state = TodoFormState.from_domain(todo=todo)
    todo_form.set_state(state=new_state)
    assert todo_form.get_state() == new_state


# def _create_todo_form(*, engine: sa.Engine) -> TodoFormView:
#     form_requests = TodoFormRequests(parent=None)
#
#     category_service = service.CategoryService(engine=engine)
#
#     user_service = service.UserService(engine=engine, username="test")
#
#     category_selector = CategorySelectorWidget(
#         category_service=category_service,
#         include_all_category=True,
#         parent=None,
#     )
#
#     user_selector = UserSelectorWidget(
#         user_service=user_service,
#         include_all_user=True,
#         parent=None,
#     )
#
#     return TodoFormView(
#         form_requests=form_requests,
#         category_selector=category_selector,
#         user_selector=user_selector,
#     )


def _generate_todo_form() -> TodoFormView:
    form_requests = TodoFormRequests(parent=None)

    user_service = fake.UserService()
    category_service = fake.CategoryService()

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

    return TodoFormView(
        form_requests=form_requests,
        category_selector=category_selector,
        user_selector=user_selector,
        parent=None,
    )
