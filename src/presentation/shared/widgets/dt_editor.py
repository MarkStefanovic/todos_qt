import datetime
import typing

from dateutil.parser import parse, ParserError
from PyQt5 import QtCore as qtc, QtWidgets as qtw

__all__ = ("DtEditor",)


class DtEditor(qtw.QWidget):
    date_changed = qtc.pyqtSignal()

    def __init__(self, initial_value: typing.Optional[datetime.date] = None):
        super().__init__()

        if initial_value:
            initial_text_value = initial_value.strftime("%m/%d/%Y")
        else:
            initial_text_value = ""

        self._text_edit = qtw.QLineEdit(initial_text_value)
        self._text_edit.textChanged.connect(self._on_text_changed)
        self._text_edit.setFixedWidth(80)
        self._text_edit.setFixedHeight(20)
        self._text_edit.setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)

        self._dt: typing.Optional[datetime.date] = initial_value

        self._is_valid = True

        layout = qtw.QStackedLayout()
        layout.addWidget(self._text_edit)

        self.setLayout(layout)

        self.setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)

    @property
    def dt(self) -> typing.Optional[datetime.date]:
        return self._dt

    @dt.setter
    def dt(self, value: typing.Optional[datetime.date]) -> None:
        if value:
            self._text_edit.setText(value.strftime("%m/%d/%Y"))
        else:
            self._text_edit.setText("")

    @property
    def is_valid(self) -> bool:
        return self._is_valid

    def _on_text_changed(self) -> None:
        if self._text_edit.text():
            try:
                self._dt = parse(self._text_edit.text()).date()
                self._is_valid = True
                self._text_edit.setStyleSheet("")
                self.date_changed.emit()
            except ParserError as pe:
                print(pe)
                self._dt = None
                self._is_valid = False
                # self._text_edit.setStyleSheet("border: 1px solid red")
                self._text_edit.setStyleSheet("""border: 1px solid red; font-family: "Arial"; font-size: 12px;""")
        else:
            self._dt = None
            self._is_valid = True
            self._text_edit.setStyleSheet("")
