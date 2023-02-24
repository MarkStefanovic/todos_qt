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
def _config() -> dict[str, typing.Any]:
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    path = os.path.abspath(os.path.join(bundle_dir, 'config.json'))
    with open(path, "r") as fh:
        return json.load(fh)


def add_holidays() -> bool:
    return _config()["add-holidays"]


def admin_usernames() -> list[str]:
    return _config()["admin-usernames"]


def db_schema() -> str | None:
    return _config()["db-schema"]


def db_url(*, json_config_path: pathlib.Path = fs.get_config_path()) -> str:
    return _config()["sqlalchemy-connection-string"]
