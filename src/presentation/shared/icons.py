import typing

# noinspection PyPep8Naming
from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa: F401

from src import adapter, domain

__all__ = (
    "app_icon",
    "add_btn_icon_name",
    "bold_btn_icon_name",
    "clear_bold_btn_icon_name",
    "refresh_btn_icon_name",
    "highlight_btn_icon_name",
    "clear_highlight_btn_icon_name",
    "back_btn_icon_name",
    "save_btn_icon_name",
)

add_btn_icon_name: typing.Final[str] = "ei.plus"
bold_btn_icon_name: typing.Final[str] = "mdi.format-bold"
clear_bold_btn_icon_name: typing.Final[str] = "mdi.bootstrap"
refresh_btn_icon_name: typing.Final[str] = "fa.refresh"
highlight_btn_icon_name: typing.Final[str] = "mdi.format-color-highlight"
clear_highlight_btn_icon_name: typing.Final[str] = "mdi.format-color-marker-cancel"
back_btn_icon_name: typing.Final[str] = "ei.arrow-left"
save_btn_icon_name: typing.Final[str] = "fa5.save"


def app_icon() -> qtg.QIcon | domain.Error:
    try:
        icon_path = adapter.fs.assets_folder() / "app.png"
        if not icon_path.exists():
            return domain.Error.new(f"app icon not found at {icon_path.resolve()!s}.")

        return qtg.QIcon(str(icon_path.resolve()))
    except Exception as e:
        return domain.Error.new(str(e))
