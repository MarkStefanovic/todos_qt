from __future__ import annotations

import dataclasses
import enum
import typing

from PyQt5 import QtCore as qtc, QtWidgets as qtw

__all__ = ("ColAlignment", "ColSpec", "ColSpecType", "Table", "TableSpec")

Key = typing.TypeVar("Key")
Row = typing.TypeVar("Row")


class ColAlignment(enum.Enum):
    Center = enum.auto()
    Left = enum.auto()
    Right = enum.auto()

    @property
    def qt(self) -> qtc.Qt.AlignmentFlag:
        alignment = {
            ColAlignment.Center: qtc.Qt.AlignHCenter | qtc.Qt.AlignTop,
            ColAlignment.Left: qtc.Qt.AlignLeft | qtc.Qt.AlignTop,
            ColAlignment.Right: qtc.Qt.AlignRight | qtc.Qt.AlignTop,
        }[self]
        return typing.cast(qtc.Qt.AlignmentFlag, alignment)


class ColSpecType(enum.Enum):
    Button = enum.auto()
    Date = enum.auto()
    Decimal = enum.auto()
    Float = enum.auto()
    Int = enum.auto()
    RichText = enum.auto()
    Timestamp = enum.auto()
    Text = enum.auto()


@dataclasses.dataclass(frozen=True)
class ColSpec(typing.Generic[Row]):
    attr_name: str | None
    display_name: str | None
    column_width: int | None
    hidden: bool
    type: ColSpecType
    alignment: ColAlignment
    on_click: typing.Callable[[Row], None] | None
    display_fn: typing.Callable[[typing.Any], str] | None

    @staticmethod
    def button(
        *,
        button_text: str,
        column_width: int = 100,
        alignment: ColAlignment = ColAlignment.Center,
        on_click: typing.Callable[[Row], None],
    ) -> ColSpec[Row]:
        return ColSpec(
            attr_name=None,
            display_name=button_text,
            display_fn=None,
            column_width=column_width,
            type=ColSpecType.Button,
            hidden=False,
            alignment=alignment,
            on_click=on_click,
        )

    @staticmethod
    def date(
        *,
        attr_name: str,
        display_name: str,
        display_format: str = "%m/%d/%y",
        column_width: int = 100,
        hidden: bool = False,
        alignment: ColAlignment = ColAlignment.Right,
    ) -> ColSpec[Row]:
        return ColSpec(
            attr_name=attr_name,
            display_name=display_name,
            display_fn=lambda dt: dt.strftime(display_format),
            column_width=column_width,
            type=ColSpecType.Date,
            hidden=hidden,
            alignment=alignment, 
            on_click=None,
        )

    @staticmethod
    def decimal(
        *,
        attr_name: str,
        display_name: str,
        display_format: str = ",.2f",
        column_width: int | None = None,
        hidden: bool = False,
        alignment: ColAlignment = ColAlignment.Right,
    ) -> ColSpec[Row]:
        return ColSpec(
            attr_name=attr_name,
            display_name=display_name,
            display_fn=lambda f: "{}".format(display_format),
            type=ColSpecType.Decimal,
            column_width=column_width,
            hidden=hidden,
            alignment=alignment,
            on_click=None,
        )

    @staticmethod
    def float(
        *,
        attr_name: str,
        display_name: str,
        display_format: str = ",.2f",
        column_width: int | None = None,
        hidden: bool = False,
        alignment: ColAlignment = ColAlignment.Right,
    ) -> ColSpec[Row]:
        return ColSpec(
            attr_name=attr_name,
            display_name=display_name,
            display_fn=lambda f: "{}".format(display_format),
            type=ColSpecType.Float,
            column_width=column_width,
            hidden=hidden,
            alignment=alignment,
            on_click=None,
        )

    @staticmethod
    def int(
        *,
        attr_name: str,
        display_name: str,
        display_format: str = ",.0f",
        column_width: int | None = None,
        hidden: bool = False,
        alignment: ColAlignment = ColAlignment.Right,
    ) -> ColSpec[Row]:
        return ColSpec(
            attr_name=attr_name,
            display_name=display_name,
            display_fn=lambda f: "{}".format(display_format),
            type=ColSpecType.Int,
            column_width=column_width,
            hidden=hidden,
            alignment=alignment,
            on_click=None,
        )

    @staticmethod
    def rich_text(
        *,
        attr_name: str,
        display_name: str,
        column_width: int | None = None,  # type: ignore
        hidden: bool = False,
        alignment: ColAlignment = ColAlignment.Left,
    ) -> ColSpec[Row]:
        return ColSpec(
            attr_name=attr_name,
            display_name=display_name,
            display_fn=None,
            type=ColSpecType.RichText,
            column_width=column_width,
            hidden=hidden,
            alignment=alignment,
            on_click=None,
        )

    @staticmethod
    def text(
        *,
        attr_name: str,
        display_name: str,
        column_width: int | None = None,  # type: ignore
        hidden: bool = False,
        alignment: ColAlignment = ColAlignment.Left,
    ) -> ColSpec[Row]:
        return ColSpec(
            attr_name=attr_name,
            display_name=display_name,
            display_fn=None,
            type=ColSpecType.Text,
            column_width=column_width,
            hidden=hidden,
            alignment=alignment,
            on_click=None,
        )

    @staticmethod
    def timestamp(
        *,
        attr_name: str,
        display_name: str,
        display_format: str = "%m/%d/%y %I:%M:%S %p",
        column_width: int | None = 200,  # type: ignore
        hidden: bool = False,
        alignment: ColAlignment = ColAlignment.Right,
    ) -> ColSpec[Row]:
        return ColSpec(
            attr_name=attr_name,
            display_name=display_name,
            display_fn=lambda ts: ts.strftime(display_format),
            type=ColSpecType.Timestamp,
            column_width=column_width,
            hidden=hidden,
            alignment=alignment,
            on_click=None,
        )


@dataclasses.dataclass(frozen=True)
class TableSpec(typing.Generic[Row]):
    col_specs: list[ColSpec[Row]]
    key_attr: str


class Table(typing.Generic[Row, Key], qtw.QTableWidget):
    def __init__(self, *, spec: TableSpec[Row]):
        super().__init__()

        self._spec = spec

        self._col_indices: dict[str, int] = {}
        for col_num, col_spec in enumerate(self._spec.col_specs):
            if col_spec.attr_name is not None:
                self._col_indices[col_spec.attr_name] = col_num

        headers = [
            ("" if col_spec.type == ColSpecType.Button else col_spec.display_name) or ""
            for col_spec in self._spec.col_specs
        ]

        self.setAlternatingRowColors(True)

        self.setColumnCount(len(headers))

        self.setHorizontalHeaderLabels(headers)

        self.setSortingEnabled(True)

        for col_num, col_spec in enumerate(self._spec.col_specs):
            if col_spec.hidden:
                self.setColumnHidden(col_num, True)

            if col_spec.column_width is not None:
                self.setColumnWidth(col_num, col_spec.column_width)

    def add_item(self, /, item: Row) -> None:
        self.setRowCount(self.rowCount() + 1)
        self._set_row(row_num=self.rowCount(), data=item)

    def clear_selection(self) -> None:
        self.clearSelection()

    def delete_item(self, *, key: Key) -> None:
        row_num = self._get_row_num_for_key(key=key)
        self.removeRow(row_num)

    @property
    def selected_row_key(self) -> typing.Any:
        if indices := self.selectedIndexes():
            row_num = indices[0].row()
            return self.item(row=row_num, column=self._col_indices[self._spec.key_attr]).data(qtc.Qt.EditRole)

    def select_row_by_key(self, *, key: Key) -> None:
        row_num = self._get_row_num_for_key(key=key)
        self.selectRow(row_num)

    def set_all(self, /, data: list[Row]) -> None:
        self.clearContents()
        self.setRowCount(0)
        self.setRowCount(len(data))

        self.setSortingEnabled(False)
        try:
            for row_num, row in enumerate(data):
                self._set_row(row_num=row_num, data=row)
        finally:
            self.setSortingEnabled(True)

    def update_item(self, /, item: Row) -> None:
        row_num = self._get_row_num_for_key(key=getattr(item, self._spec.key_attr))
        self._set_row(row_num=row_num, data=item)

    def _get_row_num_for_key(self, *, key: Key) -> int | None:
        for row_num in range(self.rowCount()):
            if key == self.item(row_num, self._col_indices[self._spec.key_attr]).data(qtc.Qt.EditRole):
                return row_num
        return None

    def _set_row(self, *, row_num: int, data: Row) -> None:
        for col_num, col_spec in enumerate(self._spec.col_specs):
            if col_spec.attr_name is None:
                value = col_spec.display_name
            else:
                value = getattr(data, col_spec.attr_name)
            if col_spec.type in (
                ColSpecType.Date,
                ColSpecType.Decimal,
                ColSpecType.Float,
                ColSpecType.Int,
                ColSpecType.Timestamp,
            ):
                item = qtw.QTableWidgetItem()
                item.setData(qtc.Qt.EditRole, value)
                if col_spec.display_fn is None:
                    item.setText(value)
                else:
                    item.setText(col_spec.display_fn(value))
                item.setTextAlignment(col_spec.alignment.qt)
                self.setItem(row_num, col_num, item)
            elif col_spec.type == ColSpecType.Text:
                item = qtw.QTableWidgetItem(value)
                item.setTextAlignment(col_spec.alignment.qt)
                self.setItem(row_num, col_num, item)
            elif col_spec.type == ColSpecType.RichText:
                widget = qtw.QTextEdit(value)
                self.setCellWidget(row=row_num, column=col_num, widget=widget)
            elif col_spec.type == ColSpecType.Button:
                btn = qtw.QPushButton(col_spec.display_name)
                btn.setFixedHeight(22)
                # noinspection PyUnresolvedReferences
                btn.clicked.connect(lambda: col_spec.on_click(data))
                self.setCellWidget(row_num, col_num, btn)
            else:
                raise ValueError(f"Unrecognized ColSpecType: {col_spec.type!r}.")

            if col_spec.column_width is not None:
                self.setColumnWidth(col_num, col_spec.column_width)
            else:
                self.resizeColumnToContents(col_num)
