import typing

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa
from loguru import logger

from src import service, domain
from src.presentation.category_selector import requests
from src.presentation.category_selector.state import CategorySelectorState

__all__ = ("CategorySelectorController",)


class CategorySelectorController(qtc.QObject):
    states: qtc.pyqtBoundSignal = qtc.pyqtSignal(CategorySelectorState)

    def __init__(
        self,
        *,
        category_selector_requests: requests.CategorySelectorRequests,
        category_service: service.CategoryService,
        include_all_category: bool,
        parent: qtc.QObject | None,
    ):
        super().__init__(parent=parent)

        self._category_selector_requests = category_selector_requests
        self._category_service: typing.Final[service.CategoryService] = category_service
        self._include_all_category: typing.Final[bool] = include_all_category

        self._category_selector_requests.refresh.connect(self.refresh)

    def refresh(self) -> None | domain.Error:
        logger.debug(f"{self.__class__.__name__}.refresh()")

        try:
            categories = self._category_service.all()

            if self._include_all_category:
                categories.insert(0, domain.ALL_CATEGORY)

            state = CategorySelectorState(
                selected_category=domain.Unspecified(),
                category_options=tuple(categories),
            )

            self.states.emit(state)

            return None
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.refresh() failed: {e!s}")

            return domain.Error.new(str(e))

    def set_category(self, /, category: domain.Category) -> None:
        state = CategorySelectorState(selected_category=category)

        self.states.emit(state)
