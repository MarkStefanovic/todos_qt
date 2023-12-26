# noinspection PyPep8Naming
from PyQt6 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw
from loguru import logger

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

        self.setWindowTitle(f"Todos - {current_user.display_name}")

        self.setWindowIcon(window_icon)

        # noinspection PyTypeChecker
        self.setWindowFlags(
            self.windowFlags()
            | qtc.Qt.WindowType.WindowMinimizeButtonHint
            | qtc.Qt.WindowType.WindowMaximizeButtonHint
            | qtc.Qt.WindowType.WindowSystemMenuHint
        )

        self._category_widget = CategoryWidget(
            category_service=category_service,
            user_is_admin=current_user.is_admin,
            parent=self,
        )

        self._todo_widget = TodoWidget(
            category_service=category_service,
            todo_service=todo_service,
            user_service=user_service,
            current_user=current_user,
            parent=self,
        )

        self._user_widget = UserWidget(
            current_user=current_user,
            user_service=user_service,
            parent=self,
        )

        self._view = MainView(
            user_is_admin=current_user.is_admin,
            category_widget=self._category_widget,
            todo_widget=self._todo_widget,
            user_widget=self._user_widget,
        )

        self.setCentralWidget(self._view)

        self._view.on_load()

        self._category_widget.categories_updated.connect(self._on_category_widget_categories_updated)
        self._user_widget.users_updated.connect(self._on_users_widget_users_updated)

    def _on_category_widget_categories_updated(self) -> None:
        logger.debug(f"{self.__class__.__name__}._on_category_widget_categories_updated()")

        self._todo_widget.refresh_categories()

    def _on_users_widget_users_updated(self) -> None:
        logger.debug(f"{self.__class__.__name__}._on_users_widget_users_updated()")

        self._todo_widget.refresh_users()
