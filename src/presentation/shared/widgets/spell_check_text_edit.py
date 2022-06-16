from __future__ import annotations

import re
import sys

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw

import enchant

__all__ = ("SpellCheckTextEdit",)


class SpellCheckTextEdit(qtw.QTextEdit):
    def __init__(self, parent: qtw.QWidget | None = None):
        super().__init__(parent=parent)

        self.dict = enchant.Dict("en_US")

        self.highlighter = Highlighter(document=self.document())
        self.highlighter.set_dictionary(self.dict)

    def mousePressEvent2(self, event: qtg.QMouseEvent) -> None:
        if event.button() == qtc.Qt.RightButton:
            # Rewrite the mouse event to a left button event so the cursor is moved to the location of the pointer.
            event = qtg.QMouseEvent(
                qtc.QEvent.MouseButtonPress,
                event.pos(),
                qtc.Qt.LeftButton,
                qtc.Qt.LeftButton,
                qtc.Qt.NoModifier,
            )
        super().mousePressEvent(event)

    def contextMenuEvent(self, event: qtg.QContextMenuEvent) -> None:
        popup_menu = self.createStandardContextMenu()

        # Select the word under the cursor.
        cursor = self.textCursor()
        cursor.select(qtg.QTextCursor.WordUnderCursor)
        self.setTextCursor(cursor)

        # Check if the selected word is misspelled and offer spelling suggestions if it is.
        if self.textCursor().hasSelection():
            text = self.textCursor().selectedText()
            if not self.dict.check(text):
                spell_menu = qtw.QMenu("Spelling Suggestions")
                for word in self.dict.suggest(text):
                    action = SpellAction(text=word, parent=spell_menu)
                    action.correct.connect(self.correct_word)  # noqa
                    spell_menu.addAction(action)
                # Only add the spelling suggests to the menu if there are suggestions.
                if spell_menu.actions():
                    popup_menu.insertSeparator(popup_menu.actions()[0])
                    popup_menu.insertMenu(popup_menu.actions()[0], spell_menu)

        popup_menu.exec_(event.globalPos())

    def correct_word(self, word: str) -> None:
        """Replace the selected text"""
        cursor = self.textCursor()
        cursor.beginEditBlock()

        cursor.removeSelectedText()
        cursor.insertText(word)

        cursor.endEditBlock()

    def highlighter_enabled(self) -> bool:
        return self.highlighter.document() is not None

    def set_highlighter_enabled(self, enable: bool) -> None:
        if enable:
            self.highlighter.setDocument(self.document())
        else:
            self.highlighter.setDocument(None)  # type: ignore


class Highlighter(qtg.QSyntaxHighlighter):
    WORDS = r"(?iu)[\w']+"

    def __init__(self, *, document: qtg.QTextDocument):
        super().__init__(document)

        self._dictionary = None

    def set_dictionary(self, /, dictionary: enchant.Dict) -> None:
        self._dictionary = dictionary

    def highlightBlock(self, text: str) -> None:
        if not self._dictionary:
            return

        fmt = qtg.QTextCharFormat()
        fmt.setUnderlineColor(qtc.Qt.red)
        fmt.setUnderlineStyle(qtg.QTextCharFormat.SpellCheckUnderline)

        for word_object in re.finditer(self.WORDS, text):
            if not self._dictionary.check(word_object.group()):
                self.setFormat(word_object.start(), word_object.end() - word_object.start(), fmt)


class SpellAction(qtw.QAction):
    """QAction that returns the text in a signal"""

    correct = qtc.pyqtSignal(str)

    def __init__(self, *, text: str, parent: qtc.QObject):
        super().__init__(parent)

        self.setText(text)

        self.triggered.connect(lambda x: self.correct.emit(self.text()))  # noqa


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    spellEdit = SpellCheckTextEdit()
    spellEdit.show()
    app.exec_()
    sys.exit(0)
