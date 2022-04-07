import sys

import qtawesome as qta
from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw

__all__ = ("RichTextEditor",)

BTN_SIZE = qtc.QSize(20, 20)


class RichTextEditor(qtw.QWidget):
    def __init__(self, icon_color: str = "white"):
        super().__init__()

        highlight_btn_icon = qta.icon("mdi6.format-color-highlight", color=icon_color)
        self._highlight_btn = qtw.QPushButton(highlight_btn_icon, "")
        self._highlight_btn.clicked.connect(self._on_highlight_btn_clicked)
        self._highlight_btn.setToolTip("Highlight")
        self._highlight_btn.setIconSize(BTN_SIZE)

        clear_highlight_btn_icon = qta.icon("mdi.format-color-marker-cancel", color=icon_color)
        self._clear_highlight_btn = qtw.QPushButton(clear_highlight_btn_icon, "")
        self._clear_highlight_btn.clicked.connect(self._on_clear_highlight_btn_clicked)
        self._clear_highlight_btn.setToolTip("Clear Highlight")
        self._clear_highlight_btn.setIconSize(BTN_SIZE)

        bold_btn_icon = qta.icon("mdi.format-bold", color=icon_color)
        self._bold_btn = qtw.QPushButton(bold_btn_icon, "")
        self._bold_btn.clicked.connect(self._bold_btn_clicked)
        self._bold_btn.setToolTip("Bold (Ctrl+B)")
        self._bold_btn.setIconSize(BTN_SIZE)

        bold_shortcut = qtw.QShortcut(qtg.QKeySequence("Ctrl+B"), self)
        bold_shortcut.activated.connect(self._bold_btn.click)

        toolbar = qtw.QHBoxLayout()
        toolbar.addWidget(self._highlight_btn)
        toolbar.addWidget(self._clear_highlight_btn)
        toolbar.addWidget(self._bold_btn)
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

    def _bold_btn_clicked(self) -> None:
        cursor = self._text_edit.textCursor()

        fmt = qtg.QTextCharFormat()

        font = qtg.QFont()

        if cursor.charFormat().fontWeight() == qtg.QFont.Bold:
            font.setBold(False)
        else:
            font.setBold(True)

        fmt.setFont(font)

        cursor.setCharFormat(fmt)

    def _on_clear_highlight_btn_clicked(self) -> None:
        fmt = qtg.QTextCharFormat()
        fmt.clearBackground()
        fmt.setForeground(self.parent().palette().text().color())
        cursor = self._text_edit.textCursor()
        cursor.setCharFormat(fmt)

    def _on_highlight_btn_clicked(self) -> None:
        fmt = qtg.QTextCharFormat()
        fmt.setForeground(qtc.Qt.black)
        fmt.setBackground(qtc.Qt.yellow)
        cursor = self._text_edit.textCursor()
        cursor.setCharFormat(fmt)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = RichTextEditor()
    w.set_value("<b>Te</b>st")
    w.show()
    app.exec()





