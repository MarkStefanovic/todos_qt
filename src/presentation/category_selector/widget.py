from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa

from src import service, domain
from src.presentation.category_selector.controller import CategorySelectorController
from src.presentation.category_selector.view import CategorySelectorView
from src.presentation.category_selector.requests import CategorySelectorRequests


__all__ = ("CategorySelectorWidget",)


class CategorySelectorWidget(qtw.QWidget):
    item_selected = qtc.pyqtSignal(domain.Category)

    def __init__(
        self,
        *,
        category_service: service.CategoryService,
        include_all_category: bool,
        parent: qtw.QWidget | None,
    ):
        super().__init__(parent=parent)

        self._requests = CategorySelectorRequests(parent=self)

        self._controller = CategorySelectorController(
            category_selector_requests=self._requests,
            category_service=category_service,
            include_all_category=include_all_category,
            parent=self,
        )

        self._view = CategorySelectorView(
            parent=self,
            states=self._controller.states,
        )

        self._view.item_selected.connect(self.item_selected)

    def selected_item(self) -> domain.Category:
        return self._view.selected_item

    def refresh(self) -> None | domain.Error:
        return self._controller.refresh()

    def select_item(self, /, item: domain.Category) -> None:
        self._controller.set_category(item)
