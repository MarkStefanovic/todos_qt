import typing

from PyQt5 import QtGui as qtg  # noqa

__all__ = (
    "NORMAL",
    "NORMAL_FONT_METRICS",
    "BOLD",
    "BOLD_FONT_METRICS",
)


NORMAL: typing.Final[qtg.QFont] = qtg.QFont("Arial", 12)

NORMAL_FONT_METRICS: typing.Final[qtg.QFontMetrics] = qtg.QFontMetrics(NORMAL)

BOLD: typing.Final[qtg.QFont] = qtg.QFont("Arial", 12)
BOLD.setBold(True)

BOLD_FONT_METRICS: typing.Final[qtg.QFontMetrics] = qtg.QFontMetrics(BOLD)
