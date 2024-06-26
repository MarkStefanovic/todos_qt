import typing
import warnings

# noinspection PyPep8Naming
from PyQt6 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw

from src.presentation.shared.widgets.table_view.attr import Attr
from src.presentation.shared.widgets.table_view.item import Item
from src.presentation.shared.widgets.table_view.key import Key

__all__ = ("TableViewModel",)


# noinspection PyPep8Naming,PyMethodMayBeStatic
class TableViewModel(qtc.QAbstractTableModel, typing.Generic[Item, Key]):
    def __init__(
        self,
        *,
        attrs: typing.Iterable[Attr[Item, typing.Any]],
        key_attr_name: str,
        parent: qtw.QWidget,
        frozen_attr_name: str | None = None,
        date_format: str = "%m/%d/%Y",
        datetime_format: str = "%m/%d/%Y %I:%M %p",
    ):
        super().__init__(parent=parent)

        self._attrs: typing.Final[tuple[Attr[Item, typing.Any], ...]] = tuple(attrs)
        self._key_attr_name: typing.Final[str] = key_attr_name

        self._frozen_attr_name: typing.Final[str | None] = frozen_attr_name
        self._date_format: typing.Final[str] = date_format
        self._datetime_format: typing.Final[str] = datetime_format

        self._column_header: typing.Final[tuple[str, ...]] = tuple(
            "" if attr.data_type == "button" else attr.display_name for attr in self._attrs
        )

        self._attr_by_col_num: typing.Final[dict[int, Attr[Item, typing.Any]]] = {
            col_num: attr for col_num, attr in enumerate(self._attrs)
        }

        self._attr_by_name: typing.Final[dict[str, Attr[Item, typing.Any]]] = {attr.name: attr for attr in self._attrs}

        self._items: list[Item] = []
        self._row_num_by_key: dict[Key, int] = {}

    @property
    def items(self) -> list[Item]:
        return self._items.copy()

    def add_item(self, /, item: Item) -> None:
        self.beginInsertRows(
            qtc.QModelIndex(),
            self.rowCount(),
            self.rowCount(),
        )
        key = getattr(item, self._key_attr_name)
        self._row_num_by_key[key] = len(self._items)
        self._items.append(item)
        self.endInsertRows()

    def columnCount(self, parent: qtc.QModelIndex = qtc.QModelIndex()) -> int:  # noqa: B008
        return len(self._column_header)

    def delete_item(self, *, key: Key) -> None:
        row_num = self._row_num_by_key.get(key)

        if row_num is None:
            warnings.warn(f"Could not find a row with the key, {key!r}.", stacklevel=1)
            return None

        self.removeRow(row_num)

    def data(
        self,
        index: qtc.QModelIndex,
        role: int = qtc.Qt.ItemDataRole.DisplayRole,
    ) -> qtc.QVariant | qtc.Qt.AlignmentFlag | qtg.QBrush | qtg.QFont | qtg.QIcon:
        if not index.isValid():
            return qtc.QVariant()

        attr = self._attr_by_col_num[index.column()]

        if attr.data_type == "button":
            if role == qtc.Qt.ItemDataRole.DecorationRole:
                if attr.icon is not None:
                    return attr.icon

            return qtc.QVariant()

        if role == qtc.Qt.ItemDataRole.TextAlignmentRole:
            match self._attr_by_name[attr.name].alignment:
                case "center":
                    return qtc.Qt.AlignmentFlag.AlignTop | qtc.Qt.AlignmentFlag.AlignHCenter
                case "left":
                    return qtc.Qt.AlignmentFlag.AlignTop | qtc.Qt.AlignmentFlag.AlignLeft
                case "right":
                    return qtc.Qt.AlignmentFlag.AlignTop | qtc.Qt.AlignmentFlag.AlignRight
                case _:
                    return qtc.Qt.AlignmentFlag.AlignTop

        if role == qtc.Qt.ItemDataRole.DisplayRole:
            item = self._items[index.row()]

            if attr.value_selector is None:
                value: typing.Any = getattr(item, attr.name)
                if value is None:
                    return qtc.QVariant()
            else:
                value = attr.value_selector(item)

            match attr.data_type:
                case "date":
                    return qtc.QVariant(value.strftime(self._date_format))
                case "datetime":
                    return qtc.QVariant(value.strftime(self._datetime_format))
                case "text":
                    return qtc.QVariant("{0}".format(value.strip(" \n\t")))
                case _:
                    return qtc.QVariant("{0}".format(value))

        # if role == qtc.Qt.FontRole:
        #     attr = self._attr_by_name[attr.name]
        # if attr.data_type == "button":
        #     return fonts.bold
        # return fonts.NORMAL

        if role == qtc.Qt.ItemDataRole.ForegroundRole:
            item = self._items[index.row()]

            if attr.color_selector is not None:
                if color := attr.color_selector(item):
                    brush = qtg.QBrush()
                    brush.setColor(color)
                    return brush

        return qtc.QVariant()

    def flags(self, index: qtc.QModelIndex) -> qtc.Qt.ItemFlag:
        return qtc.Qt.ItemFlag.ItemIsEnabled

    def get_attr_for_column_number(self, /, col_num: int) -> Attr[Item, typing.Any]:
        return self._attr_by_col_num[col_num]

    def get_column_number_for_attr_name(self, /, attr_name: str) -> int:
        try:
            return next(i for i, attr in enumerate(self._attrs) if attr.name == attr_name)
        except StopIteration as e:
            attr_names = ", ".join(attr.name for attr in self._attrs)
            raise Exception(
                f"The attr, {attr_name!r}, was not found.  Available attrs include the following: {attr_names}"
            ) from e

    def get_item(self, /, key: Key) -> Item | None:
        if self._items:
            row_num = self._row_num_by_key[key]
            return self._items[row_num]

        return None

    def get_row_num_for_key(self, /, key: Key) -> int | None:
        return self._row_num_by_key.get(key)

    def headerData(
        self,
        section: int,
        orientation: qtc.Qt.Orientation,
        role: int = qtc.Qt.ItemDataRole.DisplayRole,
    ) -> typing.Any:
        if orientation == qtc.Qt.Orientation.Horizontal and role == qtc.Qt.ItemDataRole.DisplayRole:
            return self._column_header[section]

        if orientation == qtc.Qt.Orientation.Vertical:
            if self._frozen_attr_name and role == qtc.Qt.ItemDataRole.DisplayRole:
                return str(getattr(self._items[section], self._frozen_attr_name))

            if role == qtc.Qt.ItemDataRole.TextAlignmentRole:
                return qtc.Qt.AlignmentFlag.AlignTop | qtc.Qt.AlignmentFlag.AlignLeft

        # if role == qtc.Qt.FontRole:
        #     return fonts.BOLD

    def removeRow(self, row: int, parent: qtc.QModelIndex = qtc.QModelIndex()) -> bool:  # noqa: B008
        if len(self._items) < row + 1:
            warnings.warn(
                f"Attempted to delete row {row}, but there are only {len(self._items)} items.",
                stacklevel=1,
            )
            return False

        self.beginRemoveRows(parent, row, row)

        self._items.pop(row)

        self._reindex_rows()

        self.endRemoveRows()

        return True

    def rowCount(self, parent: qtc.QModelIndex = qtc.QModelIndex()) -> int:  # noqa: B008
        return len(self._items)

    def set_items(self, /, items: typing.Iterable[Item]) -> None:
        self.layoutAboutToBeChanged.emit()

        self._items.clear()
        for item in items:
            self._items.append(item)

        self._reindex_rows()

        self.layoutChanged.emit()

    def sort(
        self,
        col: int,
        order: qtc.Qt.SortOrder = qtc.Qt.SortOrder.AscendingOrder,
    ) -> None:
        attr = self._attr_by_col_num[col]
        if attr.data_type == "button":
            return

        self.layoutAboutToBeChanged.emit()

        def key_fn(item: Item, /) -> tuple[bool, typing.Any]:
            if attr.value_selector:
                val = attr.value_selector(item)
            else:
                val = getattr(item, attr.name)

            if val is None:
                return False, None
            else:
                return True, val

        self._items = sorted(
            self._items,
            key=key_fn,
            reverse=(order == qtc.Qt.SortOrder.DescendingOrder),
        )

        self._reindex_rows()

        # self.modelReset.emit()

        self.layoutChanged.emit()

    def update_item(self, /, updated_item: Item) -> None:
        key = getattr(updated_item, self._key_attr_name)
        row_num = self._row_num_by_key[key]
        self._items[row_num] = updated_item
        last_col = len(self._column_header)
        start_index = self.index(row_num, 0)
        end_index = self.index(row_num, last_col)
        self.dataChanged.emit(start_index, end_index, [qtc.Qt.ItemDataRole.DisplayRole])

    def _reindex_rows(self) -> None:
        self._row_num_by_key.clear()
        for row_num, item in enumerate(self._items):
            key = getattr(item, self._key_attr_name)
            self._row_num_by_key[key] = row_num
