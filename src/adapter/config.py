import functools
import os
import pathlib
import sys

from src import domain

__all__ = ("DefaultConfig",)


class DefaultConfig(domain.Config):
    @functools.cached_property
    def db_path(self) -> pathlib.Path:
        folder = root_dir() / "assets"
        folder.mkdir(exist_ok=True)
        return folder / "db.sqlite"

    @functools.cached_property
    def log_dir(self) -> pathlib.Path:
        folder = root_dir() / "logs"
        folder.mkdir(exist_ok=True)
        return folder


@functools.lru_cache
def root_dir() -> pathlib.Path:
    if getattr(sys, "frozen", False):
        return pathlib.Path(os.path.dirname(sys.executable))
    else:
        folder = pathlib.Path(sys.argv[0]).parent
        if folder.name == "adapter":
            folder = folder.parent.parent
        elif folder.name == "src":
            folder = folder.parent
        assert folder.name == "todos-qt"
        return folder
