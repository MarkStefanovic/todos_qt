import functools
import os
import pathlib
import sys

__all__ = ("assets_folder", "config_path", "root_dir",)


@functools.lru_cache
def root_dir() -> pathlib.Path:
    if getattr(sys, "frozen", False):
        path = pathlib.Path(os.path.dirname(sys.executable))
        assert path is not None
        return path
    else:
        path = pathlib.Path(sys.argv[0]).parent.parent
        assert path.name == "todos-qt", f"Expected the parent folder to be named todos-qt, but the path was {path.resolve()!s}."
        return path


@functools.lru_cache
def assets_folder() -> pathlib.Path:
    folder = root_dir() / "assets"
    assert folder.exists(), f"{folder.resolve()!s} does not exist."
    return folder


@functools.lru_cache
def config_path() -> pathlib.Path:
    path = assets_folder() / "config.json"
    assert path.exists(), f"{path.resolve()!s} does not exist."
    return path
