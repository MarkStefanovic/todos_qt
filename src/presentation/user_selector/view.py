import typing

from PyQt6 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa
from loguru import logger

from src import domain
from src.presentation.shared.theme import font
from src.presentation.user_selector.state import UserSelectorState

__all__ = ("UserSelectorView",)


class UserSelectorView(qtw.QComboBox):
    def __init__(
        self,
        *,
        item_selected_requests: qtc.pyqtBoundSignal,
        states: qtc.pyqtBoundSignal,
        parent: qtw.QWidget | None,
    ):
        super().__init__(parent=parent)

        self._item_selected_requests: typing.Final[qtc.pyqtBoundSignal] = item_selected_requests
        self._states: typing.Final[qtc.pyqtBoundSignal] = states

        self.setFocusPolicy(qtc.Qt.FocusPolicy.StrongFocus)
        self.setMouseTracking(False)
        self.setStyleSheet("combobox-popup: 0;")

        # noinspection PyUnresolvedReferences
        self.currentIndexChanged.connect(self._on_current_index_changed)

        self.setMaximumHeight(font.DEFAULT_FONT_METRICS.height() + 8)
        self.setFixedWidth(font.DEFAULT_FONT_METRICS.boundingRect(" " * 30).width())
        # self.adjustSize()

        self._states.connect(self._set_state)

    def get_selected_item(self) -> domain.User:
        return self.currentData()

    def select_item(self, /, item: domain.User) -> None:
        for ix in range(self.count()):
            user = self.itemData(ix)
            if user.user_id == item.user_id:
                self.setCurrentIndex(ix)
                return None

    def set_items(self, /, items: typing.Iterable[domain.User]) -> None:
        self.blockSignals(True)
        try:
            prior_selection: domain.User = self.currentData()

            self.clear()

            for index, item in enumerate(items):
                self.addItem(item.display_name, userData=item)
                if prior_selection and item.user_id == prior_selection.user_id:
                    self.setCurrentIndex(index)
        finally:
            self.blockSignals(False)
        #
        # self.adjustSize()

    def _on_current_index_changed(self, ix: int) -> None:
        item = self.itemData(ix)
        self._item_selected_requests.emit(item)

    def _set_state(self, /, state: UserSelectorState) -> None:
        logger.debug(f"{self.__class__.__name__}._set_state({state=!r})")

        if not isinstance(state.users, domain.Unspecified):
            self.set_items(state.users)

        if not isinstance(state.selected_category, domain.Unspecified):
            self.select_item(state.selected_category)
