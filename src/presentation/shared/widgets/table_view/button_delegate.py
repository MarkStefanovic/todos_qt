import typing

from PyQt6 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa


__all__ = ("ButtonDelegate",)

from src.presentation.shared.widgets.table_view.bound_button_enabled_selector import BoundButtonEnabledSelector
from src.presentation.shared.widgets.table_view.bound_button_text_selector import BoundButtonTextSelector


class ButtonDelegate(qtw.QStyledItemDelegate):
    def __init__(
        self,
        *,
        text: str,
        button_text_selector: BoundButtonTextSelector | None,
        enabled_selector: BoundButtonEnabledSelector | None,
        icon: qtg.QIcon | None,
        normal_font: qtg.QFont,
        bold_font: qtg.QFont,
        parent: qtw.QWidget | None,
    ):
        super().__init__(parent=parent)

        self._text: typing.Final[str] = text
        self._icon: typing.Final[qtg.QIcon | None] = icon
        self._button_text_selector: typing.Final[BoundButtonTextSelector | None] = button_text_selector
        self._enabled_selector: typing.Final[BoundButtonEnabledSelector | None] = enabled_selector
        self._normal_font: typing.Final[qtg.QFont] = normal_font
        self._bold_font: typing.Final[qtg.QFont] = bold_font

        self._btn = qtw.QPushButton(self._text)
        self._btn.setStyleSheet("border-radius: 0px;")

        self._btn.setFocusPolicy(qtc.Qt.FocusPolicy.NoFocus)

    def paint(
        self,
        painter: qtg.QPainter | None,
        option: qtw.QStyleOptionViewItem,
        index: qtc.QModelIndex,
    ) -> None:
        if self._enabled_selector is not None:
            if not self._enabled_selector.is_enabled(index):
                return None

        btn = qtw.QStyleOptionButton()

        bold_font_metrics = qtg.QFontMetrics(self._bold_font)

        if self._icon:
            btn.icon = self._icon
            btn.iconSize = qtc.QSize(
                min(option.rect.width() - 4, bold_font_metrics.height() - 4),
                min(option.rect.height() - 4, bold_font_metrics.height() - 4),
            )
        else:
            if self._button_text_selector is None:
                btn_text = self._text
            else:
                btn_text = self._button_text_selector.get_text(index)

            btn.text = btn_text

        btn.rect = option.rect

        if option.state & qtw.QStyle.StateFlag.State_MouseOver:
            btn.state = qtw.QStyle.StateFlag.State_Enabled | qtw.QStyle.StateFlag.State_Sunken
        else:
            btn.state = qtw.QStyle.StateFlag.State_Enabled | qtw.QStyle.StateFlag.State_Raised

        if style := self._btn.style():
            style.drawControl(
                qtw.QStyle.ControlElement.CE_PushButton,
                btn,
                painter,
                self._btn,
            )

    def sizeHint(self, option: qtw.QStyleOptionViewItem, index: qtc.QModelIndex) -> qtc.QSize:
        if self._icon is None:
            if self._button_text_selector is None:
                btn_text = self._text
            else:
                btn_text = self._button_text_selector.get_text(index)

            bold_font_metrics = qtg.QFontMetrics(self._bold_font)

            return qtc.QSize(
                bold_font_metrics.boundingRect(btn_text).width() + (2 * bold_font_metrics.averageCharWidth()),
                option.rect.height(),
            )

        return super().sizeHint(option, index)
