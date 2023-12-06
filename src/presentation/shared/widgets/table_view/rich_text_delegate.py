"""
ref: https://gist.github.com/jniemann66/dbc298b35a840bf3f1a2206ea6284c7b
"""
import math

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa
from src.presentation.shared import fonts

__all__ = ("RichTextDelegate",)


class RichTextDelegate(qtw.QStyledItemDelegate):
    def __init__(self, *, parent: qtw.QWidget | None):
        super().__init__(parent)

    def paint(
        self,
        painter: qtg.QPainter,
        option: qtw.QStyleOptionViewItem,
        index: qtc.QModelIndex,
    ) -> None:
        if option.state & qtw.QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())

        painter.save()

        document = qtg.QTextDocument()
        document.setTextWidth(option.rect.width())

        value: qtc.QVariant | str = index.data(qtc.Qt.DisplayRole)
        if isinstance(value, qtc.QVariant):
            if value.isValid() and not value.isNull():
                s: str = str(value.value())
            else:
                s = ""
        else:
            s = str(value)

        document.setDefaultFont(fonts.NORMAL)

        document.setHtml(s)

        painter.translate(option.rect.topLeft())
        document.drawContents(painter)

        painter.restore()

    def sizeHint(self, option: qtw.QStyleOptionViewItem, index: qtc.QModelIndex) -> qtc.QSize:
        options = option
        self.initStyleOption(options, index)

        doc = qtg.QTextDocument()
        doc.setHtml(options.text)
        doc.setTextWidth(options.rect.width())

        return qtc.QSize(option.rect.width(), math.ceil(doc.size().height()))
