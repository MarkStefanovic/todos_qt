"""
qtawesome repo: https://github.com/spyder-ide/qtawesome
"""

# noinspection PyPep8Naming
from PyQt6 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa: F401
from loguru import logger

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
    except Exception as e:
        logger.error(f"{__file__}.add_btn_icon(...) failed: {e}")

        if style := parent.style():
            fallback_icon = style.standardIcon(qtw.QStyle.StandardPixmap.SP_FileDialogNewFolder)
        else:
            fallback_icon = qtg.QIcon()

        return qtg.QIcon.fromTheme("list-add", fallback_icon)


def app_icon() -> qtg.QIcon | domain.Error:
    try:
        icon_path = domain.fs.assets_folder() / "icons" / "app.png"
        if not icon_path.exists():
            return domain.Error.new(f"app icon not found at {icon_path.resolve()!s}.")

        return qtg.QIcon(str(icon_path.resolve()))
    except Exception as e:
        logger.error(f"{__file__}.app_icon() failed: {e}")

        return domain.Error.new(str(e))


def back_btn_icon(*, parent: qtw.QWidget) -> qtg.QIcon:
    # noinspection PyBroadException
    try:
        png_path = domain.fs.assets_folder() / "icons" / "arrow-left.png"
        if png_path.exists():
            return qtg.QIcon(str(png_path.resolve()))

        return qtg.QIcon(str((domain.fs.assets_folder() / "icons" / "arrow-left.svg").resolve()))
    except Exception as e:
        logger.error(f"{__file__}.back_btn_icon(...) failed: {e}")

        if style := parent.style():
            fallback_icon = style.standardIcon(qtw.QStyle.StandardPixmap.SP_FileDialogNewFolder)
        else:
            fallback_icon = qtg.QIcon()

        return qtg.QIcon.fromTheme("go-previous", fallback_icon)


def delete_btn_icon(*, parent: qtw.QWidget) -> qtg.QIcon:
    # noinspection PyBroadException
    try:
        png_path = domain.fs.assets_folder() / "icons" / "trash.png"
        if png_path.exists():
            return qtg.QIcon(str(png_path.resolve()))

        return qtg.QIcon(str((domain.fs.assets_folder() / "icons" / "trash.svg").resolve()))
    except Exception as e:
        logger.error(f"{__file__}.delete_btn_icon(...) failed: {e}")

        if style := parent.style():
            fallback_icon = style.standardIcon(qtw.QStyle.StandardPixmap.SP_DialogDiscardButton)
        else:
            fallback_icon = qtg.QIcon()

        return qtg.QIcon.fromTheme("list-remove", fallback_icon)


def edit_btn_icon(*, parent: qtw.QWidget) -> qtg.QIcon:
    # noinspection PyBroadException
    try:
        png_path = domain.fs.assets_folder() / "icons" / "pen.png"
        if png_path.exists():
            return qtg.QIcon(str(png_path.resolve()))

        return qtg.QIcon(str((domain.fs.assets_folder() / "icons" / "pen.svg").resolve()))
    except Exception as e:
        logger.error(f"{__file__}.edit_btn_icon(...) failed: {e}")

        if style := parent.style():
            fallback_icon = style.standardIcon(qtw.QStyle.StandardPixmap.SP_FileDialogContentsView)
        else:
            fallback_icon = qtg.QIcon()

        return qtg.QIcon.fromTheme("edit-undo", fallback_icon)


def refresh_btn_icon(*, parent: qtw.QWidget) -> qtg.QIcon:
    # noinspection PyBroadException
    try:
        png_path = domain.fs.assets_folder() / "icons" / "refresh.png"
        if png_path.exists():
            return qtg.QIcon(str(png_path.resolve()))

        return qtg.QIcon(str((domain.fs.assets_folder() / "icons" / "refresh.svg").resolve()))
    except Exception as e:
        logger.error(f"{__file__}.refresh_btn_icon(...) failed: {e}")

        if style := parent.style():
            fallback_icon = style.standardIcon(qtw.QStyle.StandardPixmap.SP_BrowserReload)
        else:
            fallback_icon = qtg.QIcon()

        return qtg.QIcon.fromTheme("view-refresh", fallback_icon)


def save_btn_icon(*, parent: qtw.QWidget) -> qtg.QIcon:
    # noinspection PyBroadException
    try:
        png_path = domain.fs.assets_folder() / "icons" / "save.png"
        if png_path.exists():
            return qtg.QIcon(str(png_path.resolve()))

        return qtg.QIcon(str((domain.fs.assets_folder() / "icons" / "save.svg").resolve()))
    except Exception as e:
        logger.error(f"{__file__}.save_btn_icon(...) failed: {e}")

        if style := parent.style():
            fallback_icon = style.standardIcon(qtw.QStyle.StandardPixmap.SP_DialogSaveButton)
        else:
            fallback_icon = qtg.QIcon()

        return qtg.QIcon.fromTheme("document-save-as", fallback_icon)
