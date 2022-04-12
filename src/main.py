import os
import sys
import types
import typing

from loguru import logger
from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw

from src import adapter, domain, presentation, service
from src.adapter import fs

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
        palette.setColor(*selector, color)

    return palette


@logger.catch
def main() -> None:
    config = adapter.config()

    log_folder = fs.root_dir() / "logs"
    log_folder.mkdir(exist_ok=True)

    logger.add(
        log_folder / "error.log",
        rotation="5 MB",
        retention="7 days",
        level="ERROR",
    )

    if getattr(sys, "frozen", False):
        logger.add(sys.stderr, format="{time} {level} {message}", level="DEBUG")

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

    app.setStyle("Fusion")  # type: ignore

    app.setStyleSheet("""
        QWidget { font-family: "Arial"; font-size: 11pt; }
        QPushButton { font-weight: "bold"; }
        QPushButton:hover:!pressed { background-color: rgb(80, 80, 160); }
        QPushButton:!hover { background-color: none; }
        QTabBar::tab:selected { background: rgb(80, 80, 120); }
        QTabBar::tab:hover { background: rgb(100, 100, 160); }
    """)

    app.setPalette(cobalt())

    app_icon = qtg.QIcon(str((fs.assets_folder() / "icons" / "app.png").resolve()))

    engine = adapter.db.get_engine(url=config.sqlalchemy_url, echo=True)

    username = os.environ.get("USERNAME", "unknown").lower()

    category_service = service.DbCategoryService(engine=engine)

    user_service = service.DbUserService(engine=engine, username=username)

    todo_service = service.DbTodoService(engine=engine, username=username)

    if config.add_holidays:
        for category in (domain.TODO_CATEGORY, domain.HOLIDAY_CATEGORY):
            if category_service.get(category_id=category.category_id) is None:
                category_service.add(category=category)

        for holiday in domain.HOLIDAYS:
            if todo_service.get(todo_id=holiday.todo_id) is None:
                todo_service.upsert(todo=holiday)
    else:
        if category_service.get(category_id=domain.TODO_CATEGORY.category_id) is None:
            category_service.add(category=domain.TODO_CATEGORY)

    main_view = presentation.MainView(window_icon=app_icon)

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
