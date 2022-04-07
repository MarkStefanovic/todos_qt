import dataclasses
import datetime
import logging

from src import domain
from src.presentation.category.form.state import CategoryFormState
from src.presentation.category.view import CategoryView
from src.presentation.shared.widgets import popup

__all__ = ("CategoryController",)

logger = logging.getLogger()


class CategoryController:
    def __init__(
        self,
        *,
        category_service: domain.CategoryService,
        view: CategoryView,
    ):
        self._category_service = category_service
        self._view = view

        self._view.dash.add_btn.clicked.connect(self._on_dash_add_btn_clicked)
        self._view.dash.refresh_btn.clicked.connect(self._on_dash_refresh_btn_clicked)
        self._view.dash.delete_btn_clicked.connect(self._on_dash_delete_btn_clicked)
        self._view.dash.edit_btn_clicked.connect(self._on_dash_edit_btn_clicked)

        self._view.form.back_btn.clicked.connect(self._on_form_back_btn_clicked)
        self._view.form.save_btn.clicked.connect(self._on_form_save_btn_clicked)

    def _on_dash_add_btn_clicked(self) -> None:
        state = self._view.get_state()

        new_state = dataclasses.replace(
            state,
            form_state=CategoryFormState.initial(),
            dash_active=False,
        )

        self._view.set_state(state=new_state)

    def _on_dash_delete_btn_clicked(self) -> None:
        state = self._view.get_state()

        try:
            if category := state.dash_state.selected_category:
                if popup.confirm(question=f"Are you sure you want to delete {category.name}?"):
                    self._category_service.delete(category_id=category.category_id)

                    categories = self._category_service.all()

                    new_state = dataclasses.replace(
                        state,
                        dash_state=dataclasses.replace(
                            state.dash_state,
                            categories=categories,
                            status=_add_timestamp(message=f"Deleted {category.name}."),
                        )
                    )

                    self._view.set_state(state=new_state)
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

    def _on_dash_edit_btn_clicked(self) -> None:
        state = self._view.get_state()

        if category := state.dash_state.selected_category:
            new_state = dataclasses.replace(
                state,
                form_state=CategoryFormState.from_domain(category=category),
                dash_active=False,
            )

            self._view.set_state(state=new_state)

    def _on_dash_refresh_btn_clicked(self) -> None:
        state = self._view.get_state()

        try:
            categories = self._category_service.all()

            new_state = dataclasses.replace(
                state,
                dash_state=dataclasses.replace(
                    state.dash_state,
                    categories=categories,
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
            category = state.form_state.to_domain()

            if self._category_service.get(category_id=category.category_id):
                self._category_service.update(category=category)
                status = f"{category.name} updated."
            else:
                self._category_service.add(category=category)
                status = f"{category.name} added."

            categories = self._category_service.all()

            new_state = dataclasses.replace(
                state,
                dash_state=dataclasses.replace(
                    state.dash_state,
                    categories=categories,
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
                dash_active=True,
            )

        self._view.set_state(state=new_state)


def _add_timestamp(*, message: str) -> str:
    ts_str = datetime.datetime.now().strftime("%m/%d @ %I:%M %p")
    return f"{ts_str}: {message}"
