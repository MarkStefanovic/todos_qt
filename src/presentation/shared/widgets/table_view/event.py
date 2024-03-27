import dataclasses
import typing

from src.presentation.shared.widgets.table_view import Attr
from src.presentation.shared.widgets.table_view.value import Value
from src.presentation.shared.widgets.table_view.item import Item

__all__ = (
    "ButtonClickedEvent",
    "DoubleClickedEvent",
)


@dataclasses.dataclass(frozen=True, kw_only=True)
class ButtonClickedEvent(typing.Generic[Item, Value]):
    attr: Attr[Item, Value]
    item: Item


@dataclasses.dataclass(frozen=True, kw_only=True)
class DoubleClickedEvent(typing.Generic[Item, Value]):
    attr: Attr[Item, Value]
    item: Item
