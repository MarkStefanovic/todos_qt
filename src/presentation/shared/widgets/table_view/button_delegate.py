"""
https://stackoverflow.com/questions/4857274/pyside-pyqt-qstyleditemdelegate-list-in-table?rq=3
https://stackoverflow.com/questions/47849366/pyqt-qpushbutton-delegate-in-column-of-a-treeview
https://stackoverflow.com/questions/11777637/adding-button-to-qtableview
https://stackoverflow.com/questions/61432097/custom-qpushbutton-inside-qstyleditemdelegate
https://stackoverflow.com/questions/11777637/adding-button-to-qtableview
"""
import typing

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa

__all__ = ("ButtonDelegate",)


class ButtonDelegate(qtw.QStyledItemDelegate):
    clicked = qtc.pyqtSignal(qtc.QModelIndex)

    def __init__(
        self,
        *,
        text: str,
        button_text_selector: typing.Callable[[qtc.QModelIndex], str] | None,
        enabled_selector: typing.Callable[[qtc.QModelIndex], bool] | None,
        parent: qtw.QWidget | None,
    ):
        super().__init__(parent=parent)

        self._text: typing.Final[str] = text
        self._button_text_selector: typing.Final[typing.Callable[[qtc.QModelIndex], str] | None] = button_text_selector
        self._enabled_selector: typing.Final[typing.Callable[[qtc.QModelIndex], bool] | None] = enabled_selector

        self._btn = qtw.QPushButton(self._text)
        self._btn.setFocusPolicy(qtc.Qt.NoFocus)

    def editorEvent(
        self,
        event: qtc.QEvent,
        model: qtc.QAbstractItemModel,
        option: qtw.QStyleOptionViewItem,
        index: qtc.QModelIndex,
    ) -> bool:
        # if event.type() == qtc.QEvent.MouseMove:
        #     if option.rect.top() < event.y() < option.rect.top() + self._height:
        #         print("mouse_over")

        if event is not None:
            if event.type() == qtc.QEvent.MouseButtonRelease:
                button_height = min(option.fontMetrics.height() + 8, option.rect.height())

                y_coord: int = event.y()  # type: ignore
                if option.rect.top() < y_coord < option.rect.top() + button_height:
                    self._on_click(index=index)

                return True

        return super().editorEvent(event, model, option, index)

    def paint(
        self,
        painter: qtg.QPainter,
        option: qtw.QStyleOptionViewItem,
        index: qtc.QModelIndex,
    ) -> None:
        btn = qtw.QStyleOptionButton()

        if self._button_text_selector is None:
            btn_text = self._text
        else:
            # noinspection PyArgumentList
            btn_text = self._button_text_selector(index=index)  # type: ignore

        btn.text = btn_text

        # btn.features = qtw.QStyleOptionButton.DefaultButton
        btn.rect = qtc.QRect(
            option.rect.x(),
            option.rect.y(),
            option.rect.width(),
            min(option.fontMetrics.height() + 8, option.rect.height()),
        )

        if self._button_is_enabled(index=index):
            btn.state = (
                qtw.QStyle.State_Raised if option.state & qtw.QStyle.State_MouseOver else qtw.QStyle.State_Sunken
            )
        else:
            btn.state = qtw.QStyle.State_Off

        self._btn.style().drawControl(qtw.QStyle.CE_PushButton, btn, painter, self._btn)

    def _on_click(self, *, index: qtc.QModelIndex) -> None:
        self.clicked.emit(index)

    def _button_is_enabled(self, *, index: qtc.QModelIndex) -> bool:
        if self._enabled_selector is None:
            return True

        return self._enabled_selector(index=index)  # type: ignore
