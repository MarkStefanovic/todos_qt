import qtawesome as qta

# noinspection PyPep8Naming
from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa: F401

from src import adapter, domain

__all__ = (
    "app_icon",
    "add_btn_icon",
    "bold_btn_icon",
    "clear_bold_btn_icon",
    "refresh_btn_icon",
    "highlight_btn_icon",
    "clear_highlight_btn_icon",
    "back_btn_icon",
    "save_btn_icon",
)


def add_btn_icon(*, parent: qtw.QWidget | None) -> qtg.QIcon:
    return _icon(icon_name="ei.plus", parent=parent)


def app_icon() -> qtg.QIcon | domain.Error:
    try:
        icon_path = adapter.fs.assets_folder() / "app.png"
        if not icon_path.exists():
            return domain.Error.new(f"app icon not found at {icon_path.resolve()!s}.")

        return qtg.QIcon(str(icon_path.resolve()))
    except Exception as e:
        return domain.Error.new(str(e))


def bold_btn_icon(*, parent: qtw.QWidget | None) -> qtg.QIcon:
    return _icon(icon_name="mdi.format-bold", parent=parent)


def clear_bold_btn_icon(*, parent: qtw.QWidget | None) -> qtg.QIcon:
    return _icon(icon_name="mdi.bootstrap", parent=parent)


def refresh_btn_icon(*, parent: qtw.QWidget | None) -> qtg.QIcon:
    return _icon(icon_name="fa.refresh", parent=parent)


def highlight_btn_icon(*, parent: qtw.QWidget | None) -> qtg.QIcon:
    return _icon(icon_name="mdi.format-color-highlight", parent=parent)


def clear_highlight_btn_icon(*, parent: qtw.QWidget | None) -> qtg.QIcon:
    return _icon(icon_name="mdi.format-color-marker-cancel", parent=parent)


def back_btn_icon(*, parent: qtw.QWidget | None) -> qtg.QIcon:
    return _icon(icon_name="ei.arrow-left", parent=parent)


def save_btn_icon(*, parent: qtw.QWidget | None) -> qtg.QIcon:
    return _icon(icon_name="fa5.save", parent=parent)


def _icon(*, icon_name: str, parent: qtw.QWidget | None) -> qtg.QIcon:
    if parent is None:
        return qta.icon(icon_name)

    return qta.icon(icon_name, color=parent.palette().text().color())
