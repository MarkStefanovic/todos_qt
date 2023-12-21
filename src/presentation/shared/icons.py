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


def add_btn_icon(*, parent: qtw.QWidget) -> qtg.QIcon:
    # noinspection PyBroadException
    try:
        import qtawesome as qta

        return qta.icon(icon_name="ei.plus", color=parent.palette().text().color())
    except:  # noqa: E722
        return parent.style().standardIcon(qtw.QStyle.SP_FileDialogNewFolder)


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
        import qtawesome as qta

        return qta.icon(icon_name="ei.arrow-left", color=parent.palette().text().color())
    except:  # noqa: E722
        return parent.style().standardIcon(qtw.QStyle.SP_MediaSeekBackward)


def bold_btn_icon(*, parent: qtw.QWidget) -> qtg.QIcon:
    # noinspection PyBroadException
    try:
        import qtawesome as qta

        return qta.icon(icon_name="mdi.format-bold", color=parent.palette().text().color())
    except:  # noqa: E722
        return parent.style().standardIcon(qtw.QStyle.SP_MediaVolume)


def clear_bold_btn_icon(*, parent: qtw.QWidget) -> qtg.QIcon:
    # noinspection PyBroadException
    try:
        import qtawesome as qta

        return qta.icon(icon_name="mdi.bootstrap", color=parent.palette().text().color())
    except:  # noqa: E722
        return parent.style().standardIcon(qtw.QStyle.SP_MediaVolumeMuted)


def clear_highlight_btn_icon(*, parent: qtw.QWidget) -> qtg.QIcon:
    # noinspection PyBroadException
    try:
        import qtawesome as qta

        return qta.icon(icon_name="mdi.format-color-marker-cancel", color=parent.palette().text().color())
    except:  # noqa: E722
        return parent.style().standardIcon(qtw.QStyle.SP_DialogCloseButton)


def highlight_btn_icon(*, parent: qtw.QWidget) -> qtg.QIcon:
    # noinspection PyBroadException
    try:
        import qtawesome as qta

        return qta.icon(icon_name="mdi.format-color-highlight", color=parent.palette().text().color())
    except:  # noqa: E722
        return parent.style().standardIcon(qtw.QStyle.SP_DialogResetButton)


def refresh_btn_icon(*, parent: qtw.QWidget) -> qtg.QIcon:
    # noinspection PyBroadException
    try:
        import qtawesome as qta

        return qta.icon(icon_name="fa.refresh", color=parent.palette().text().color())
    except:  # noqa: E722
        return parent.style().standardIcon(qtw.QStyle.SP_BrowserReload)


def save_btn_icon(*, parent: qtw.QWidget) -> qtg.QIcon:
    # noinspection PyBroadException
    try:
        import qtawesome as qta

        return qta.icon(icon_name="fa5.save", color=parent.palette().text().color())
    except:  # noqa: E722
        return parent.style().standardIcon(qtw.QStyle.SP_DialogSaveButton)
