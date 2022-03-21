import functools
import pathlib
import sys
import types
import typing

import sqlmodel as sm
from loguru import logger
from PyQt5 import QtGui as qtg, QtWidgets as qtw
from qt_material import apply_stylesheet

from src import adapter, presentation, service

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

    window = presentation.MainView(window_icon=app_icon)

    apply_stylesheet(app, theme="dark_amber.xml")

    screen = app.desktop().screenGeometry()
    if screen.width() >= 2050:
        width = 2050
    else:
        width = screen.width()
    window.setGeometry(0, 0, width, screen.height())
    window.show()

    engine = adapter.db.get_engine(url=config.sqlalchemy_url, echo=True)

    with sm.Session(engine) as session:
        todo_service = service.DbTodoService(session=session)

        sys.exit(app.exec())


if __name__ == "__main__":
    main()
