import typing

from PyQt6 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa

from src import domain
from src.presentation.category_selector.controller import CategorySelectorController
from src.presentation.category_selector.state import CategorySelectorState
from src.presentation.category_selector.view import CategorySelectorView

__all__ = ("CategorySelectorWidget",)


class CategorySelectorWidget(qtw.QWidget):
    item_selected = qtc.pyqtSignal(domain.Category)

    def __init__(
        self,
        *,
        category_service: domain.CategoryService,
        include_all_category: bool,
        parent: qtw.QWidget | None,
    ):
        super().__init__(parent=parent)

        self._controller = CategorySelectorController(
            category_service=category_service,
            include_all_category=include_all_category,
            parent=self,
        )

        self._view = CategorySelectorView(
            parent=self,
            states=self._controller.states,
        )

        layout = qtw.QStackedLayout()
        layout.addWidget(self._view)
        self.setLayout(layout)

        self.setFixedSize(self._view.size())

        self._view.item_selected.connect(self.item_selected.emit)

    def refresh(self) -> None | domain.Error:
        return self._controller.refresh()

    def selected_item(self) -> domain.Category:
        return self._view.selected_item

    def select_item(self, /, item: domain.Category) -> None:
        self._controller.set_category(item)

    def set_items(self, /, items: typing.Iterable[domain.Category]) -> None:
        self._view.set_state(CategorySelectorState(category_options=tuple(items)))
