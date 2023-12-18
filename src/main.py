import sys
import types
import typing

# noinspection PyPep8Naming
from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa: F401
from loguru import logger

from src import adapter, domain, presentation, service
from src.adapter import config

__all__ = ("main",)


@logger.catch
def main() -> None | domain.Error:
    log_folder = adapter.fs.root_dir() / "logs"
    log_folder.mkdir(exist_ok=True)

    logger.add(log_folder / "error.log", rotation="5 MB", retention="7 days", level="ERROR")
    # logger.add(sys.stderr, format="{time} {level} {message}", level="DEBUG")

    except_hook = sys.excepthook

    # noinspection SpellCheckingInspection
    def exception_hook(
        exctype: typing.Type[BaseException],
        value: BaseException,
        traceback: types.TracebackType | None,
    ) -> None:
        logger.exception(value)
        except_hook(exctype, value, traceback)
        sys.exit(1)

    # noinspection SpellCheckingInspection
    sys.excepthook = exception_hook

    app = qtw.QApplication(sys.argv)

    presentation.theme.apply_theme(app=app)

    engine = adapter.db.create_engine(url=adapter.config.db_url(), echo=True)
    if isinstance(engine, domain.Error):
        return engine

    username: typing.Final[str] = config.current_user()

    category_service = service.CategoryService(engine=engine)

    user_service: typing.Final[service.UserService] = service.UserService(
        engine=engine,
        username=username,
    )

    current_user = user_service.get_current_user()

    todo_service = service.TodoService(engine=engine, username=username)

    app_icon = presentation.icons.app_icon()
    if isinstance(app_icon, domain.Error):
        return app_icon

    main_view = presentation.MainWidget(
        window_icon=app_icon,
        current_user=current_user,
        category_service=category_service,
        todo_service=todo_service,
        user_service=user_service,
    )

    app.setWindowIcon(app_icon)

    # screen = app.desktop().screenGeometry()
    # if screen.width() >= 2050:
    #     width = 2050
    #     main_view.setGeometry(0, 0, width, screen.height())
    #     main_view.show()
    # else:
    #     main_view.showFullScreen()
    #     main_view.showMaximized()

    main_view.showFullScreen()
    main_view.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
