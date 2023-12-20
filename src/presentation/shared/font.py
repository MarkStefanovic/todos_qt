import typing

# noinspection PyPep8Naming
from PyQt5 import QtGui as qtg

__all__ = (
    "DEFAULT_FONT",
    "DEFAULT_FONT_METRICS",
    "BOLD_FONT",
    "BOLD_FONT_METRICS",
)


DEFAULT_FONT: typing.Final[qtg.QFont] = qtg.QFont()
DEFAULT_FONT.setFamily("Arial")
DEFAULT_FONT.setPointSize(12)

DEFAULT_FONT_METRICS = qtg.QFontMetrics(DEFAULT_FONT)

BOLD_FONT: typing.Final[qtg.QFont] = qtg.QFont()
BOLD_FONT.setFamily("Arial")
BOLD_FONT.setPointSize(12)
BOLD_FONT.setBold(True)
BOLD_FONT_METRICS = qtg.QFontMetrics(BOLD_FONT)
