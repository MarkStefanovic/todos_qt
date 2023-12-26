import functools
import json
import os
import typing

from src import domain

__all__ = (
    "current_user",
    "db_schema",
)


@functools.lru_cache
def _config() -> dict[str, typing.Any] | domain.Error:
    # noinspection PyBroadException
    try:
        path = domain.fs.config_path()
        with path.open("r") as fh:
            return json.load(fh)
    except:  # noqa: E722
        return domain.Error.new("An error occurred while reading config.json.")


def current_user() -> str | domain.Error:
    # noinspection PyBroadException
    try:
        config = _config()
        if isinstance(config, domain.Error):
            return config

        username = config.get("current-user")
        if username:
            return username
        return os.environ.get("USERNAME", "user")
    except:  # noqa: E722
        return domain.Error.new("An error occurred while looking up current user from config.json.")


def db_schema() -> str | None | domain.Error:
    # noinspection PyBroadException
    try:
        config = _config()
        if isinstance(config, domain.Error):
            return config

        return config.get("db-schema")
    except:  # noqa: E722
        return domain.Error.new("An error occurred while looking up db schema from config.json.")
