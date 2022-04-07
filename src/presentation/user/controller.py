import dataclasses
import datetime

from loguru import logger

from src import domain
from src.presentation.user.form.state import UserFormState
from src.presentation.user.view import UserView

__all__ = ("UserController",)


class UserController:
    def __init__(self, *, user_service: domain.UserService, view: UserView):
        self._user_service = user_service
        self._view = view

        self._view.dash.add_btn.clicked.connect(self._on_dash_add_btn_clicked)
        self._view.dash.refresh_btn.clicked.connect(self._on_dash_refresh_btn_clicked)
        self._view.form.back_btn.clicked.connect(self._on_form_back_btn_clicked)
        self._view.form.save_btn.clicked.connect(self._on_form_save_btn_clicked)

    def _on_dash_add_btn_clicked(self) -> None:
        state = self._view.get_state()

        new_state = dataclasses.replace(
            state,
            form_state=UserFormState.initial(),
            dash_active=False,
        )

        self._view.set_state(state=new_state)

    def _on_dash_refresh_btn_clicked(self) -> None:
        state = self._view.get_state()

        try:
            users = self._user_service.all()

            current_user = self._user_service.current_user()

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
                )
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

            users = self._user_service.all()

            current_user = self._user_service.current_user()

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
                )
            )

        self._view.set_state(state=new_state)


def _add_timestamp(*, message: str) -> str:
    ts_str = datetime.datetime.now().strftime("%m/%d @ %I:%M %p")
    return f"{ts_str}: {message}"
