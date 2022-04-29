from __future__ import annotations

from PyQt5 import QtWidgets as qtw

from src.presentation.category.dash.view import CategoryDash
from src.presentation.category.form.view import CategoryForm
from src.presentation.category.state import CategoryState

__all__ = ("CategoryView",)


class CategoryView(qtw.QWidget):
    def __init__(self, *, parent: qtw.QWidget | None = None):
        super().__init__(parent=parent)

        self.dash = CategoryDash()
        self.form = CategoryForm()

        self.stacked_layout = qtw.QStackedLayout()
        self.stacked_layout.addWidget(self.dash)
        self.stacked_layout.addWidget(self.form)

        self.setLayout(self.stacked_layout)

    def get_state(self) -> CategoryState:
        return CategoryState(
            dash_state=self.dash.get_state(),
            form_state=self.form.get_state(),
            dash_active=self.stacked_layout.currentIndex() == 0,
        )

    def set_state(self, *, state: CategoryState) -> None:
        self.dash.set_state(state=state.dash_state)
        self.form.set_state(state=state.form_state)
        if state.dash_active:
            self.stacked_layout.setCurrentIndex(0)
        else:
            self.stacked_layout.setCurrentIndex(1)
