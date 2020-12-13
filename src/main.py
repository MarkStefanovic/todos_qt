import functools
import pathlib
import sys
import traceback
import types
import typing

from PyQt5 import QtWidgets as qtw
from loguru import logger

import src.adapter.sqlite_db
from src import adapter, service, presentation

all = ("main",)


def exception_hook(
    original_exception_hook: typing.Callable[
        [
            typing.Optional[typing.Type[BaseException]],
            typing.Optional[BaseException],
            typing.Optional[types.TracebackType],
        ],
        bool,
    ],
    db: typing.Optional[src.adapter.sqlite_db.SqliteDb],
    exc_type: typing.Optional[typing.Type[BaseException]],
    exc_val: typing.Optional[BaseException],
    exc_tb: typing.Optional[types.TracebackType],
) -> None:
    if db is not None:
        db.__exit__(exc_type, exc_val, exc_tb)
    logger.error(f"EXCEPTION: {exc_val}")
    tb = "TRACEBACK:\n" + "\n".join(traceback.format_tb(exc_tb))
    logger.error(tb)
    original_exception_hook(exc_type, exc_val, exc_tb)
    sys.exit(1)


@logger.catch
def main() -> None:
    config = adapter.EnvironConfig()
    error_log_fp = config.log_dir() / "error.log"
    logger.add(
        error_log_fp,
        # format="{time} {level} {message}",
        rotation="5 MB",
        retention="7 days",
        level="ERROR",
    )
    logger.info(f"Logging errors to {error_log_fp!s}.")
    logger.info("Starting Todo app.")

    db_path = pathlib.Path(config.db_path())
    with src.adapter.sqlite_db.SqliteDb(db_path) as db:
        uow = adapter.DefaultTodoUnitOfWork(db)
        todo_service = service.TodoService(uow)

        # workaround for PyQt exceptions somehow bypassing outer context manager's __exit__ methods
        original_except_hook = sys.excepthook
        sys.excepthook = functools.partial(exception_hook, original_except_hook, db)

        app = qtw.QApplication(sys.argv)
        window = presentation.MainView(todo_service)
        window.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    main()
