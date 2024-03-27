from __future__ import annotations

import datetime
import typing

# noinspection PyPep8Naming
from PyQt6 import QtGui as qtg

from src.presentation.shared.widgets.table_view import protocols
from src.presentation.shared.widgets.table_view.item import Item
from src.presentation.shared.widgets.table_view.value import Value

__all__ = (
    "Attr",
    "text",
    "button",
    "timestamp",
    "date",
    "integer",
)


class Attr(typing.Generic[Item, Value]):
    __slots__ = (
        "alignment",
        "data_type",
        "display_name",
        "hidden",
        "name",
        "enabled_selector",
        "value_selector",
        "color_selector",
        "icon",
        "width",
    )

    def __init__(
        self,
        *,
        alignment: typing.Literal["center", "left", "right"],
        data_type: typing.Literal["button", "date", "datetime", "int", "text"],
        display_name: str,
        hidden: bool,
        enabled_when: protocols.EnabledSelector[Item] | None,
        name: str,
        value_selector: protocols.ValueSelector[Item, Value] | None,
        text_color_selector: protocols.TextColorSelector[Item] | None,
        icon: qtg.QIcon | None,
        width: int | None,
    ):
        self.alignment: typing.Final[typing.Literal["center", "left", "right"]] = alignment
        self.data_type: typing.Final[typing.Literal["button", "date", "datetime", "int", "text"]] = data_type
        self.display_name: typing.Final[str] = display_name
        self.hidden: typing.Final[bool] = hidden
        self.enabled_selector: typing.Final[protocols.EnabledSelector | None] = enabled_when
        self.name: typing.Final[str] = name
        self.value_selector: typing.Final[protocols.ValueSelector | None] = value_selector
        self.color_selector: typing.Final[protocols.TextColorSelector | None] = text_color_selector
        self.icon: typing.Final[qtg.QIcon | None] = icon
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
            f"  hidden: {self.hidden!r}"
            f"  name: {self.name!r}"
            f"  icon: {self.icon!r}"
            f"  width: {self.width!r}"
            "]"
        )


def text(
    name: str,
    display_name: str,
    alignment: typing.Literal["center", "left", "right"] = "left",
    width: int | None = None,
    value_selector: protocols.ValueSelector[Item, str] | None = None,
    text_color_selector: protocols.TextColorSelector[Item] | None = None,
    hidden: bool = False,
) -> Attr[Item, str]:
    return Attr(
        name=name,
        data_type="text",
        display_name=display_name,
        hidden=hidden,
        alignment=alignment,
        width=width,
        enabled_when=None,
        value_selector=value_selector,
        text_color_selector=text_color_selector,
        icon=None,
    )


def button(
    name: str,
    button_text: str,
    width: int | None = None,
    enabled_when: protocols.EnabledSelector[Item] | None = None,
    text_selector: protocols.ValueSelector[Item, str] | None = None,
    text_color_selector: protocols.TextColorSelector[Item] | None = None,
    icon: qtg.QIcon | None = None,
) -> Attr[Item, str]:
    return Attr(
        name=name,
        data_type="button",
        display_name=button_text,
        hidden=False,
        alignment="center",
        width=width,
        enabled_when=enabled_when,
        value_selector=text_selector,
        text_color_selector=text_color_selector,
        icon=icon,
    )


def timestamp(
    name: str,
    display_name: str,
    width: int | None = None,
    value_selector: protocols.ValueSelector[Item, datetime.datetime | None] | None = None,
    text_color_selector: protocols.TextColorSelector[Item] | None = None,
    hidden: bool = False,
) -> Attr[Item, datetime.datetime | None]:
    return Attr(
        name=name,
        data_type="datetime",
        display_name=display_name,
        hidden=hidden,
        alignment="center",
        width=width,
        enabled_when=None,
        value_selector=value_selector,
        text_color_selector=text_color_selector,
        icon=None,
    )


def date(
    name: str,
    display_name: str,
    width: int | None = None,
    value_selector: protocols.ValueSelector[Item, datetime.date | None] | None = None,
    text_color_selector: protocols.TextColorSelector[Item] | None = None,
    hidden: bool = False,
) -> Attr[Item, datetime.date | None]:
    return Attr(
        name=name,
        data_type="date",
        display_name=display_name,
        hidden=hidden,
        alignment="center",
        width=width,
        enabled_when=None,
        value_selector=value_selector,
        text_color_selector=text_color_selector,
        icon=None,
    )


def integer(
    name: str,
    display_name: str,
    alignment: typing.Literal["center", "left", "right"] = "center",
    width: int | None = None,
    value_selector: protocols.ValueSelector[Item, int | None] | None = None,
    text_color_selector: protocols.TextColorSelector[Item] | None = None,
    hidden: bool = False,
) -> Attr[Item, int | None]:
    return Attr(
        name=name,
        data_type="int",
        display_name=display_name,
        hidden=hidden,
        alignment=alignment,
        width=width,
        enabled_when=None,
        value_selector=value_selector,
        text_color_selector=text_color_selector,
        icon=None,
    )
