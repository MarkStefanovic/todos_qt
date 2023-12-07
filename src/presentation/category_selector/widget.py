from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa

from src import service, domain
from src.presentation.category_selector.controller import CategorySelectorController
from src.presentation.category_selector.view import CategorySelectorView

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

        self._view = CategorySelectorView(parent=self)

        self._controller = CategorySelectorController(
            view=self._view,
            category_service=category_service,
            include_all_category=include_all_category,
            parent=self,
        )

        self._view.item_selected.connect(self.item_selected)

    def get_selected_item(self) -> domain.Category:
        return self._view.get_selected_item()

    def refresh(self) -> None | domain.Error:
        return self._controller.refresh()
