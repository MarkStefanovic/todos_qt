import logging
import typing

# noinspection PyPep8Naming
from PyQt6 import QtCore as qtc

from src import domain
from src.presentation.category import dash, form
from src.presentation.category.state import CategoryState

__all__ = ("CategoryController",)

logger = logging.getLogger()


class CategoryController(qtc.QObject):
    categories_updated = qtc.pyqtSignal()
    states = qtc.pyqtSignal(CategoryState)

    def __init__(
        self,
        *,
        category_service: domain.CategoryService,
        dash_requests: dash.requests.CategoryDashRequests,
        form_requests: form.requests.CategoryFormRequests,
        parent: qtc.QObject | None,
    ):
        super().__init__(parent=parent)

        self._category_service: typing.Final[domain.CategoryService] = category_service
        self._dash_requests: typing.Final[dash.requests.CategoryDashRequests] = dash_requests
        self._form_requests: typing.Final[form.requests.CategoryFormRequests] = form_requests

        self._dash_requests.add.connect(self._on_add_request)
        self._dash_requests.delete.connect(self._on_delete_request)
        self._dash_requests.edit.connect(self._on_edit_request)
        self._dash_requests.refresh.connect(self.refresh)

        self._form_requests.back.connect(self._on_back_request)
        self._form_requests.save.connect(self._on_save_request)

    def refresh(self) -> None:
        logger.debug(f"{self.__class__.__name__}.refresh()")

        try:
            self._set_status("Refreshing categories...")

            categories = self._category_service.all()
            if isinstance(categories, domain.Error):
                self._set_status(categories.error_message)
                return None

            self.states.emit(
                CategoryState(
                    dash_state=dash.CategoryDashState(
                        categories=categories,
                        status="Categories refreshed.",
                    ),
                ),
            )
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.refresh() failed: {e!s}")

            self._set_status(str(e))

    def _on_add_request(self) -> None:
        logger.debug(f"{self.__class__.__name__}._on_add_request()")

        try:
            self.states.emit(
                CategoryState(
                    form_state=form.CategoryFormState.initial(),
                    dash_active=False,
                )
            )
        except Exception as e:
            logger.error(f"{self.__class__.__name__}._on_add_request() failed: {e!s}")

            self._set_status(str(e))

    def _on_delete_request(self, /, request: dash.requests.Delete) -> None:
        logger.debug(f"{self.__class__.__name__}._on_delete_request({request=!r})")

        try:
            delete_result = self._category_service.delete(
                category_id=request.category.category_id,
            )
            if isinstance(delete_result, domain.Error):
                self._set_status(delete_result.error_message)
                return None

            self.categories_updated.emit()

            self.states.emit(
                CategoryState(
                    dash_state=dash.CategoryDashState(
                        category_deleted=request.category,
                        status=f"Deleted {request.category.name}.",
                    )
                )
            )
        except Exception as e:
            logger.error(f"{self.__class__.__name__}._on_delete_request({request=!r}) failed: {e!s}")

            self._set_status(str(e))

    def _on_edit_request(self, /, request: dash.requests.Edit) -> None:
        logger.debug(f"{self.__class__.__name__}._on_edit_request({request=!r})")

        try:
            self.states.emit(
                CategoryState(
                    form_state=form.CategoryFormState.from_domain(category=request.category),
                    dash_active=False,
                )
            )
        except Exception as e:
            logger.error(f"{self.__class__.__name__}._on_edit_request({request=!r}) failed: {e!s}")

            self._set_status(str(e))

    def _on_back_request(self) -> None:
        logger.debug(f"{self.__class__.__name__}._on_back_request()")

        try:
            self.states.emit(CategoryState(dash_active=True))
        except Exception as e:
            logger.error(f"{self.__class__.__name__}._on_back_request() failed: {e!s}")

            self._set_status(str(e))

    def _on_save_request(self, /, event: form.requests.Save) -> None:
        logger.debug(f"{self.__class__.__name__}._on_save_request({event=!r})")

        try:
            if self._category_service.get(category_id=event.category.category_id):
                self._category_service.update(category=event.category)

                self.categories_updated.emit()

                state = CategoryState(
                    dash_state=dash.CategoryDashState(
                        category_edited=event.category,
                        status=f"{event.category.name} updated.",
                    ),
                    dash_active=True,
                )
            else:
                self._category_service.add(category=event.category)

                self.categories_updated.emit()

                state = CategoryState(
                    dash_state=dash.CategoryDashState(
                        category_added=event.category,
                        status=f"{event.category.name} added.",
                    ),
                    dash_active=True,
                )

            self.states.emit(state)
        except Exception as e:
            logger.error(f"{self.__class__.__name__}._on_save_request({event=!r}) failed: {e!s}")

            self._set_status(str(e))

    def _set_status(self, /, status: str) -> None:
        self.states.emit(CategoryState(dash_state=dash.CategoryDashState(status=status)))
