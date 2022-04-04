from __future__ import annotations

import dataclasses

from src.presentation.category.dash.state import CategoryDashState
from src.presentation.category.form.state import CategoryFormState

__all__ = ("CategoryState",)


@dataclasses.dataclass(frozen=True)
class CategoryState:
    dash_state: CategoryDashState
    form_state: CategoryFormState
    dash_active: bool

    @staticmethod
    def initial() -> CategoryState:
        return CategoryState(
            dash_state=CategoryDashState.initial(),
            form_state=CategoryFormState.initial(),
            dash_active=True,
        )
