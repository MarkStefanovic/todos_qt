import sys

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw
from src.presentation.shared import icons

import qtawesome as qta

__all__ = ("RichTextEditor",)


BTN_SIZE = qtc.QSize(20, 20)


class RichTextEditor(qtw.QWidget):
    def __init__(self, parent: qtw.QWidget | None = None):
        super().__init__(parent=parent)

        # icon_color = self.parent().palette().text().color()

        highlight_btn_icon = qta.icon(icons.highlight_btn_icon_name, color=self.parent().palette().text().color())
        self._highlight_btn = qtw.QPushButton(highlight_btn_icon, "", parent=self)
        self._highlight_btn.clicked.connect(self._on_highlight_btn_clicked)
        self._highlight_btn.setToolTip("Highlight")
        self._highlight_btn.setIconSize(BTN_SIZE)

        clear_highlight_btn_icon = qta.icon(icons.clear_highlight_btn_icon_name, color=self.parent().palette().text().color())
        self._clear_highlight_btn = qtw.QPushButton(clear_highlight_btn_icon, "", parent=self)
        self._clear_highlight_btn.clicked.connect(self._on_clear_highlight_btn_clicked)
        self._clear_highlight_btn.setToolTip("Clear Highlight")
        self._clear_highlight_btn.setIconSize(BTN_SIZE)

        bold_btn_icon = qta.icon(icons.bold_btn_icon_name, color=self.parent().palette().text().color())
        self._bold_btn = qtw.QPushButton(bold_btn_icon, "", parent=self)
        self._bold_btn.clicked.connect(self._bold_btn_clicked)
        self._bold_btn.setToolTip("Bold (Ctrl+B)")
        self._bold_btn.setIconSize(BTN_SIZE)

        clear_bold_btn_icon = qta.icon(icons.clear_bold_btn_icon_name, color=self.parent().palette().text().color())
        self._clear_bold_btn = qtw.QPushButton(clear_bold_btn_icon, "", parent=self)
        self._clear_bold_btn.clicked.connect(self._on_clear_bold_btn_clicked)
        self._clear_bold_btn.setToolTip("Clear Bold")
        self._clear_bold_btn.setIconSize(BTN_SIZE)

        bold_shortcut = qtw.QShortcut(qtg.QKeySequence("Ctrl+B"), self)
        bold_shortcut.activated.connect(self._bold_btn.click)

        toolbar = qtw.QHBoxLayout()
        toolbar.addWidget(self._highlight_btn)
        toolbar.addWidget(self._clear_highlight_btn)
        toolbar.addWidget(self._bold_btn)
        toolbar.addWidget(self._clear_bold_btn)
        toolbar.addSpacerItem(qtw.QSpacerItem(0, 0, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum))

        self._text_edit = qtw.QTextEdit()
        self._text_edit.setAcceptRichText(True)

        layout = qtw.QVBoxLayout()
        layout.addLayout(toolbar)
        layout.addWidget(self._text_edit)

        self.setLayout(layout)

    def get_value(self) -> str:
        return self._text_edit.toHtml()

    def set_value(self, /, value: str) -> None:
        self._text_edit.setHtml(value)

    def _on_clear_bold_btn_clicked(self) -> None:
        cursor = self._text_edit.textCursor()
        fmt = cursor.charFormat()
        fmt.setFontWeight(qtg.QFont.Normal)
        cursor.mergeCharFormat(fmt)

    def _bold_btn_clicked(self) -> None:
        cursor = self._text_edit.textCursor()
        fmt = cursor.charFormat()
        fmt.setFontWeight(qtg.QFont.Bold)
        cursor.mergeCharFormat(fmt)

    def _on_clear_highlight_btn_clicked(self) -> None:
        cursor = self._text_edit.textCursor()
        fmt = cursor.charFormat()
        fmt.setForeground(self.parent().palette().text().color())
        fmt.setBackground(self.parent().palette().base().color())
        cursor.mergeCharFormat(fmt)

    def _on_highlight_btn_clicked(self) -> None:
        cursor = self._text_edit.textCursor()
        fmt = cursor.charFormat()
        fmt.setBackground(qtc.Qt.yellow)
        fmt.setForeground(qtc.Qt.black)
        cursor.mergeCharFormat(fmt)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = RichTextEditor()
    w.set_value("<b>Te</b>st")
    w.show()
    app.exec()





