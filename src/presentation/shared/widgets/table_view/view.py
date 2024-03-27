import typing

from PyQt6 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa

from src.presentation.shared.widgets.table_view.attr import Attr
from src.presentation.shared.widgets.table_view.bound_button_enabled_selector import BoundButtonEnabledSelector
from src.presentation.shared.widgets.table_view.bound_button_text_selector import BoundButtonTextSelector
from src.presentation.shared.widgets.table_view.button_delegate import ButtonDelegate
from src.presentation.shared.widgets.table_view.event import ButtonClickedEvent, DoubleClickedEvent
from src.presentation.shared.widgets.table_view.item import Item
from src.presentation.shared.widgets.table_view.key import Key
from src.presentation.shared.widgets.table_view.model import TableViewModel

__all__ = ("TableView",)


class TableView(qtw.QTableView, typing.Generic[Item, Key]):
    button_clicked = qtc.pyqtSignal(ButtonClickedEvent)
    double_clicked = qtc.pyqtSignal(DoubleClickedEvent)

    def __init__(
        self,
        *,
        attrs: typing.Iterable[Attr[typing.Any, typing.Any]],
        key_attr_name: str,
        normal_font: qtg.QFont,
        bold_font: qtg.QFont,
        parent: qtw.QWidget | None,
        date_format: str = "%m/%d/%Y",
        datetime_format: str = "%m/%d/%Y %I:%M %p",
    ):
        super().__init__(parent=parent)

        self._attrs: typing.Final[tuple[Attr[typing.Any, typing.Any], ...]] = tuple(attrs)
        self._key_attr_name: typing.Final[str] = key_attr_name
        self._normal_font: typing.Final[qtg.QFont] = normal_font
        self._bold_font: typing.Final[qtg.QFont] = bold_font
        self._date_format: typing.Final[str] = date_format
        self._datetime_format: typing.Final[str] = datetime_format

        self._view_model: typing.Final[TableViewModel[Item, Key]] = TableViewModel(
            parent=self,
            attrs=self._attrs,
            key_attr_name=key_attr_name,
            date_format=self._date_format,
            datetime_format=self._datetime_format,
        )

        self.setModel(self._view_model)

        for attr in self._attrs:
            col_num = self._view_model.get_column_number_for_attr_name(attr.name)

            if attr.hidden:
                self.setColumnHidden(col_num, True)

            if attr.data_type == "button":
                if attr.value_selector is None:
                    btn_txt_selector: BoundButtonTextSelector | None = None
                else:
                    btn_txt_selector = BoundButtonTextSelector(model=self._view_model)

                if attr.enabled_selector is None:
                    btn_enabled_selector: BoundButtonEnabledSelector | None = None
                else:
                    btn_enabled_selector = BoundButtonEnabledSelector(model=self._view_model)

                btn_delegate = ButtonDelegate(
                    text=attr.display_name,
                    button_text_selector=btn_txt_selector,
                    enabled_selector=btn_enabled_selector,
                    icon=attr.icon,
                    normal_font=self._normal_font,
                    bold_font=self._bold_font,
                    parent=self,
                )

                self.setItemDelegateForColumn(col_num, btn_delegate)

        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)
        self.setMouseTracking(True)
        self.setWordWrap(True)

        self._col_widths: typing.Final[dict[int, int]] = {}
        for col_num, attr in enumerate(self._attrs):
            if attr.width:
                col_width = attr.width
            else:
                if attr.data_type == "date":
                    col_width = qtg.QFontMetrics(self._normal_font).boundingRect("   88/88/8888   ").width()
                else:
                    col_width = qtg.QFontMetrics(self._bold_font).boundingRect(attr.display_name + "    ").width()

            self._col_widths[col_num] = col_width

        if horizontal_header := self.horizontalHeader():
            horizontal_header.setDefaultAlignment(qtc.Qt.AlignmentFlag.AlignHCenter | qtc.Qt.AlignmentFlag.AlignBottom)

        self.setCornerButtonEnabled(False)

        # noinspection PyUnresolvedReferences
        self.clicked.connect(self._on_click)
        # noinspection PyUnresolvedReferences
        self.doubleClicked.connect(lambda ix: self._on_double_click(index=ix))
        # self.selectionModel().selectionChanged.connect(self._on_selection_changed)

        self._view_model.layoutChanged.connect(self._resize_rows)

        self._resize_rows()

    @property
    def items(self) -> list[Item]:
        return self._view_model.items

    def add_item(self, /, item: Item) -> None:
        self._view_model.add_item(item)

        row = self._get_row_number_for_item(item)
        if row is not None:
            self._resize_row(row)

    def clear_selection(self) -> None:
        if model := self.selectionModel():
            model.clear()

    def delete_item(self, *, key: Key) -> None:
        self._view_model.delete_item(key=key)

    def get_item(self, *, key: Key) -> Item | None:
        return self._view_model.get_item(key=key)

    def select_item_by_key(self, /, key: Key) -> None:
        row_num = self._view_model.get_row_num_for_key(key)
        if row_num is not None:
            index = self._view_model.index(row_num, 0)
            if selection_model := self.selectionModel():
                selection_model.select(index, qtc.QItemSelectionModel.SelectionFlag.Rows)

        return None

    @property
    def selected_item(self) -> Item | None:
        if selection_model := self.selectionModel():
            if indices := selection_model.selectedIndexes():
                return self._view_model.items[indices[0].row()]

        return None

    def set_items(self, /, items: typing.Iterable[Item]) -> None:
        self._view_model.set_items(items)
        self._resize_rows()

    def update_item(self, /, item: Item) -> None:
        self._view_model.update_item(item)

        row = self._get_row_number_for_item(item)
        if row is not None:
            self._resize_row(row)

    def _get_row_number_for_item(self, /, item: Item) -> int | None:
        key = getattr(item, self._key_attr_name)

        return self._view_model.get_row_num_for_key(key)

    def _on_click(self, /, index: qtc.QModelIndex) -> None:
        attr = self._view_model.get_attr_for_column_number(index.column())

        if attr.data_type == "button":
            if attr.enabled_selector is None:
                item = self._view_model.items[index.row()]
                self.button_clicked.emit(ButtonClickedEvent(attr=attr, item=item))
            else:
                item = self._view_model.items[index.row()]
                if attr.enabled_selector(item):
                    self.button_clicked.emit(ButtonClickedEvent(attr=attr, item=item))
        # else:
        #     item = self._view_model.get_item_for_row(index.row())
        #     self.clicked.emit(ButtonClickedEvent(attr=attr, item=item))

    def _on_double_click(self, *, index: qtc.QModelIndex) -> None:
        attr = self._view_model.get_attr_for_column_number(index.column())

        item = self._view_model.items[index.row()]
        if item:
            event = DoubleClickedEvent(attr=attr, item=item)
            self.double_clicked.emit(event)

    def _resize_row(self, /, row: int) -> None:
        default_row_height = qtg.QFontMetrics(self._normal_font).height()
        self.setRowHeight(row, default_row_height)
        self.resizeRowToContents(row)
        if self.rowHeight(row) > 300:
            self.setRowHeight(row, 300)

    def _resize_rows(self) -> None:
        default_row_height = qtg.QFontMetrics(self._normal_font).height()

        for row_num in range(self._view_model.rowCount()):
            self.setRowHeight(row_num, default_row_height)

            self.resizeRowToContents(row_num)

            if self.rowHeight(row_num) > 300:
                self.setRowHeight(row_num, 300)

        if header := self.horizontalHeader():
            for col_num, col_width in self._col_widths.items():
                header.resizeSection(col_num, col_width)

        if vertical_header := self.verticalHeader():
            vertical_header.setHidden(True)
