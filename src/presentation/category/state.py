from __future__ import annotations

import dataclasses

from src import domain
from src.presentation.category.dash.state import CategoryDashState
from src.presentation.category.form.state import CategoryFormState

__all__ = ("CategoryState",)


@dataclasses.dataclass(frozen=True)
class CategoryState:
    dash_state: CategoryDashState
    form_state: CategoryFormState
    dash_active: bool

    @staticmethod
    def initial(*, current_user: domain.User) -> CategoryState:
        return CategoryState(
            dash_state=CategoryDashState.initial(current_user=current_user),
            form_state=CategoryFormState.initial(),
            dash_active=True,
        )
