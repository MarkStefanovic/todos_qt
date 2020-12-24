import abc
import pathlib

__all__ = ("Config",)


class Config(abc.ABC):
    @abc.abstractmethod
    def db_path(self) -> pathlib.Path:
        raise NotImplementedError

    @abc.abstractmethod
    def log_dir(self) -> pathlib.Path:
        raise NotImplementedError
