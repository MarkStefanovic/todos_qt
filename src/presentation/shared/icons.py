"""
qtawesome repo: https://github.com/spyder-ide/qtawesome
"""

# noinspection PyPep8Naming
from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa: F401

from src import adapter, domain


__all__ = (
    "app_icon",
    "add_btn_icon",
    "bold_btn_icon",
    "clear_bold_btn_icon",
    "delete_btn_icon",
    "edit_btn_icon",
    "refresh_btn_icon",
    "highlight_btn_icon",
    "clear_highlight_btn_icon",
    "back_btn_icon",
    "save_btn_icon",
)


def add_btn_icon(*, parent: qtw.QWidget) -> qtg.QIcon:
    # noinspection PyBroadException
    try:
        return qtg.QIcon(str((adapter.fs.assets_folder() / "icons" / "plus.svg").resolve()))
    except:  # noqa: E722
        return qtg.QIcon.fromTheme("list-add", parent.style().standardIcon(qtw.QStyle.SP_FileDialogNewFolder))


def app_icon() -> qtg.QIcon | domain.Error:
    try:
        icon_path = adapter.fs.assets_folder() / "app.png"
        if not icon_path.exists():
            return domain.Error.new(f"app icon not found at {icon_path.resolve()!s}.")

        return qtg.QIcon(str(icon_path.resolve()))
    except Exception as e:
        return domain.Error.new(str(e))


def back_btn_icon(*, parent: qtw.QWidget) -> qtg.QIcon:
    # noinspection PyBroadException
    try:
        return qtg.QIcon(str((adapter.fs.assets_folder() / "icons" / "arrow-left-solid.svg").resolve()))
    except:  # noqa: E722
        return qtg.QIcon.fromTheme("go-previous", parent.style().standardIcon(qtw.QStyle.SP_FileDialogNewFolder))


# def bold_btn_icon(*, parent: qtw.QWidget) -> qtg.QIcon:
#     # noinspection PyBroadException
#     try:
#         return qtg.QIcon.fromTheme("format-text-bold")
#     except:  # noqa: E722
#         try:
#             import qtawesome as qta
#
#             return qta.icon(icon_name="mdi.format-bold", color=parent.palette().text().color())
#         except:  # noqa: E722
#             return parent.style().standardIcon(qtw.QStyle.SP_MediaVolume)
#
#
# def clear_bold_btn_icon(*, parent: qtw.QWidget) -> qtg.QIcon:
#     # noinspection PyBroadException
#     try:
#         return qtg.QIcon.fromTheme("go-last")
#     except:  # noqa: E722
#         try:
#             import qtawesome as qta
#
#             return qta.icon(icon_name="mdi.bootstrap", color=parent.palette().text().color())
#         except:  # noqa: E722
#             return parent.style().standardIcon(qtw.QStyle.SP_MediaVolumeMuted)


# def clear_highlight_btn_icon(*, parent: qtw.QWidget) -> qtg.QIcon:
#     # noinspection PyBroadException
#     try:
#         return qtg.QIcon.fromTheme("go-last")
#     except:  # noqa: E722
#         try:
#             import qtawesome as qta
#
#             return qta.icon(icon_name="mdi.format-color-marker-cancel", color=parent.palette().text().color())
#         except:  # noqa: E722
#             return parent.style().standardIcon(qtw.QStyle.SP_DialogCloseButton)


def delete_btn_icon(*, parent: qtw.QWidget) -> qtg.QIcon:
    # noinspection PyBroadException
    try:
        return qtg.QIcon(str((adapter.fs.assets_folder() / "icons" / "trash-solid.svg").resolve()))
    except:  # noqa: E722
        return qtg.QIcon.fromTheme("list-remove", parent.style().standardIcon(qtw.QStyle.SP_DialogDiscardButton))


def edit_btn_icon(*, parent: qtw.QWidget) -> qtg.QIcon:
    # noinspection PyBroadException
    try:
        return qtg.QIcon(str((adapter.fs.assets_folder() / "icons" / "pen-solid.svg").resolve()))
    except:  # noqa: E722
        return qtg.QIcon.fromTheme("edit-undo", parent.style().standardIcon(qtw.QStyle.SP_FileDialogContentsView))


# def highlight_btn_icon(*, parent: qtw.QWidget) -> qtg.QIcon:
#     # noinspection PyBroadException
#     try:
#         return qtg.QIcon.fromTheme("format-justify-fill")
#     except:  # noqa: E722
#         try:
#             import qtawesome as qta
#
#             return qta.icon(icon_name="mdi.format-color-highlight", color=parent.palette().text().color())
#         except:  # noqa: E722
#             return parent.style().standardIcon(qtw.QStyle.SP_DialogResetButton)


def refresh_btn_icon(*, parent: qtw.QWidget) -> qtg.QIcon:
    # noinspection PyBroadException
    try:
        return qtg.QIcon(str((adapter.fs.assets_folder() / "icons" / "arrows-rotate-solid.svg").resolve()))
    except:  # noqa: E722
        return qtg.QIcon.fromTheme("view-refresh", parent.style().standardIcon(qtw.QStyle.SP_BrowserReload))


def save_btn_icon(*, parent: qtw.QWidget) -> qtg.QIcon:
    # noinspection PyBroadException
    try:
        return qtg.QIcon(str((adapter.fs.assets_folder() / "icons" / "floppy-disk-solid.svg").resolve()))
    except:  # noqa: E722
        return qtg.QIcon.fromTheme("document-save-as", parent.style().standardIcon(qtw.QStyle.SP_DialogSaveButton))
