import datetime

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa

from src.presentation.shared import fonts

__all__ = ("StatusBar",)


class StatusBar(qtw.QStatusBar):
    def __init__(self, *, parent: qtw.QWidget | None):
        super().__init__(parent=parent)

        self.setFont(fonts.NORMAL)

    def set_status(self, /, status: str) -> None:
        self.showMessage(f"{datetime.datetime.now():%I:%M %p}: {status}")
        self.repaint()
