import abc
import datetime
import typing

from PyQt5 import QtCore as qtc


__all__ = ("ListViewModel",)


class ListViewModel(qtc.QAbstractTableModel):
    def __init__(self) -> None:
        super().__init__()

        self._data: typing.List[typing.Any] = []

    @abc.abstractmethod
    def fetch_data(self) -> typing.List[typing.List[typing.Any]]:
        raise NotImplementedError

    def columnCount(self, parent: qtc.QModelIndex = qtc.QModelIndex()) -> int:
        return len(self._header)

    def data(self, index: qtc.QModelIndex, role: int = qtc.Qt.EditRole) -> typing.Any:
        if index.isValid() and role == qtc.Qt.DisplayRole:
            value = self._data[index.row()][index.column()]
            if isinstance(value, datetime.date):
                return value.strftime("%Y-%m-%d")
            else:
                return value

    def delete(self, /, todo_id: int) -> None:
        if row_num := self.get_row_number(todo_id=todo_id):
            self.removeRows(row_num, 1)

    def flags(self, index: qtc.QModelIndex) -> qtc.Qt.ItemFlags:
        return super().flags(index) | qtc.Qt.ItemIsEditable  # type: ignore

    def get_row(self, /, todo_id: int) -> typing.Optional[typing.List[typing.Any]]:
        return next((row for row in self._data if row[0] == todo_id), None)

    def get_row_number(self, /, todo_id: int) -> typing.Optional[int]:
        return next(
            (row_num for row_num, row in enumerate(self._data) if row[0] == todo_id),
            None,
        )

    def headerData(
        self,
        section: int,
        orientation: qtc.Qt.Orientation,
        role: int = qtc.Qt.DisplayRole,
    ) -> typing.Any:
        if orientation == qtc.Qt.Horizontal and role == qtc.Qt.DisplayRole:
            return self._header[section]
        else:
            return super().headerData(section, orientation, role)

    def insertRows(
        self, row: int, count: int, parent: qtc.QModelIndex = qtc.QModelIndex()
    ) -> bool:
        self.beginInsertRows(parent or qtc.QModelIndex(), row, row + count - 1)
        for _ in range(count):
            default_row = [""] * len(self._header)
            self._data.insert(row, default_row)
        self.endInsertRows()
        return True

    def refresh(self) -> None:
        self.beginResetModel()
        self._data = self.fetch_data()
        self.endResetModel()

    def removeRows(
        self, row: int, count: int, parent: qtc.QModelIndex = qtc.QModelIndex()
    ) -> bool:
        self.beginRemoveRows(parent or qtc.QModelIndex(), row, row + count - 1)
        for _ in range(count):
            del self._data[row]
        self.endRemoveRows()
        return True

    def rowCount(self, parent: qtc.QModelIndex = qtc.QModelIndex()) -> int:
        return len(self._data)

    def setData(
        self, index: qtc.QModelIndex, value: typing.Any, role: int = qtc.Qt.EditRole
    ) -> bool:
        if index.isValid() and role == qtc.Qt.EditRole:
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, [role])
            return True
        else:
            return False

    def sort(
        self, column: int, order: qtc.Qt.SortOrder = qtc.Qt.AscendingOrder
    ) -> None:
        self.layoutAboutToBeChanged.emit()  # type: ignore
        self._data.sort(key=lambda x: x[column])
        if order == qtc.Qt.DescendingOrder:
            self._data.reverse()
        self.layoutChanged.emit()  # type: ignore
