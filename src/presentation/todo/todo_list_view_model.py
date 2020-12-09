import datetime
import typing

from PyQt5 import QtCore as qtc

from src import service, domain

__all__ = ("TableListViewModel",)


class TableListViewModel(qtc.QAbstractTableModel):
    def __init__(
        self, todo_service: service.TodoService, category: domain.TodoCategory
    ):
        super().__init__()

        self._todo_service = todo_service
        self._category = category

        self._header = [
            "id",
            "Description",
            "Frequency",
            "Days",
            "Day",
            "Due",
            "Completed",
        ]
        self._data = self.fetch_data()

    def fetch_data(self) -> typing.List[typing.List[typing.Any]]:
        if self._category == domain.TodoCategory.Todo:
            rows = self._todo_service.current_todos(datetime.date.today())
        else:
            rows = self._todo_service.current_reminders(datetime.date.today())
        return [
            [
                row.todo_id,
                row.description,
                str(row.frequency),
                str(row.days_until()),
                row.current_date().strftime("%a"),
                row.current_date().strftime("%Y-%m-%d"),
                row.date_completed.strftime("%Y-%m-%d") if row.date_completed else "",
            ]
            for row in rows
        ]

    def columnCount(self, parent: qtc.QModelIndex = qtc.QModelIndex()) -> int:
        return len(self._header)

    def data(self, index: qtc.QModelIndex, role: int = qtc.Qt.EditRole) -> typing.Any:
        # if not index.isValid():
        #     return None
        # elif role != Qt.DisplayRole:
        #     return None
        # return self.mylist[index.row()][index.column()]

        if role == qtc.Qt.DisplayRole:
            value = self._data[index.row()][index.column()]
            if isinstance(value, datetime.date):
                return value.strftime("%Y-%m-%d")
            else:
                return value

        # if role == qtc.Qt.DecorationRole:
        #     value = self._data[index.row()][index.column()]
        # if isinstance(value, datetime):
        #     return QtGui.QIcon('calendar.png')

    def delete(self, /, todo_id: int) -> None:
        row_num = get_row_number_by_id(rows=self._data, todo_id=todo_id)
        self._todo_service.delete_todo(todo_id)
        self.removeRows(row_num, 1)

    def flags(self, index: qtc.QModelIndex) -> qtc.Qt.ItemFlags:
        return super().flags(index) | qtc.Qt.ItemIsEditable  # type: ignore

    def get_row_by_id(self, /, todo_id: int) -> typing.List[typing.Any]:
        print(f"{todo_id=!r}")
        return next(row for row in self._data if row[0] == todo_id)

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

    def mark_complete(self, /, todo_id: int) -> None:
        row_num = get_row_number_by_id(rows=self._data, todo_id=todo_id)
        self._todo_service.mark_complete(todo_id)
        self.removeRows(row_num, 1)

    def refresh(self) -> None:
        self.beginResetModel()
        self._data = self.fetch_data()
        self.endResetModel()

        # old_rows = len(self._data)
        # new_rows = len(self._data)
        #
        # if old_rows > new_rows:
        #     self.beginRemoveRows()
        # self.insertRows(0, len(self._data))
        # for row, _ in enumerate(self._data):
        #     for col, _ in enumerate(self._header):
        #         ix = self.createIndex(row, col)
        #         self.begin
        #         self.dataChanged.emit(ix, ix, [qtc.Qt.DisplayRole])

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


def get_row_number_by_id(
    *, rows: typing.List[typing.List[typing.Any]], todo_id: int
) -> int:
    return next(row_num for row_num, row in enumerate(rows) if row[0] == todo_id)
