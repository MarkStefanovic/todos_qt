import pathlib
import typing


__all__ = (
    "TodosException",
    "ConnectionClosed",
    "InvalidDtoType",
)


class TodosException(Exception):
    def __init__(self, /, message: str) -> None:
        self.message = message


class ConnectionClosed(TodosException):
    def __init__(self) -> None:
        super().__init__("Attempted to use a closed connection.")


class DeveloperError(TodosException):
    def __init__(self, /, message: str) -> None:
        super().__init__(message)


class FileNotFound(TodosException):
    def __init__(self, /, fp: pathlib.Path) -> None:
        self.fp = fp
        super().__init__(f"{fp!s} does not exist.")


class InvalidDtoType(TodosException):
    def __init__(self, cls: typing.Type[typing.Any]) -> None:
        msg = f"The domain type must be either a dataclasses.dataclass or a pydantic.BaseModel, but got {cls.__name__}.."
        super().__init__(msg)


class OutsideTransaction(TodosException):
    def __init__(self, /, resource_name: str) -> None:
        self.resource_name = resource_name
        super().__init__(f"Attempted to access {resource_name} outside a `with` block.")
