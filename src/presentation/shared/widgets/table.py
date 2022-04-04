from __future__ import annotations

import dataclasses
import datetime
import decimal
import enum
import typing

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw

__all__ = (
    "ColAlignment",
    "ColSpec",
    "ColSpecType",
    "Table",
    "TableSpec",
    "button_col",
    "date_col",
    "decimal_col",
    "float_col",
    "int_col",
    "text_col",
    "timestamp_col",
)

Key = typing.TypeVar("Key")
Row = typing.TypeVar("Row")
Value = typing.TypeVar("Value")


class ColAlignment(enum.Enum):
    Center = enum.auto()
    Left = enum.auto()
    Right = enum.auto()

    @property
    def qt_alignment(self) -> int:
        return int(
            {
                ColAlignment.Center: qtc.Qt.AlignHCenter | qtc.Qt.AlignTop,
                ColAlignment.Left: qtc.Qt.AlignLeft | qtc.Qt.AlignTop,
                ColAlignment.Right: qtc.Qt.AlignRight | qtc.Qt.AlignTop,
            }[self]
        )


class ColSpecType(enum.Enum):
    Button = enum.auto()
    Date = enum.auto()
    Decimal = enum.auto()
    Dropdown = enum.auto()
    Float = enum.auto()
    Int = enum.auto()
    RichText = enum.auto()
    Timestamp = enum.auto()
    Text = enum.auto()


@dataclasses.dataclass(frozen=True)
class ColSpec(typing.Generic[Row, Value]):
    attr_name: str | None
    selector: typing.Callable[[Row], typing.Any] | None
    display_name: str | None
    column_width: int | None
    hidden: bool
    type: ColSpecType
    alignment: ColAlignment
    on_click: typing.Callable[[Row], None] | None
    display_fn: typing.Callable[[typing.Any], str]
    enable_when: typing.Callable[[Row], bool] | None
    values: dict[Value, str] | None
    on_value_changed: typing.Callable[[Value], None] | None

    def __post_init__(self) -> None:
        if self.type != ColSpecType.Button:
            assert self.attr_name is not None or self.selector is not None, "Either [attr_name] or [selector] must be provided, but both were None."


def button_col(
    *,
    button_text: str,
    column_width: int = 100,
    alignment: ColAlignment = ColAlignment.Center,
    enable_when: typing.Callable[[Row], bool] | None = None,
    on_click: typing.Callable[[Row], None],
) -> ColSpec[Row, str]:
    return ColSpec(
        attr_name=None,
        selector=None,
        display_name=button_text,
        display_fn=str,
        column_width=column_width,
        type=ColSpecType.Button,
        hidden=False,
        alignment=alignment,
        on_click=on_click,
        enable_when=enable_when,
        values=None,
        on_value_changed=None,
    )


def date_col(
    *,
    display_name: str,
    attr_name: str | None = None,
    selector: typing.Callable[[Row], datetime.date] | None = None,
    display_format: str = "%m/%d/%y",
    column_width: int = 100,
    hidden: bool = False,
    alignment: ColAlignment = ColAlignment.Right,
    display_fn: typing.Callable[[datetime.date], str] | None = None,
) -> ColSpec[Row, datetime.date]:
    if display_fn is None:
        display_fn = lambda dt: "" if dt is None or dt == datetime.date(1900, 1, 1) else dt.strftime(display_format)

    return ColSpec(
        attr_name=attr_name,
        selector=selector,
        display_name=display_name,
        display_fn=display_fn,
        column_width=column_width,
        type=ColSpecType.Date,
        hidden=hidden,
        alignment=alignment,
        on_click=None,
        enable_when=None,
        values=None,
        on_value_changed=None,
    )


def decimal_col(
    *,
    display_name: str,
    attr_name: str | None = None,
    selector: typing.Callable[[Row], decimal.Decimal] | None = None,
    display_format: str = ",.2f",
    column_width: int | None = 100,
    hidden: bool = False,
    alignment: ColAlignment = ColAlignment.Right,
) -> ColSpec[Row, decimal.Decimal]:
    return ColSpec(
        attr_name=attr_name,
        selector=selector,
        display_name=display_name,
        display_fn=lambda v: "" if v is None else ("{0:" + display_format + "}").format(v),
        type=ColSpecType.Decimal,
        column_width=column_width,
        hidden=hidden,
        alignment=alignment,
        on_click=None,
        enable_when=None,
        values=None,
        on_value_changed=None,
    )


def dropdown_col(
    *,
    display_name: str,
    values: dict[Value, str],
    on_value_changed: typing.Callable[[Value], None],
    attr_name: str | None = None,
    selector: typing.Callable[[Row], decimal.Decimal] | None = None,
    column_width: int = 100,
    alignment: ColAlignment = ColAlignment.Center,
    enable_when: typing.Callable[[Row], bool] | None = None,
) -> ColSpec[Row, Value]:
    return ColSpec(
        attr_name=attr_name,
        selector=selector,
        display_name=display_name,
        display_fn=str,
        column_width=column_width,
        type=ColSpecType.Dropdown,
        hidden=False,
        alignment=alignment,
        on_click=None,
        enable_when=enable_when,
        values=values,
        on_value_changed=on_value_changed,
    )


def float_col(
    *,
    display_name: str,
    attr_name: str | None = None,
    selector: typing.Callable[[Row], float] | None = None,
    display_format: str = ",.2f",
    column_width: int | None = 100,
    hidden: bool = False,
    alignment: ColAlignment = ColAlignment.Right,
) -> ColSpec[Row, float]:
    return ColSpec(
        attr_name=attr_name,
        selector=selector,
        display_name=display_name,
        display_fn=lambda v: "" if v is None else ("{0:" + display_format + "}").format(v),
        type=ColSpecType.Float,
        column_width=column_width,
        hidden=hidden,
        alignment=alignment,
        on_click=None,
        enable_when=None,
        values=None,
        on_value_changed=None,
    )


def int_col(
    *,
    display_name: str,
    attr_name: str | None = None,
    selector: typing.Callable[[Row], int] | None = None,
    display_format: str = ",.0f",
    column_width: int | None = 100,
    hidden: bool = False,
    alignment: ColAlignment = ColAlignment.Right,
) -> ColSpec[Row, int]:
    return ColSpec(
        attr_name=attr_name,
        selector=selector,
        display_name=display_name,
        display_fn=lambda v: "" if v is None else ("{0:" + display_format + "}").format(v),
        type=ColSpecType.Int,
        column_width=column_width,
        hidden=hidden,
        alignment=alignment,
        on_click=None,
        enable_when=None,
        values=None,
        on_value_changed=None,
    )


def text_col(
    *,
    display_name: str,
    attr_name: str | None = None,
    selector: typing.Callable[[Row], str] | None = None,
    column_width: int | None = None,
    hidden: bool = False,
    alignment: ColAlignment = ColAlignment.Left,
) -> ColSpec[Row, str]:
    return ColSpec(
        attr_name=attr_name,
        selector=selector,
        display_name=display_name,
        display_fn=str,
        type=ColSpecType.Text,
        column_width=column_width,
        hidden=hidden,
        alignment=alignment,
        on_click=None,
        enable_when=None,
        values=None,
        on_value_changed=None,
    )


def timestamp_col(
    *,
    display_name: str,
    attr_name: str | None = None,
    selector: typing.Callable[[Row], datetime.datetime] | None = None,
    display_format: str = "%m/%d/%y %I:%M:%S %p",
    column_width: int | None = 200,
    hidden: bool = False,
    alignment: ColAlignment = ColAlignment.Right,
    display_fn: typing.Callable[[datetime.date], str] | None = None,
) -> ColSpec[Row, datetime.datetime]:
    if display_fn is None:
        display_fn = lambda ts: "" if ts is None or ts == datetime.datetime(1900, 1, 1) else ts.strftime(display_format)

    return ColSpec(
        attr_name=attr_name,
        selector=selector,
        display_name=display_name,
        display_fn=display_fn,
        type=ColSpecType.Timestamp,
        column_width=column_width,
        hidden=hidden,
        alignment=alignment,
        on_click=None,
        enable_when=None,
        values=None,
        on_value_changed=None,
    )


@dataclasses.dataclass(frozen=True)
class TableSpec(typing.Generic[Row]):
    col_specs: list[ColSpec[Row, typing.Any]]
    key_attr: str


class Table(typing.Generic[Row, Key], qtw.QWidget):
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

        self._table = qtw.QTableWidget()
        self._table.setAlternatingRowColors(True)
        self._table.setWordWrap(True)
        self._table.setColumnCount(len(headers))
        self._table.setHorizontalHeaderLabels(headers)
        self._table.setSortingEnabled(True)

        for col_num, col_spec in enumerate(self._spec.col_specs):
            if col_spec.hidden:
                self._table.setColumnHidden(col_num, True)

            if col_spec.column_width is not None:
                self._table.setColumnWidth(col_num, col_spec.column_width)

        layout = qtw.QVBoxLayout()
        layout.addWidget(self._table)

        self.setLayout(layout)

        self._items: dict[Key, Row] = {}

    def add_item(self, /, item: Row) -> None:
        key = getattr(item, self._spec.key_attr)
        self._items[key] = item
        self._table.setRowCount(self.rowCount() + 1)
        self._set_row(row_num=self.rowCount(), data=item)

    def clear_selection(self) -> None:
        self._table.clearSelection()

    def delete_item(self, *, key: Key) -> None:
        del self._items[key]

        row_num = self._get_row_num_for_key(key=key)
        if row_num is not None:
            self._table.removeRow(row_num)

    @property
    def items(self) -> list[Row]:
        return list(self._items.values())

    @property
    def selected_item(self) -> Row | None:
        if indices := self._table.selectedIndexes():
            row_num = indices[0].row()
            key = self._table.item(row_num, self._col_indices[self._spec.key_attr]).data(qtc.Qt.EditRole)
            return self._items[key]
        return None

    def select_item_by_key(self, *, key: Key) -> None:
        row_num = self._get_row_num_for_key(key=key)
        if row_num is not None:
            self._table.selectRow(row_num)

    def set_all(self, /, data: list[Row]) -> None:
        self._items = {
            getattr(row, self._spec.key_attr): row
            for row in data
        }

        self._table.clearContents()
        self._table.setRowCount(len(data))

        self._table.setSortingEnabled(False)
        try:
            for row_num, row in enumerate(data):
                self._set_row(row_num=row_num, data=row)
        finally:
            self._table.setSortingEnabled(True)

    def update_item(self, /, item: Row) -> None:
        row_num = self._get_row_num_for_key(key=getattr(item, self._spec.key_attr))
        if row_num is not None:
            self._set_row(row_num=row_num, data=item)

    def _get_row_num_for_key(self, *, key: Key) -> int | None:
        for row_num in range(self._table.rowCount()):
            if key == self._table.item(row_num, self._col_indices[self._spec.key_attr]).data(qtc.Qt.EditRole):
                return row_num
        return None

    def _set_row(self, *, row_num: int, data: Row) -> None:
        for col_num, col_spec in enumerate(self._spec.col_specs):
            if col_spec.type in (
                ColSpecType.Date,
                ColSpecType.Decimal,
                ColSpecType.Float,
                ColSpecType.Int,
                ColSpecType.Text,
                ColSpecType.Timestamp,
            ):
                if col_spec.selector is None:
                    if col_spec.attr_name is None:
                        raise Exception("If a [selector] is not provided, then [attr_name] is required.")
                    value = getattr(data, col_spec.attr_name)
                else:
                    value = col_spec.selector(data)
                display_value = col_spec.display_fn(value)  # type: ignore
                item = TableItem(value=value, display_value=display_value)
                item.setTextAlignment(col_spec.alignment.qt_alignment)
                self._table.setItem(row_num, col_num, item)
            elif col_spec.type == ColSpecType.Button:
                if col_spec.on_click is None:
                    raise Exception("[on_click] is required for a Button column.")
                else:
                    btn = qtw.QPushButton(col_spec.display_name)
                    assert col_spec.column_width is not None
                    btn.setFixedWidth(col_spec.column_width - 6)
                    btn.clicked.connect(col_spec.on_click)
                    self._table.setCellWidget(row_num, col_num, btn)

                if col_spec.enable_when is not None:
                    btn.setEnabled(col_spec.enable_when(data))
            elif col_spec.type == ColSpecType.Dropdown:
                if col_spec.on_value_changed is None:
                    raise Exception("[on_value_changed] is required for a Dropdown column.")

                if col_spec.values is None:
                    raise Exception("[values] is required for a Dropdown column.")

                if col_spec.selector is None:
                    if col_spec.attr_name is None:
                        raise Exception("If a [selector] is not provided, then [attr_name] is required.")
                    value = getattr(data, col_spec.attr_name)
                else:
                    value = col_spec.selector(data)

                cbo = qtw.QComboBox()
                for ix, (v, display_value) in enumerate(col_spec.values.items()):
                    cbo.addItem(display_value, v)
                    if value == v:
                        cbo.setCurrentIndex(ix)

                assert col_spec.column_width is not None
                cbo.setFixedWidth(col_spec.column_width - 6)

                cbo.currentIndexChanged.connect(lambda _: col_spec.on_value_changed(cbo.currentData()))  # type: ignore
                self._table.setCellWidget(row_num, col_num, cbo)

                if col_spec.enable_when is not None:
                    cbo.setEnabled(col_spec.enable_when(data))
            else:
                raise Exception(f"Unrecognized ColSpecType: {col_spec.type!r}.")

            if col_spec.column_width is None:
                self._table.resizeColumnToContents(col_num)
            else:
                self._table.setColumnWidth(col_num, col_spec.column_width)

        self._table.resizeRowsToContents()


class TableItem(qtw.QTableWidgetItem):
    def __init__(self, value: typing.Any, display_value: str):
        super().__init__(display_value)

        self._value = value

        # noinspection PyTypeChecker
        self.setFlags(qtc.Qt.ItemIsSelectable | qtc.Qt.ItemIsEnabled)  # type: ignore

    def __lt__(self, other: object) -> bool:
        assert isinstance(other, TableItem)

        if self._value is None and other is None:
            return False

        if self._value is None:
            return True

        if other._value is None:
            return False

        return self._value < other._value
