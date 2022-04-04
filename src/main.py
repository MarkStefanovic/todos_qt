import datetime
import functools
import pathlib
import sys
import types
import typing

from loguru import logger
from PyQt5 import QtGui as qtg, QtWidgets as qtw
from qt_material import apply_stylesheet

from src import adapter, domain, presentation, service

__all__ = ("main",)


@functools.lru_cache
def root_dir() -> pathlib.Path:
    if getattr(sys, "frozen", False):
        path = pathlib.Path(getattr(sys, '_MEIPASS'))
        assert path is not None
        return path
    else:
        path = pathlib.Path(sys.argv[0]).parent.parent
        assert path.name == "todos-qt", f"Expected the parent folder to be named todos-qt, but the path was {path.resolve()!s}."
        return path


@logger.catch
def main() -> None:
    config = adapter.json_config.load(path=root_dir() / "assets" / "config.json")

    log_folder = root_dir() / "logs"
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

    app_icon = qtg.QIcon(str((root_dir() / "assets" / "icons" / "app.png").resolve()))

    engine = adapter.db.get_engine(url=config.sqlalchemy_url, echo=True)

    category_service = service.DbCategoryService(engine=engine)

    for category in (domain.TODO_CATEGORY, domain.HOLIDAY_CATEGORY):
        if not category_service.get(category_id=category.category_id):
            category_service.add(category=category)

    todo_service = service.DbTodoService(engine=engine)

    for holiday in domain.HOLIDAYS:
        if todo_service.get(todo_id=holiday.todo_id) is None:
            todo_service.upsert(todo=holiday)

    todos = todo_service.get_where(
        date_filter=datetime.date.today(),
        due_filter=True,
        description_like="",
        category_filter=presentation.ALL_CATEGORY,
    )

    categories = category_service.all()

    state = presentation.MainState(
        today=datetime.date.today(),
        active_tab="todo",
        todo_state=presentation.TodoState.initial(
            todos=todos,
            category_options=categories,
        ),
        category_state=presentation.CategoryState(
            dash_state=presentation.CategoryDashState(
                categories=categories,
                selected_category=None,
                status="",
            ),
            form_state=presentation.CategoryFormState.initial(),
            dash_active=True,
        ),
    )

    main_view = presentation.MainView(state=state, window_icon=app_icon)

    apply_stylesheet(app, theme="dark_amber.xml")

    screen = app.desktop().screenGeometry()
    if screen.width() >= 2100:
        width = 2100
    else:
        width = screen.width()
    main_view.setGeometry(0, 0, width, screen.height())

    main_view.show()

    todo_controller = presentation.TodoController(
        category_service=category_service,
        todo_service=todo_service,
        view=main_view.todos,
    )

    category_controller = presentation.CategoryController(
        category_service=category_service,
        view=main_view.categories,
    )

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
