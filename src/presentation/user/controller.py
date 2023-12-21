import typing

# noinspection PyPep8Naming
from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa: F401
from loguru import logger

from src import domain
from src.presentation.user import dash, form
from src.presentation.user.form.state import UserFormState
from src.presentation.user.state import UserState

__all__ = ("UserController",)


class UserController(qtc.QObject):
    users_updated = qtc.pyqtSignal()
    states = qtc.pyqtSignal(UserState)

    def __init__(
        self,
        *,
        dash_requests: dash.requests.UserDashRequests,
        form_requests: form.requests.UserFormRequests,
        current_user: domain.User,
        user_service: domain.UserService,
        parent: qtc.QObject | None,
    ):
        super().__init__(parent=parent)

        self._dash_requests: typing.Final[dash.requests.UserDashRequests] = dash_requests
        self._form_requests: typing.Final[form.requests.UserFormRequests] = form_requests
        self._current_user: typing.Final[domain.User] = current_user
        self._user_service: typing.Final[domain.UserService] = user_service

        self._dash_requests.add.connect(self._on_dash_add_btn_clicked)
        self._dash_requests.delete.connect(self._on_dash_delete_btn_clicked)
        self._dash_requests.edit.connect(self._on_dash_edit_btn_clicked)
        self._dash_requests.refresh.connect(self.refresh)
        self._form_requests.back.connect(self._on_form_back_btn_clicked)
        self._form_requests.save.connect(self._on_form_save_btn_clicked)

    def refresh(self) -> None:
        logger.debug(f"{self.__class__.__name__}.refresh()")

        try:
            self._set_status("Refreshing Users...")

            users = self._user_service.where(active=True)
            if isinstance(users, domain.Error):
                self._set_status(str(users))
                return None

            self.states.emit(
                UserState(
                    dash_state=dash.UserDashState(
                        users=users,
                        status="Users refreshed.",
                    ),
                )
            )
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.refresh() failed: {e!s}")

            self._set_status(str(e))

    def _on_dash_add_btn_clicked(self) -> None:
        logger.debug(f"{self.__class__.__name__}._on_dash_add_btn_clicked()")

        try:
            self.states.emit(
                UserState(
                    form_state=form.UserFormState.initial(),
                    dash_active=False,
                )
            )
        except Exception as e:
            logger.error(f"{self.__class__.__name__}._on_dash_add_btn_clicked() failed: {e!s}")

            self._set_status(str(e))

    def _on_dash_delete_btn_clicked(self, /, request: dash.requests.DeleteRequest) -> None:
        logger.debug(f"{self.__class__.__name__}._on_dash_delete_btn_clicked()")

        try:
            delete_result = self._user_service.delete(user_id=request.user.user_id)
            if isinstance(delete_result, domain.Error):
                self._set_status(str(delete_result))

            self.users_updated.emit()
        except Exception as e:
            logger.error(f"{self.__class__.__name__}._on_dash_delete_btn_clicked() failed: {e!s}")

            self._set_status(str(e))

    def _on_dash_edit_btn_clicked(self, /, event: dash.requests.EditRequest) -> None:
        logger.debug(f"{self.__class__.__name__}._on_dash_edit_btn_clicked({event=!r})")

        try:
            self.states.emit(
                UserState(
                    form_state=UserFormState.from_domain(user=event.user),
                    dash_active=False,
                )
            )
        except Exception as e:
            logger.error(f"{self.__class__.__name__}._on_dash_edit_btn_clicked({event=!r}) failed: {e!s}")

            self._set_status(str(e))

    def _on_form_back_btn_clicked(self) -> None:
        logger.debug(f"{self.__class__.__name__}._on_form_back_btn_clicked()")

        try:
            self.states.emit(UserState(dash_active=True))
        except Exception as e:
            logger.error(f"{self.__class__.__name__}._on_form_back_btn_clicked() failed: {e!s}")

            self._set_status(str(e))

    def _on_form_save_btn_clicked(self, /, request: form.requests.SaveRequest) -> None:
        try:
            db_user = self._user_service.get(user_id=request.user.user_id)
            if isinstance(db_user, domain.Error):
                self._set_status(str(db_user))
                return None

            if db_user is None:
                add_result = self._user_service.add(user=request.user)
                if isinstance(add_result, domain.Error):
                    self._set_status(str(add_result))
                    return None

                self.users_updated.emit()

                self.states.emit(
                    UserState(
                        dash_active=True,
                        form_state=UserFormState.initial(),
                        dash_state=dash.UserDashState(
                            user_added=request.user,
                            selected_user=request.user,
                            status=f"{request.user.display_name} added.",
                        ),
                    )
                )
            else:
                update_result = self._user_service.update(user=request.user)
                if isinstance(update_result, domain.Error):
                    self._set_status(str(update_result))
                    return None

                self.users_updated.emit()

                self.states.emit(
                    UserState(
                        dash_active=True,
                        form_state=UserFormState.initial(),
                        dash_state=dash.UserDashState(
                            user_updated=request.user,
                            selected_user=request.user,
                            status=f"{request.user.display_name} updated.",
                        ),
                    )
                )
        except Exception as e:
            logger.error(f"{self.__class__.__name__}._on_form_save_btn_clicked({request=!r}) failed: {e!s}")

            self._set_status(str(e))

    def _set_status(self, /, status: str) -> None:
        self.states.emit(UserState(dash_state=dash.UserDashState(status=status)))
