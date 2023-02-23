from __future__ import annotations

import os
import sys
import types
import typing

from loguru import logger
from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw

from src import adapter, domain, presentation, service

__all__ = ("main",)


def cobalt() -> qtg.QPalette:
    base_color = qtg.QColor(15, 15, 25)
    alternate_color = qtg.QColor(35, 35, 50)
    tooltip_background_color = qtg.QColor(25, 25, 25)
    link_color = qtg.QColor(42, 130, 218)
    highlight_background_color = qtg.QColor(42, 130, 218)

    color_lkp = {
        (qtg.QPalette.Window,): alternate_color,
        (qtg.QPalette.WindowText,): qtc.Qt.white,
        (qtg.QPalette.Base,): base_color,
        (qtg.QPalette.AlternateBase,): alternate_color,
        (qtg.QPalette.ToolTipBase,): tooltip_background_color,
        (qtg.QPalette.ToolTipText,): qtc.Qt.white,
        (qtg.QPalette.Text,): qtc.Qt.white,
        (qtg.QPalette.Button,): alternate_color,
        (qtg.QPalette.ButtonText,): qtc.Qt.white,
        (qtg.QPalette.BrightText,): qtc.Qt.red,
        (qtg.QPalette.Link,): link_color,
        (qtg.QPalette.Highlight,): highlight_background_color,
        (qtg.QPalette.HighlightedText,): base_color,
        (qtg.QPalette.Active, qtg.QPalette.Button): alternate_color,
        (qtg.QPalette.Disabled, qtg.QPalette.ButtonText): qtc.Qt.darkGray,
        (qtg.QPalette.Disabled, qtg.QPalette.WindowText): qtc.Qt.darkGray,
        (qtg.QPalette.Disabled, qtg.QPalette.Text): qtc.Qt.darkGray,
        (qtg.QPalette.Disabled, qtg.QPalette.Light): alternate_color,
    }

    palette = qtg.QPalette()
    for selector, color in color_lkp.items():
        palette.setColor(*selector, color)  # type: ignore

    return palette


@logger.catch
def main() -> None:
    log_folder = adapter.fs.root_dir() / "logs"
    log_folder.mkdir(exist_ok=True)

    logger.add(log_folder / "error.log", rotation="5 MB", retention="7 days", level="ERROR")
    # logger.add(sys.stderr, format="{time} {level} {message}", level="DEBUG")

    except_hook = sys.excepthook

    def exception_hook(
        exctype: typing.Type[BaseException],
        value: BaseException,
        traceback: types.TracebackType | None,
    ) -> None:
        logger.exception(value)
        except_hook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook

    app = qtw.QApplication(sys.argv)

    app.setStyle("Fusion")

    app.setStyleSheet("""
        QWidget { font-size: 11pt; }
        QHeaderView { font-weight: bold; }
        QPushButton { font-weight: "bold"; }
        QPushButton:hover:!pressed { background-color: rgb(80, 80, 140); }
        QPushButton:!hover { background-color: rgb(60, 60, 80); }
        QTabBar::tab:selected { 
            background: rgb(80, 80, 100);
            border: 1px solid rgb(140, 140, 180); 
            border-bottom-color: none; 
            border-top-left-radius: 1px;
            border-top-right-radius: 1px;
            min-width: 60px;
            padding: 4px;
        }
        QTabBar::tab:hover { background: rgb(100, 100, 140); }
        QPushButton#table_btn { background-color: none; border: none; }
        QPushButton#table_btn:enabled { color: cyan; }
        QPushButton#table_btn:disabled { color: none; }
        QPushButton#table_btn:hover:!pressed { background-color: rgb(80, 80, 140); }
        QPushButton#table_btn:!hover { background-color: none; }
    """)

    app.setPalette(cobalt())

    app_icon = qtg.QIcon(str((adapter.fs.assets_folder() / "icons" / "app.png").resolve()))

    engine = adapter.db.create_engine(url=adapter.config.db_url(), echo=True)

    username = os.environ.get("USERNAME", "unknown").lower()

    category_service = service.CategoryService(engine=engine)

    user_service = service.UserService(engine=engine, username=username)
    user_service.add_admins()

    todo_service = service.TodoService(engine=engine, username=username)
    # todo_service.cleanup()

    if adapter.config.add_holidays():
        for category in (domain.TODO_CATEGORY, domain.HOLIDAY_CATEGORY):
            if category_service.get(category_id=category.category_id) is None:
                category_service.add(category=category)
    else:
        if category_service.get(category_id=domain.TODO_CATEGORY.category_id) is None:
            category_service.add(category=domain.TODO_CATEGORY)

    if adapter.config.add_holidays():
        todo_service.add_default_holidays_for_all_users()

    main_view = presentation.MainView(window_icon=app_icon)

    app.setWindowIcon(app_icon)

    todo_controller = presentation.TodoController(
        category_service=category_service,
        todo_service=todo_service,
        user_service=user_service,
        view=main_view.todos,
    )

    category_controller = presentation.CategoryController(
        category_service=category_service,
        user_service=user_service,
        view=main_view.categories,
    )

    user_controller = presentation.UserController(
        user_service=user_service,
        view=main_view.users,
    )

    if user_service.current_user():
        todo_controller.show_current_user_todos()
    else:
        todo_controller.show_current_todos()

    screen = app.desktop().screenGeometry()
    if screen.width() >= 2050:
        width = 2050
        main_view.setGeometry(0, 0, width, screen.height())
        main_view.show()
    else:
        main_view.showFullScreen()
        main_view.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
