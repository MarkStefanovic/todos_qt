from __future__ import annotations

import qdarkgraystyle
from PyQt5 import QtWidgets as qtw

from src import service, domain
from src.presentation.todo import todo_list_view

__all__ = ("MainView",)


class MainView(qtw.QMainWindow):
    def __init__(
        self,
        /,
        todo_service: service.TodoService,
    ):
        super().__init__()

        self.setWindowTitle("Todos")
        # self.setWindowIcon(qtg.QIcon("home.png"))
        # self.setGeometry(500, 200, 300, 250)
        self.resize(800, 400)
        self.setStyleSheet(qdarkgraystyle.load_stylesheet())

        self._todo_view = todo_list_view.TodoListView(
            todo_service=todo_service, category=domain.TodoCategory.Todo
        )
        self._reminder_view = todo_list_view.TodoListView(
            todo_service=todo_service, category=domain.TodoCategory.Reminder
        )

        self._tabs = qtw.QTabWidget()
        self._tabs.addTab(self._todo_view, "Todos")
        self._tabs.addTab(self._reminder_view, "Reminders")

        # layout = qtw.QHBoxLayout()
        # stack = qtw.QStackedWidget()
        # stack.addWidget(self._todo_view)
        # stack.addWidget(self._reminder_view)

        # layout = qtw.QHBoxLayout()
        # layout.addWidget(self.table_view)
        # self.setLayout(layout)

        self.setCentralWidget(self._tabs)

        # menu = self.menuBar()
        # file_menu = menu.addMenu("File")
        # file_menu.addAction("Open", self.select_file)
        # file_menu.addAction("Save", self.save)
        # edit_menu = menu.addMenu("Edit")
        # edit_menu.addAction("Insert Above", self.insert_above)
        # edit_menu.addAction("Insert Below", self.insert_below)
        # edit_menu.addAction("Remove Row(s)", self.remove_rows)

    # def save(self) -> None:
    #     if self.model:
    #         self.model.save_data()
