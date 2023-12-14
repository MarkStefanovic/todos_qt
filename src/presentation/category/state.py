from __future__ import annotations

import dataclasses

from src import domain
from src.presentation.category.dash.state import CategoryDashState
from src.presentation.category.form.state import CategoryFormState

__all__ = ("CategoryState",)


@dataclasses.dataclass(frozen=True)
class CategoryState:
    dash_state: CategoryDashState | domain.Unspecified = domain.Unspecified()
    form_state: CategoryFormState | domain.Unspecified = domain.Unspecified()
    dash_active: bool | domain.Unspecified = domain.Unspecified()

    @staticmethod
    def set_status(status: str, /) -> CategoryState:
        return CategoryState(dash_state=CategoryDashState(status=status))
