import typing

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa
from loguru import logger

from src import service, domain
from src.presentation.category_selector.view import CategorySelectorView

__all__ = ("CategorySelectorController",)


class CategorySelectorController(qtc.QObject):
    def __init__(
        self,
        *,
        view: CategorySelectorView,
        category_service: service.CategoryService,
        include_all_category: bool,
        parent: qtc.QObject | None,
    ):
        super().__init__(parent=parent)

        self._view: typing.Final[CategorySelectorView] = view
        self._category_service: typing.Final[service.CategoryService] = category_service
        self._include_all_category: typing.Final[bool] = include_all_category

    def refresh(self) -> None | domain.Error:
        logger.debug(f"{self.__class__.__name__}.refresh()")

        try:
            self._category_service.refresh()

            categories = self._category_service.all()

            if self._include_all_category:
                categories.insert(0, domain.ALL_CATEGORY)

            self._view.set_items(categories)

            return None
        except Exception as e:
            return domain.Error.new(str(e))
