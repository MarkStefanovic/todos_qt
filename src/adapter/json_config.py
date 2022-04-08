import functools
import json

from src import domain
from src.adapter.fs import config_path

__all__ = ("config",)


@functools.lru_cache(1)
def config() -> domain.Config:
    with config_path().open("r") as fh:
        data = json.load(fh)
        return domain.Config(**data)
