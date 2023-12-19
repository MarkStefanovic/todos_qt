# noinspection PyPep8Naming
from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw

from src import domain
from src.presentation.category.widget import CategoryWidget
from src.presentation.todo.widget import TodoWidget
from src.presentation.user.widget import UserWidget
from src.presentation.view import MainView

__all__ = ("MainWidget",)


class MainWidget(qtw.QMainWindow):
    def __init__(
        self,
        *,
        window_icon: qtg.QIcon,
        current_user: domain.User,
        category_service: domain.CategoryService,
        todo_service: domain.TodoService,
        user_service: domain.UserService,
    ):
        super().__init__()

        self.setWindowTitle(f"Todos - {current_user.username}")

        self.setWindowIcon(window_icon)

        # noinspection PyTypeChecker
        self.setWindowFlags(
            self.windowFlags()
            | qtc.Qt.WindowMinimizeButtonHint
            | qtc.Qt.WindowMaximizeButtonHint
            | qtc.Qt.WindowSystemMenuHint
        )

        category_widget = CategoryWidget(
            category_service=category_service,
            current_user=current_user,
            parent=self,
        )

        todo_widget = TodoWidget(
            category_service=category_service,
            todo_service=todo_service,
            user_service=user_service,
            current_user=current_user,
            parent=self,
        )

        user_widget = UserWidget(
            current_user=current_user,
            user_service=user_service,
            parent=self,
        )

        self._view = MainView(
            category_widget=category_widget,
            todo_widget=todo_widget,
            user_widget=user_widget,
        )

        self.setCentralWidget(self._view)

        self._view.on_load()
