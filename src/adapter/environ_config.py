import os
import pathlib

import dotenv

from src import domain

__all__ = ("EnvironConfig",)


class EnvironConfig(domain.Config):
    def __init__(self) -> None:
        dotenv.load_dotenv(dotenv_path=dotenv.find_dotenv())

    def db_path(self) -> pathlib.Path:
        return pathlib.Path(os.environ["DB_PATH"])

    def log_dir(self) -> pathlib.Path:
        return pathlib.Path(os.environ["LOG_DIR"])
