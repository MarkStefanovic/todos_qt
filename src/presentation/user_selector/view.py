import typing

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa

from src import domain
from src.presentation.shared import fonts

__all__ = ("UserSelectorView",)


class UserSelectorView(qtw.QComboBox):
    item_selected = qtc.pyqtSignal(domain.User)

    def __init__(self, *, parent: qtw.QWidget | None):
        super().__init__(parent=parent)

        self.setFont(fonts.NORMAL)

        self.setFocusPolicy(qtc.Qt.StrongFocus)
        self.setMouseTracking(False)
        self.setStyleSheet("combobox-popup: 0;")

        # noinspection PyUnresolvedReferences
        self.currentIndexChanged.connect(self._on_current_index_changed)

        self.addItem(fonts.NORMAL_FONT_METRICS.width(" " * 40))
        self.adjustSize()

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

        self.adjustSize()

    def _on_current_index_changed(self, ix: int) -> None:
        item = self.itemData(ix)
        self.item_selected.emit(item)
