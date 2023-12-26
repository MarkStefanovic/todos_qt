import sys
import typing

from PyQt5 import QtWidgets as qtw
from loguru import logger

from src import adapter, domain, presentation, service

__all__ = ("main",)


def main(
    *,
    db_url: str,
    user_is_admin: bool,
) -> None | domain.Error:
    # noinspection PyShadowingNames
    try:
        app = qtw.QApplication(sys.argv)

        presentation.theme.cobalt.apply_theme(app)

        engine = adapter.db.create_engine(url=db_url)
        if isinstance(engine, domain.Error):
            return engine

        create_tables_result = adapter.db.create_tables(engine=engine)
        if isinstance(create_tables_result, domain.Error):
            return create_tables_result

        username = adapter.config.current_user()
        if isinstance(username, domain.Error):
            return username

        category_service = service.CategoryService(engine=engine)

        add_default_categories_result = category_service.add_default_categories()
        if isinstance(add_default_categories_result, domain.Error):
            return add_default_categories_result

        user_service: typing.Final[service.UserService] = service.UserService(
            engine=engine,
            username=username,
            user_is_admin=user_is_admin,
        )

        current_user = user_service.get_current_user()
        if isinstance(current_user, domain.Error):
            return current_user

        todo_service = service.TodoService(engine=engine, username=username)

        app_icon = presentation.theme.icons.app_icon()
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

        main_view.showFullScreen()
        main_view.showMaximized()

        sys.exit(app.exec())
    except Exception as e:
        logger.error(f"{__file__}.main() failed: {e!s}")

        return domain.Error.new(str(e))
