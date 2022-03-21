import functools
import json
import pathlib

from src import domain

__all__ = ("load",)


@functools.lru_cache(1)
def load(*, path: pathlib.Path) -> domain.Config:
    with path.open("r") as fh:
        data = json.load(fh)
        return domain.Config(**data)
