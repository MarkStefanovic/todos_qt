import dataclasses
import datetime
import typing

from loguru import logger

# noinspection PyPep8Naming
from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa: F401

from src import domain
from src.presentation.shared.widgets import popup
from src.presentation.user import dash, form
from src.presentation.user.form.state import UserFormState
from src.presentation.user.state import UserState

__all__ = ("UserController",)


class UserController(qtc.QObject):
    states = qtc.pyqtSignal(UserState)

    def __init__(
        self,
        *,
        dash_requests: dash.requests.UserDashRequests,
        form_requests: form.requests.UserFormRequests,
        user_service: domain.UserService,
        parent: qtc.QObject | None,
    ):
        super().__init__(parent=parent)

        self._dash_requests: typing.Final[dash.requests.UserDashRequests] = dash_requests
        self._form_requests: typing.Final[form.requests.UserFormRequests] = form_requests
        self._user_service: typing.Final[domain.UserService] = user_service

        self._dash_requests.add.connect(self._on_dash_add_btn_clicked)
        self._dash_requests.delete.connect(self._on_dash_delete_btn_clicked)
        self._dash_requests.edit.connect(self._on_dash_edit_btn_clicked)
        self._dash_requests.refresh.clicked.connect(self.refresh)
        self._form_requests.back.connect(self._on_form_back_btn_clicked)
        self._form_requests.save.connect(self._on_form_save_btn_clicked)

    def refresh(self) -> None:
        try:
            users = self._user_service.where()

            current_user = self._user_service.get_current_user()

            new_state = dataclasses.replace(
                state,
                dash_state=dataclasses.replace(
                    state.dash_state,
                    users=users,
                    current_user=current_user,
                    status=_add_timestamp(message="Refreshed."),
                ),
            )
        except Exception as e:
            logger.exception(e)
            new_state = dataclasses.replace(
                state,
                dash_state=dataclasses.replace(
                    state.dash_state,
                    status=_add_timestamp(message=str(e)),
                ),
            )

        self._view.set_state(state=new_state)

    def _on_dash_add_btn_clicked(self) -> None:
        state = self._view.get_state()

        new_state = dataclasses.replace(
            state,
            form_state=UserFormState.initial(),
            dash_active=False,
        )

        self._view.set_state(state=new_state)

    def _on_dash_delete_btn_clicked(self) -> None:
        state = self._view.get_state()

        try:
            if user := state.dash_state.selected_user:
                if popup.confirm(
                    question=f"Are you sure you want to delete {user.display_name}?",
                    title="Confirm Delete",
                ):
                    self._user_service.delete(user_id=user.user_id)

                    users = self._user_service.where()

                    new_state = dataclasses.replace(
                        state,
                        dash_state=dataclasses.replace(
                            state.dash_state,
                            users=users,
                            status=_add_timestamp(message=f"Deleted {user.display_name}."),
                        ),
                    )
                else:
                    new_state = dataclasses.replace(
                        state,
                        dash_state=dataclasses.replace(
                            state.dash_state,
                            status=_add_timestamp(message="Delete cancelled."),
                        ),
                    )
            else:
                new_state = dataclasses.replace(
                    state,
                    dash_state=dataclasses.replace(
                        state.dash_state,
                        status=_add_timestamp(message="No user was selected."),
                    ),
                )
        except Exception as e:
            logger.exception(e)
            new_state = dataclasses.replace(
                state,
                dash_state=dataclasses.replace(
                    state.dash_state,
                    status=_add_timestamp(message=str(e)),
                ),
            )

        self._view.set_state(state=new_state)

    def _on_dash_edit_btn_clicked(self) -> None:
        state = self._view.get_state()

        if user := state.dash_state.selected_user:
            new_state = dataclasses.replace(
                state,
                form_state=UserFormState.from_domain(user=user),
                dash_active=False,
            )
        else:
            new_state = dataclasses.replace(
                state,
                dash_state=dataclasses.replace(
                    state.dash_state,
                    status=_add_timestamp(message="Please select a user first."),
                ),
            )

        self._view.set_state(state=new_state)

    def _on_form_back_btn_clicked(self) -> None:
        state = self._view.get_state()

        new_state = dataclasses.replace(state, dash_active=True)

        self._view.set_state(state=new_state)

    def _on_form_save_btn_clicked(self) -> None:
        state = self._view.get_state()

        try:
            if user := self._user_service.get(user_id=state.form_state.user_id):
                self._user_service.update(user=user)
                status = f"{user.display_name} updated."
            else:
                new_user = state.form_state.to_domain()
                self._user_service.add(user=new_user)
                status = f"{new_user.display_name} added."

            users = self._user_service.where()

            current_user = self._user_service.get_current_user()

            new_state = dataclasses.replace(
                state,
                dash_state=dataclasses.replace(
                    state.dash_state,
                    users=users,
                    current_user=current_user,
                    status=_add_timestamp(message=status),
                ),
                dash_active=True,
            )
        except Exception as e:
            logger.exception(e)
            new_state = dataclasses.replace(
                state,
                dash_state=dataclasses.replace(
                    state.dash_state,
                    status=_add_timestamp(message=str(e)),
                ),
            )

        self._view.set_state(state=new_state)


def _add_timestamp(*, message: str) -> str:
    ts_str = datetime.datetime.now().strftime("%m/%d @ %I:%M %p")
    return f"{ts_str}: {message}"
