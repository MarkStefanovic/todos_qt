import sys
import types
import typing

from loguru import logger

from src import domain
from src.main import main

if __name__ == "__main__":
    try:
        log_folder = domain.fs.root_dir() / "logs"
        log_folder.mkdir(exist_ok=True)

        logger.add(log_folder / "error.log", rotation="5 MB", retention="7 days", level="ERROR")
        # logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")

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

        full_db_path = domain.fs.assets_folder() / "todo.db"
        db_url = f"sqlite:///{full_db_path.resolve()!s}"

        result = main(
            config_file_path=domain.fs.assets_folder() / "config.json",
            db_url=db_url,
            user_is_admin=True,
        )
        if isinstance(result, domain.Error):
            logger.error(str(result))
            sys.exit(1)
    except Exception as e:
        logger.error(f"{__file__}.__main__ failed: {e!s}")

        sys.exit(1)
