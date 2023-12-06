from PyQt5 import QtGui as qtg

__all__ = (
    "NORMAL",
    "BOLD",
)


NORMAL = qtg.QFont("Arial", 12)

BOLD = qtg.QFont("Arial", 12)
BOLD.setBold(True)
