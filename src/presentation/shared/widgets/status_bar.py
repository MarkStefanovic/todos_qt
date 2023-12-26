import datetime

from PyQt6 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa

__all__ = ("StatusBar",)


class StatusBar(qtw.QStatusBar):
    def __init__(self, *, parent: qtw.QWidget | None):
        super().__init__(parent=parent)

        self._message: str = ""

    @property
    def message(self) -> str:
        return self._message

    def set_status(self, /, status: str) -> None:
        self._message = status

        self.showMessage(f"{datetime.datetime.now():%I:%M %p}: {status}")
        self.repaint()
