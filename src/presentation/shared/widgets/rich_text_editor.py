import sys

import qtawesome as qta
from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw

__all__ = ("RichTextEditor",)

BTN_SIZE = qtc.QSize(20, 20)


class RichTextEditor(qtw.QWidget):
    def __init__(self):
        super().__init__()

        highlight_btn_icon = qta.icon("mdi6.format-color-highlight")
        self._highlight_btn = qtw.QPushButton(highlight_btn_icon, "")
        self._highlight_btn.clicked.connect(self._on_highlight_btn_clicked)
        self._highlight_btn.setToolTip("Highlight")
        self._highlight_btn.setIconSize(BTN_SIZE)

        clear_highlight_btn_icon = qta.icon("mdi.format-color-marker-cancel")
        self._clear_highlight_btn = qtw.QPushButton(clear_highlight_btn_icon, "")
        self._clear_highlight_btn.clicked.connect(self._on_clear_highlight_btn_clicked)
        self._clear_highlight_btn.setToolTip("Clear Highlight")
        self._clear_highlight_btn.setIconSize(BTN_SIZE)

        bold_btn_icon = qta.icon("mdi.format-bold")
        self._bold_btn = qtw.QPushButton(bold_btn_icon, "")
        self._bold_btn.clicked.connect(self._bold_btn_clicked)
        self._bold_btn.setToolTip("Bold")
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

        cursor = self._text_edit.textCursor()
        cursor.setCharFormat(fmt)

    def _on_highlight_btn_clicked(self) -> None:
        fmt = qtg.QTextCharFormat()
        fmt.setBackground(qtc.Qt.yellow)

        cursor = self._text_edit.textCursor()
        cursor.setCharFormat(fmt)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = RichTextEditor()
    w.show()
    app.exec()





