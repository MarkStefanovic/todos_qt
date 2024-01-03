import typing

from PyQt6 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa
from loguru import logger

from src import domain
from src.presentation.category_selector.state import CategorySelectorState
from src.presentation.shared.theme import font

__all__ = ("CategorySelectorView",)


class CategorySelectorView(qtw.QComboBox):
    item_selected = qtc.pyqtSignal(domain.Category)

    def __init__(self, *, states: qtc.pyqtBoundSignal, parent: qtw.QWidget | None):
        super().__init__(parent=parent)

        self._states: typing.Final[qtc.pyqtBoundSignal] = states

        self.setFocusPolicy(qtc.Qt.FocusPolicy.StrongFocus)
        self.setMouseTracking(False)
        self.setStyleSheet("combobox-popup: 0;")

        # noinspection PyUnresolvedReferences
        self.currentIndexChanged.connect(self._on_current_index_changed)

        self.setMaximumHeight(font.DEFAULT_FONT_METRICS.height() + 8)
        self.setFixedWidth(font.DEFAULT_FONT_METRICS.boundingRect(" " * 30).width())
        self.setSizePolicy(qtw.QSizePolicy.Policy.Fixed, qtw.QSizePolicy.Policy.Fixed)

        self._states.connect(self.set_state)

    @property
    def selected_item(self) -> domain.Category:
        if isinstance(self.currentData(), domain.Category):
            return typing.cast(domain.Category, self.currentData())

        logger.error(
            f"{self.__class__.__name__}.selected_item() did not return a domain.Category.  "
            f"It returned {self.currentData()!r}."
        )

        return domain.TODO_CATEGORY

    def set_state(self, /, state: CategorySelectorState) -> None:
        logger.debug(f"{self.__class__.__name__}._set_state({state=!r})")

        if not isinstance(state.category_options, domain.Unspecified):
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

        if isinstance(state.selected_category, domain.Category):
            for ix in range(self.count()):
                category: domain.Category = self.itemData(ix)
                if category.category_id == state.selected_category.category_id:
                    self.setCurrentIndex(ix)
                    return None

    def _on_current_index_changed(self, ix: int) -> None:
        if item := self.itemData(ix):
            self.item_selected.emit(item)
