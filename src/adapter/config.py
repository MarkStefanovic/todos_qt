import functools
import json
import os
import pathlib
import typing

from src.adapter import fs

__all__ = (
    "add_holidays",
    "current_user",
    "db_schema",
    "db_url",
)


@functools.lru_cache
def _config(*, path: pathlib.Path = fs.config_path()) -> dict[str, typing.Any]:
    with path.open("r") as fh:
        return json.load(fh)


def add_holidays(*, config_path: pathlib.Path = fs.config_path()) -> bool:
    return _config(path=config_path)["add-holidays"]


def current_user(*, config_path: pathlib.Path = fs.config_path()) -> str:
    username = _config(path=config_path).get("current-user")
    if username:
        return username
    return os.environ.get("USERNAME", "anonymous")


def db_schema(*, config_path: pathlib.Path = fs.config_path()) -> str | None:
    return _config(path=config_path)["db-schema"]


def db_url(*, secrets_path: pathlib.Path = fs.secrets_path(), assets_folder: pathlib.Path = fs.assets_folder()) -> str:
    url = _config(path=secrets_path)["sqlalchemy-connection-string"]
    if url:
        return url

    full_db_path = assets_folder / "todo.db"
    return f"sqlite:///{full_db_path.resolve()!s}"


if __name__ == '__main__':
    print(_config())