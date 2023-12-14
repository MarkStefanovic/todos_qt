import typing

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa

from src import domain
from src.presentation.category_selector.state import CategorySelectorState
from src.presentation.shared import fonts

__all__ = ("CategorySelectorView",)


class CategorySelectorView(qtw.QComboBox):
    item_selected = qtc.pyqtSignal(domain.Category)

    def __init__(self, *, states: qtc.pyqtBoundSignal, parent: qtw.QWidget | None):
        super().__init__(parent=parent)

        self._states: typing.Final[qtc.pyqtBoundSignal] = states

        self.setFont(fonts.NORMAL)

        self.setFocusPolicy(qtc.Qt.StrongFocus)
        self.setMouseTracking(False)
        self.setStyleSheet("combobox-popup: 0;")

        # noinspection PyUnresolvedReferences
        self.currentIndexChanged.connect(self._on_current_index_changed)

        self.addItem(" " * 40)
        self.adjustSize()

        self._states.connect(self._set_state)

    @property
    def selected_item(self) -> domain.Category:
        return self.currentData()

    def _set_state(self, /, state: CategorySelectorState) -> None:
        if isinstance(state.category_options, tuple):
            self.blockSignals(True)
            try:
                prior_selection: domain.Category = self.currentData()

                self.clear()

                for index, item in enumerate(state.category_options):
                    self.addItem(item.name, userData=item)
                    if prior_selection and item.category_id == prior_selection.category_id:
                        self.setCurrentIndex(index)
            finally:
                self.blockSignals(False)

            self.adjustSize()

        if isinstance(state.selected_category, domain.Category):
            for ix in range(self.count()):
                category: domain.Category = self.itemData(ix)
                if category.category_id == state.selected_category.category_id:
                    self.setCurrentIndex(ix)
                    return None

    def _on_current_index_changed(self, ix: int) -> None:
        item = self.itemData(ix)
        self.item_selected.emit(item)
