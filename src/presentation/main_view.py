from __future__ import annotations

import qdarkgraystyle
from PyQt5 import QtCore as qtc, QtWidgets as qtw

from src import service, domain
from src.presentation.todo import todo_list_view, todo_list_view_model

__all__ = ("MainView",)


class MainView(qtw.QDialog):
    def __init__(self, /, todo_service: service.TodoService):
        super().__init__()

        self.setWindowTitle("Todos")
        # self.setWindowIcon(qtg.QIcon("home.png"))
        self.setGeometry(100, 100, 1200, 500)
        self.setStyleSheet(qdarkgraystyle.load_stylesheet())
        self.setWindowFlags(
            self.windowFlags()  # type: ignore
            | qtc.Qt.WindowMinimizeButtonHint
            | qtc.Qt.WindowSystemMenuHint
        )

        todo_model = todo_list_view_model.TodoListViewModel(
            todo_service=todo_service, category=domain.TodoCategory.Todo
        )
        reminder_model = todo_list_view_model.TodoListViewModel(
            todo_service=todo_service, category=domain.TodoCategory.Reminder
        )
        self._todo_view = todo_list_view.TodoListView(todo_model)
        self._reminder_view = todo_list_view.TodoListView(reminder_model)

        self._tabs = qtw.QTabWidget()
        self._tabs.addTab(self._todo_view, "Todos")
        self._tabs.addTab(self._reminder_view, "Reminders")

        layout = qtw.QHBoxLayout()
        layout.addWidget(self._todo_view)
        layout.addWidget(self._reminder_view)

        self._todo_view.show()
        self._reminder_view.show()

        self.setLayout(layout)

        # self.setCentralWidget(self._tabs)

        # menu = self.menuBar()
        # file_menu = menu.addMenu("File")
        # file_menu.addAction("Open", self.select_file)
        # file_menu.addAction("Save", self.save)
        # edit_menu = menu.addMenu("Edit")
        # edit_menu.addAction("Insert Above", self.insert_above)
        # edit_menu.addAction("Insert Below", self.insert_below)
        # edit_menu.addAction("Remove Row(s)", self.remove_rows)
