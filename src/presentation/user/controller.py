from src import domain
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

    def _on_dash_refresh_btn_clicked(self) -> None:

    def _on_form_back_btn_clicked(self) -> None:

    def _on_form_save_btn_clicked(self) -> None:
