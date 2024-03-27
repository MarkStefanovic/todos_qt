import typing

__all__ = ("Item",)

Item = typing.TypeVar("Item", contravariant=True)
