import dataclasses
import functools
import typing

from PyQt6 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa

from src.presentation.shared.theme import font
from src.presentation.shared.widgets.table_view.attr import Attr, Value
from src.presentation.shared.widgets.table_view.button_delegate import ButtonDelegate
from src.presentation.shared.widgets.table_view.item import Item
from src.presentation.shared.widgets.table_view.key import Key
from src.presentation.shared.widgets.table_view.model import TableViewModel

__all__ = (
    "ButtonClickedEvent",
    "DoubleClickEvent",
    "TableView",
)


@dataclasses.dataclass(frozen=True, kw_only=True)
class ButtonClickedEvent(typing.Generic[Item, Value]):
    attr: Attr[Item, Value]
    item: Item


@dataclasses.dataclass(frozen=True, kw_only=True)
class DoubleClickEvent(typing.Generic[Item, Value]):
    attr: Attr[Item, Value]
    item: Item


class TableView(qtw.QTableView, typing.Generic[Item, Key]):
    button_clicked = qtc.pyqtSignal(ButtonClickedEvent)
    double_click = qtc.pyqtSignal(DoubleClickEvent)

    def __init__(
        self,
        *,
        attrs: typing.Iterable[Attr[typing.Any, typing.Any]],
        parent: qtw.QWidget | None,
        date_format: str = "%m/%d/%Y",
        datetime_format: str = "%m/%d/%Y %I:%M %p",
    ):
        super().__init__(parent=parent)

        self._attrs: typing.Final[tuple[Attr[typing.Any, typing.Any], ...]] = tuple(attrs)
        self._date_format: typing.Final[str] = date_format
        self._datetime_format: typing.Final[str] = datetime_format

        self._font_metrics = font.DEFAULT_FONT_METRICS

        self._key_attr_name: typing.Final[str] = next(attr.name for attr in self._attrs if attr.key)

        self._view_model: typing.Final[TableViewModel[Item]] = TableViewModel(
            parent=self,
            attrs=self._attrs,
            date_format=self._date_format,
            datetime_format=self._datetime_format,
        )

        self._key_col: typing.Final[int] = self._view_model.get_column_number_for_attr_name(
            self._key_attr_name
        )

        self.setModel(self._view_model)

        for attr in self._attrs:
            if attr.data_type == "button":
                if attr.value_selector is None:
                    btn_txt_selector: typing.Callable[[qtc.QModelIndex], str] | None = None
                else:
                    btn_txt_selector = functools.partial(
                        self._button_text_selector,
                        attr_button_text_selector=attr.value_selector,
                    )

                if attr.enabled_selector is None:
                    btn_enabled_selector: typing.Callable[[qtc.QModelIndex], bool] | None = None
                else:
                    btn_enabled_selector = functools.partial(
                        self._button_enabled_selector,
                        attr_button_enabled_selector=attr.enabled_selector,
                    )

                btn_delegate = ButtonDelegate(
                    text=attr.display_name,
                    button_text_selector=btn_txt_selector,
                    enabled_selector=btn_enabled_selector,
                    icon=attr.icon,
                    parent=self,
                )

                col_num = self._view_model.get_column_number_for_attr_name(attr.name)

                self.setItemDelegateForColumn(col_num, btn_delegate)

        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)
        self.setColumnHidden(self._key_col, True)
        self.setMouseTracking(True)
        self.setWordWrap(True)

        for col_num, attr in enumerate(self._attrs):
            if attr.width is None:
                if attr.data_type == "date":
                    col_width = self._font_metrics.boundingRect("  88/88/8888  ").width()
                else:
                    col_width = self._font_metrics.boundingRect(
                        attr.display_name + "33333333"
                    ).width()
            else:
                col_width = attr.width

            if header := self.horizontalHeader():
                header.resizeSection(col_num, col_width)

        if header := self.horizontalHeader():
            header.setDefaultAlignment(
                qtc.Qt.AlignmentFlag.AlignHCenter | qtc.Qt.AlignmentFlag.AlignBottom
                # | qtg.QTextOption.WrapMode.WordWrap.value
            )
            header.setMinimumHeight(font.BOLD_FONT_METRICS.height() + 8)
            # self.horizontalHeader().setSectionResizeMode(
            #     qtw.QHeaderView.ResizeMode.ResizeToContents
            # )
            header.setMaximumSectionSize(400)
            header.setMaximumHeight(self._font_metrics.height() * 2 + 8)

        if vertical_header := self.verticalHeader():
            # header.setDefaultAlignment(
            #     qtc.Qt.AlignmentFlag.AlignTop | qtc.Qt.AlignmentFlag.AlignLeft
            # )
            #     # display at most 5 lines
            vertical_header.setMaximumSectionSize(self._font_metrics.height() * 5 + 8)
            # vertical_header.setSectionResizeMode(qtw.QHeaderView.ResizeMode.Fixed)
            # vertical_header.setTextElideMode(qtc.Qt.TextElideMode.ElideRight)

        # noinspection PyUnresolvedReferences
        self.clicked.connect(self._on_click)
        # noinspection PyUnresolvedReferences
        self.doubleClicked.connect(lambda ix: self._on_double_click(index=ix))
        # self.selectionModel().selectionChanged.connect(self._on_selection_changed)

        self._view_model.layoutChanged.connect(lambda: self.resizeRowsToContents())
        self._view_model.layoutChanged.connect(lambda: self.resizeColumnsToContents())

    @property
    def items(self) -> list[Item]:
        return self._view_model.items

    def add_item(self, /, item: Item) -> None:
        self._view_model.add_item(item)

    def clear_highlight(self, *keys: Key) -> None:
        row_nums: list[int] = []
        for key in keys:
            row_num = self._view_model.get_row_num_for_key(str(key))
            if row_num is not None:
                row_nums.append(row_num)

        self._view_model.clear_highlight(*row_nums)

    def clear_highlights(self) -> None:
        self._view_model.clear_highlights()

    def clear_selection(self) -> None:
        if model := self.selectionModel():
            model.clear()

    def delete_item(self, *, key: Key) -> None:
        self._view_model.delete_item(key=str(key))

    def get_item(self, *, key: Key) -> Item | None:
        return self._view_model.get_item(key=str(key))

    def highlight_row(self, *keys: Key) -> None:
        keys_to_highlight = {str(key) for key in keys}
        return self._view_model.highlight_row(*keys_to_highlight)

    def select_item_by_key(self, /, key: Key) -> None:
        if model := self.model():
            for row_num in range(model.rowCount()):
                index = model.index(row_num, self._key_col)
                model_key = model.data(index)
                if model_key == key:
                    if selection_model := self.selectionModel():
                        selection_model.select(index, qtc.QItemSelectionModel.SelectionFlag.Rows)

                    return None

    @property
    def selected_item(self) -> Item | None:
        if selection_model := self.selectionModel():
            if indices := selection_model.selectedIndexes():
                row_num = indices[0].row()
                if model := self.model():
                    key = model.data(model.index(row_num, self._key_col))
                    return self.get_item(key=key)

        return None

    def set_items(self, /, items: typing.Iterable[Item]) -> None:
        self._view_model.set_items(items)

    def update_item(self, /, item: Item) -> None:
        self._view_model.update_item(item)

    def _button_enabled_selector(
        self,
        attr_button_enabled_selector: typing.Callable[[Item], bool],
        index: qtc.QModelIndex,
    ) -> bool:
        if model := self.model():
            key = model.data(model.index(index.row(), self._key_col))

            if isinstance(key, qtc.QVariant):
                key = str(key.value())
            else:
                key = str(key)

            if key is None:
                return False

            item = self.get_item(key=key)

            if item is None:
                return False

            return attr_button_enabled_selector(item)

        return False

    def _button_text_selector(
        self,
        attr_button_text_selector: typing.Callable[[Item], str],
        index: qtc.QModelIndex,
    ) -> str:
        if model := self.model():
            key = model.data(model.index(index.row(), self._key_col))

            if isinstance(key, qtc.QVariant):
                key = str(key.value())
            else:
                key = str(key)

            if key is None:
                return ""

            item = self.get_item(key=key)

            if item is None:
                return ""

            return attr_button_text_selector(item)

        return ""

    def _on_click(self, /, index: qtc.QModelIndex) -> None:
        attr = self._view_model.get_attr_for_column_number(index.column())

        if attr.data_type == "button":
            key_index = self._view_model.index(index.row(), self._key_col)
            if not key_index.isValid():
                return

            model_data = self._view_model.data(key_index)
            if isinstance(model_data, (qtc.Qt.AlignmentFlag, qtg.QBrush, qtg.QFont, qtg.QIcon)):
                return

            key = model_data.value()

            if item := self._view_model.get_item(key):
                if attr.enabled_selector is None:
                    self.button_clicked.emit(ButtonClickedEvent(attr=attr, item=item))
                else:
                    if attr.enabled_selector(item):
                        self.button_clicked.emit(ButtonClickedEvent(attr=attr, item=item))
        else:
            key_index = self._view_model.index(index.row(), self._key_col)

            model_data = self._view_model.data(key_index)
            if isinstance(model_data, (qtc.Qt.AlignmentFlag, qtg.QBrush, qtg.QFont, qtg.QIcon)):
                return

            key = model_data.value()

            self._view_model.clear_highlights()
            self._view_model.highlight_row(str(key))

    def _on_double_click(self, *, index: qtc.QModelIndex) -> None:
        attr = self._view_model.get_attr_for_column_number(index.column())

        key_index = self._view_model.index(index.row(), self._key_col)

        if not key_index.isValid():
            return

        model_data = self._view_model.data(key_index)
        if isinstance(model_data, (qtc.Qt.AlignmentFlag, qtg.QBrush, qtg.QFont, qtg.QIcon)):
            return

        key = model_data.value()
        item = self._view_model.get_item(key)
        if item:
            event = DoubleClickEvent(attr=attr, item=item)
            self.double_click.emit(event)

    # def _on_selection_changed(self, selected: qtc.QItemSelection, deselected: qtc.QItemSelection) -> None:
    #     print("_on_selection_changed")
    #     if selected:
    #         first_selection = selected[0]
    #         top_row = first_selection.top()
    #         if top_row is not None:
    #             key_index = self._view_model.index(top_row, self._key_col)
    #
    #             model_data = self._view_model.data(key_index)
    #             if isinstance(model_data, (qtc.Qt.Alignment, qtc.Qt.AlignmentFlag, qtg.QBrush, qtg.QFont, qtg.QIcon)):
    #                 return
    #
    #             key = model_data.value()
    #
    #             self._view_model.clear_highlights()
    #             self._view_model.highlight_row(key)
