import functools
import os
import pathlib
import sys

__all__ = (
    "assets_folder",
    "root_dir",
)


@functools.lru_cache
def root_dir() -> pathlib.Path:
    if getattr(sys, "frozen", False):
        path = pathlib.Path(os.path.dirname(sys.executable))
        assert path is not None
        return path
    else:
        project_root = pathlib.Path(__file__).parent.parent.parent
        assert (project_root / "pyproject.toml").exists(), (
            f"An error occurred while looking up the project root.  {project_root.resolve()!s} does not contain a "
            f"pyproject.toml file."
        )
        return project_root


@functools.lru_cache
def assets_folder() -> pathlib.Path:
    folder = root_dir() / "assets"

    assert folder.exists(), f"{folder.resolve()!s} does not exist."

    return folder
