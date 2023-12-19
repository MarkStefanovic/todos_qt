import typing

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa
from loguru import logger

from src import domain
from src.presentation.category_selector.state import CategorySelectorState

__all__ = ("CategorySelectorController",)


class CategorySelectorController(qtc.QObject):
    states = qtc.pyqtSignal(CategorySelectorState)

    def __init__(
        self,
        *,
        category_service: domain.CategoryService,
        include_all_category: bool,
        parent: qtc.QObject | None,
    ):
        super().__init__(parent=parent)

        self._category_service: typing.Final[domain.CategoryService] = category_service
        self._include_all_category: typing.Final[bool] = include_all_category

    def refresh(self) -> None | domain.Error:
        logger.debug(f"{self.__class__.__name__}.refresh()")

        try:
            categories = self._category_service.all()
            if isinstance(categories, domain.Error):
                return categories

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
