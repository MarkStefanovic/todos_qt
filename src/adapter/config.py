import functools
import json
import os
import pathlib
import sys
import typing

from src.adapter import fs

__all__ = (
    "add_holidays",
    "admin_usernames",
    "db_schema",
    "db_url",
)


@functools.lru_cache
def _config(*, path: pathlib.Path = fs.config_path()) -> dict[str, typing.Any]:
    with path.open("r") as fh:
        return json.load(fh)


def add_holidays(*, config_path: pathlib.Path = fs.config_path()) -> bool:
    return _config(path=config_path)["add-holidays"]


def admin_usernames(*, config_path: pathlib.Path = fs.config_path()) -> list[str]:
    return _config(path=config_path)["admin-usernames"]


def db_schema(*, config_path: pathlib.Path = fs.config_path()) -> str | None:
    return _config(path=config_path)["db-schema"]


def db_url(*, config_path: pathlib.Path = fs.config_path()) -> str:
    return _config(path=config_path)["sqlalchemy-connection-string"]


if __name__ == '__main__':
    print(_config())
