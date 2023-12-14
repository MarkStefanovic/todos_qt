# noinspection PyPep8Naming
from PyQt5 import QtCore as qtc

__all__ = ("CategorySelectorRequests",)


class CategorySelectorRequests(qtc.QObject):
    refresh: qtc.pyqtBoundSignal = qtc.pyqtSignal()
