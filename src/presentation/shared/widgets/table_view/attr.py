from __future__ import annotations

import datetime
import typing

__all__ = (
    "Attr",
    "text",
    "button",
    "timestamp",
    "date",
    "integer",
    "Item",
    "Value",
)

Item = typing.TypeVar("Item")
Value = typing.TypeVar("Value")


class Attr(typing.Generic[Item, Value]):
    __slots__ = (
        "alignment",
        "data_type",
        "display_name",
        "key",
        "name",
        "enabled_selector",
        "value_selector",
        "width",
        "rich_text",
    )

    def __init__(
        self,
        *,
        alignment: typing.Literal["center", "left", "right"],
        data_type: typing.Literal["button", "date", "datetime", "int", "text"],
        display_name: str,
        enabled_selector: typing.Callable[[Item], bool] | None,
        key: bool,
        name: str,
        rich_text: bool,
        value_selector: typing.Callable[[Item], Value] | None,
        width: int | None,
    ):
        self.alignment: typing.Final[typing.Literal["center", "left", "right"]] = alignment
        self.data_type: typing.Final[typing.Literal["button", "date", "datetime", "int", "text"]] = data_type
        self.display_name: typing.Final[str] = display_name
        self.enabled_selector: typing.Final[typing.Callable[[Item], bool] | None] = enabled_selector
        self.key: typing.Final[bool] = key
        self.name: typing.Final[str] = name
        self.rich_text: typing.Final[bool] = rich_text
        self.value_selector: typing.Final[typing.Callable[[Item], Value] | None] = value_selector
        self.width: typing.Final[int | None] = width

    def __eq__(self, other: object) -> bool:
        assert isinstance(other, Attr), f"Cannot compare an Attr to {other!r}."

        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return (
            "Attr ["
            f"  alignment: {self.alignment!r}"
            f"  data_type: {self.data_type!r}"
            f"  display_name: {self.display_name!r}"
            f"  enabled_selector: {self.enabled_selector!r}"
            f"  key: {self.key!r}"
            f"  name: {self.name!r}"
            f"  rich_text: {self.rich_text!r}"
            f"  value_selector: {self.value_selector!r}"
            f"  width: {self.width!r}"
            "]"
        )


def text(
    name: str,
    display_name: str,
    key: bool = False,
    alignment: typing.Literal["center", "left", "right"] = "left",
    width: int | None = None,
    value_selector: typing.Callable[[Item], str] | None = None,
    rich_text: bool = False,
) -> Attr[Item, str]:
    return Attr(
        name=name,
        data_type="text",
        display_name=display_name,
        key=key,
        alignment=alignment,
        width=width,
        enabled_selector=None,
        value_selector=value_selector,
        rich_text=rich_text,
    )


def button(
    name: str,
    button_text: str,
    width: int | None = None,
    enabled_selector: typing.Callable[[Item], bool] | None = None,
    text_selector: typing.Callable[[Item], str] | None = None,
) -> Attr[Item, str]:
    return Attr(
        name=name,
        data_type="button",
        display_name=button_text,
        key=False,
        alignment="center",
        width=width,
        enabled_selector=enabled_selector,
        value_selector=text_selector,
        rich_text=False,
    )


def timestamp(
    name: str,
    display_name: str,
    width: int | None = None,
    value_selector: typing.Callable[[Item], datetime.datetime | None] | None = None,
) -> Attr[Item, datetime.datetime | None]:
    return Attr(
        name=name,
        data_type="datetime",
        display_name=display_name,
        key=False,
        alignment="center",
        width=width,
        enabled_selector=None,
        value_selector=value_selector,
        rich_text=False,
    )


def date(
    name: str,
    display_name: str,
    width: int | None = None,
    value_selector: typing.Callable[[Item], datetime.date | None] | None = None,
) -> Attr[Item, datetime.date | None]:
    return Attr(
        name=name,
        data_type="date",
        display_name=display_name,
        key=False,
        alignment="center",
        width=width,
        enabled_selector=None,
        value_selector=value_selector,
        rich_text=False,
    )


def integer(
    name: str,
    display_name: str,
    key: bool = False,
    alignment: typing.Literal["center", "left", "right"] = "center",
    width: int | None = None,
    value_selector: typing.Callable[[Item], int] | None = None,
) -> Attr[Item, int]:
    return Attr(
        name=name,
        data_type="int",
        display_name=display_name,
        key=key,
        alignment=alignment,
        width=width,
        enabled_selector=None,
        value_selector=value_selector,
        rich_text=False,
    )
