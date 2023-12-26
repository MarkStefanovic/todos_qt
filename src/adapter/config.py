import functools
import json
import os
import pathlib
import typing

from src import domain

__all__ = (
    "db_schema",
    "username",
)


@functools.lru_cache
def _config(*, config_file_path: pathlib.Path) -> dict[str, typing.Any] | domain.Error:
    # noinspection PyBroadException
    try:
        if not config_file_path.exists():
            return domain.Error.new(f"config_file_path, {config_file_path.resolve()!s}, does not exist.")

        with config_file_path.open("r") as fh:
            return json.load(fh)
    except:  # noqa: E722
        return domain.Error.new("An error occurred while reading config.json.")


def username(*, config_file_path: pathlib.Path) -> str | domain.Error:
    # noinspection PyBroadException
    try:
        config = _config(config_file_path=config_file_path)
        if isinstance(config, domain.Error):
            return config

        config_file_username = config.get("current-user")
        if config_file_username:
            return config_file_username

        return os.environ.get("USERNAME", "user")
    except:  # noqa: E722
        return domain.Error.new("An error occurred while looking up current user from config.json.")


def db_schema(*, config_file_path: pathlib.Path) -> str | None | domain.Error:
    # noinspection PyBroadException
    try:
        config = _config(config_file_path=config_file_path)
        if isinstance(config, domain.Error):
            return config

        return config.get("db-schema")
    except:  # noqa: E722
        return domain.Error.new("An error occurred while looking up db schema from config.json.")
