"""
qtawesome repo: https://github.com/spyder-ide/qtawesome
"""

# noinspection PyPep8Naming
from PyQt6 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa: F401

from src import domain

__all__ = (
    "app_icon",
    "add_btn_icon",
    "delete_btn_icon",
    "edit_btn_icon",
    "refresh_btn_icon",
    "back_btn_icon",
    "save_btn_icon",
)


def add_btn_icon(*, parent: qtw.QWidget) -> qtg.QIcon:
    # noinspection PyBroadException
    try:
        png_path = domain.fs.assets_folder() / "icons" / "plus.png"
        if png_path.exists():
            return qtg.QIcon(str(png_path.resolve()))

        return qtg.QIcon(str((domain.fs.assets_folder() / "icons" / "plus.svg").resolve()))
    except:  # noqa: E722
        return qtg.QIcon.fromTheme(
            "list-add", parent.style().standardIcon(qtw.QStyle.StandardPixmap.SP_FileDialogNewFolder)
        )


def app_icon() -> qtg.QIcon | domain.Error:
    try:
        icon_path = domain.fs.assets_folder() / "icons" / "app.png"
        if not icon_path.exists():
            return domain.Error.new(f"app icon not found at {icon_path.resolve()!s}.")

        return qtg.QIcon(str(icon_path.resolve()))
    except Exception as e:
        return domain.Error.new(str(e))


def back_btn_icon(*, parent: qtw.QWidget) -> qtg.QIcon:
    # noinspection PyBroadException
    try:
        png_path = domain.fs.assets_folder() / "icons" / "arrow-left.png"
        if png_path.exists():
            return qtg.QIcon(str(png_path.resolve()))

        return qtg.QIcon(str((domain.fs.assets_folder() / "icons" / "arrow-left.svg").resolve()))
    except:  # noqa: E722
        return qtg.QIcon.fromTheme(
            "go-previous", parent.style().standardIcon(qtw.QStyle.StandardPixmap.SP_FileDialogNewFolder)
        )


def delete_btn_icon(*, parent: qtw.QWidget) -> qtg.QIcon:
    # noinspection PyBroadException
    try:
        png_path = domain.fs.assets_folder() / "icons" / "trash.png"
        if png_path.exists():
            return qtg.QIcon(str(png_path.resolve()))

        return qtg.QIcon(str((domain.fs.assets_folder() / "icons" / "trash.svg").resolve()))
    except:  # noqa: E722
        return qtg.QIcon.fromTheme(
            "list-remove", parent.style().standardIcon(qtw.QStyle.StandardPixmap.SP_DialogDiscardButton)
        )


def edit_btn_icon(*, parent: qtw.QWidget) -> qtg.QIcon:
    # noinspection PyBroadException
    try:
        png_path = domain.fs.assets_folder() / "icons" / "pen.png"
        if png_path.exists():
            return qtg.QIcon(str(png_path.resolve()))

        return qtg.QIcon(str((domain.fs.assets_folder() / "icons" / "pen.svg").resolve()))
    except:  # noqa: E722
        return qtg.QIcon.fromTheme(
            "edit-undo", parent.style().standardIcon(qtw.QStyle.StandardPixmap.SP_FileDialogContentsView)
        )


def refresh_btn_icon(*, parent: qtw.QWidget) -> qtg.QIcon:
    # noinspection PyBroadException
    try:
        png_path = domain.fs.assets_folder() / "icons" / "refresh.png"
        if png_path.exists():
            return qtg.QIcon(str(png_path.resolve()))

        return qtg.QIcon(str((domain.fs.assets_folder() / "icons" / "refresh.svg").resolve()))
    except:  # noqa: E722
        return qtg.QIcon.fromTheme(
            "view-refresh", parent.style().standardIcon(qtw.QStyle.StandardPixmap.SP_BrowserReload)
        )


def save_btn_icon(*, parent: qtw.QWidget) -> qtg.QIcon:
    # noinspection PyBroadException
    try:
        png_path = domain.fs.assets_folder() / "icons" / "save.png"
        if png_path.exists():
            return qtg.QIcon(str(png_path.resolve()))

        return qtg.QIcon(str((domain.fs.assets_folder() / "icons" / "save.svg").resolve()))
    except:  # noqa: E722
        return qtg.QIcon.fromTheme(
            "document-save-as", parent.style().standardIcon(qtw.QStyle.StandardPixmap.SP_DialogSaveButton)
        )
