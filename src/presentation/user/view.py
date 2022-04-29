from __future__ import annotations

from PyQt5 import QtWidgets as qtw

from src.presentation.user.dash.view import UserDash
from src.presentation.user.form.view import UserForm
from src.presentation.user.state import UserState

__all__ = ("UserView",)


class UserView(qtw.QWidget):
    def __init__(self, *, parent: qtw.QWidget | None = None):
        super().__init__(parent=parent)

        self.dash = UserDash()
        self.form = UserForm()

        self.stacked_layout = qtw.QStackedLayout()
        self.stacked_layout.addWidget(self.dash)
        self.stacked_layout.addWidget(self.form)

        self.setLayout(self.stacked_layout)

    def get_state(self) -> UserState:
        return UserState(
            dash_state=self.dash.get_state(),
            form_state=self.form.get_state(),
            dash_active=self.stacked_layout.currentIndex() == 0,
        )

    def set_state(self, *, state: UserState) -> None:
        self.dash.set_state(state=state.dash_state)
        self.form.set_state(state=state.form_state)
        if state.dash_active:
            self.stacked_layout.setCurrentIndex(0)
        else:
            self.stacked_layout.setCurrentIndex(1)
