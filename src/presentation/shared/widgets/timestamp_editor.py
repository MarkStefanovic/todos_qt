from __future__ import annotations

import datetime

from dateutil.parser import parse, ParserError
from PyQt6 import QtCore as qtc, QtWidgets as qtw

__all__ = ("TimestampEditor",)


class TimestampEditor(qtw.QWidget):
    def __init__(self, *, fmt: str = "%m/%d/%y @ %I:%M %p", parent: qtw.QWidget | None = None):
        super().__init__(parent=parent)

        self._fmt = fmt

        self._text_edit = qtw.QLineEdit("", parent=self)
        self._text_edit.textChanged.connect(self.validate)
        self._text_edit.setFixedWidth(130)
        self._text_edit.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)

        layout = qtw.QStackedLayout()
        layout.addWidget(self._text_edit)

        self.setLayout(layout)

        self.setSizePolicy(qtw.QSizePolicy.Policy.Fixed, qtw.QSizePolicy.Policy.Fixed)

        self._ts: datetime.datetime | None = None
        self._is_valid = True

    def get_value(self) -> datetime.datetime | None:
        if self._ts == "":
            self._ts = None
        return self._ts

    def set_value(self, value: datetime.datetime | None) -> None:
        if value:
            self._text_edit.setText(value.strftime(self._fmt))
        else:
            self._text_edit.setText("")

    @property
    def is_valid(self) -> bool:
        return self._is_valid

    def validate(self) -> None:
        if self._text_edit.text():
            try:
                self._ts = parse(self._text_edit.text())
                self._is_valid = True
                self._text_edit.setStyleSheet("")
            except ParserError as pe:
                print(pe)
                self._ts = None
                self._is_valid = False
                self._text_edit.setStyleSheet("""border: 1px solid red;""")
        else:
            self._ts = None
            self._is_valid = True
            self._text_edit.setStyleSheet("")
