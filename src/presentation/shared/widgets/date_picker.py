import datetime

from PyQt5 import QtCore as qtc, QtWidgets as qtw  # noqa

from src.presentation.shared import font

__all__ = ("DatePicker",)


class DatePicker(qtw.QDateEdit):
    date_changed = qtc.pyqtSignal()

    def __init__(self, *, parent: qtw.QWidget | None):
        super().__init__(parent=parent)

        self.setCalendarPopup(True)
        # self.setFont(theme.fonts.NORMAL)
        # self.setStyleSheet(theme.fonts.INTERACTIVE_WIDGET_STYLESHEET)
        # self.menuBar().setCornerWidget(self._date_edit, qtc.Qt.Corner.TopLeftCorner)
        # self._date_edit.setDateTime(qtc.QDateTime.currentDateTime())
        self.setAlignment(qtc.Qt.AlignHCenter)
        self.setDisplayFormat("MM/dd/yyyy")
        self.setFixedWidth(font.DEFAULT_FONT_METRICS.width("  88/88/8888  "))
        self.setFixedHeight(font.DEFAULT_FONT_METRICS.height())

        self.dateChanged.connect(lambda: self.date_changed.emit())  # noqa

    def get_value(self) -> datetime.date | None:
        return self.date().toPyDate()

    def set_value(self, /, value: datetime.date | None) -> None:
        if value:
            self.setDate(value)
        else:
            self.clear()
