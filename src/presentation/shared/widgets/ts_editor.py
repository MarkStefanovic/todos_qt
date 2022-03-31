import datetime
import typing

from dateutil.parser import parse, ParserError
from PyQt5 import QtWidgets as qtw

__all__ = ("TsEditor",)


class TsEditor(qtw.QWidget):
    def __init__(self, initial_value: typing.Optional[datetime.datetime] = None):
        super().__init__()

        if initial_value:
            initial_text_value = initial_value.strftime("%m/%d/%Y %I:%M %p")
        else:
            initial_text_value = ""

        self._text_edit = qtw.QLineEdit(initial_text_value)
        self._text_edit.textChanged.connect(self.validate)
        self._text_edit.setFixedWidth(130)
        self._text_edit.setFixedHeight(20)
        self._text_edit.setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)

        self._ts: typing.Optional[datetime.datetime] = initial_value

        self._is_valid = True

        layout = qtw.QStackedLayout()
        layout.addWidget(self._text_edit)

        self.setLayout(layout)

        self.setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)

    @property
    def ts(self) -> typing.Optional[datetime.datetime]:
        if self._ts == "":
            self._ts = None
        return self._ts

    @ts.setter
    def ts(self, value: typing.Optional[datetime.datetime]) -> None:
        if value:
            self._text_edit.setText(value.strftime("%m/%d/%Y %I:%M %p"))
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
                self._text_edit.setStyleSheet("""border: 1px solid red; font-family: "Arial"; font-size: 12px;""")
        else:
            self._ts = None
            self._is_valid = True
            self._text_edit.setStyleSheet("")
