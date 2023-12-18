# noinspection PyPep8Naming
from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa: F401

__all__ = ("apply_theme",)


def apply_theme(*, app: qtw.QApplication) -> None:
    app.setStyle("Fusion")

    app.setStyleSheet(
        """
        QWidget { 
            font-family: Arial;
            font-size: 12pt; 
        }
        QHeaderView { font-weight: bold; }
        QPushButton { 
            color: cyan;
            font-weight: bold; 
        }
        QPushButton:hover:!pressed { background-color: rgb(80, 80, 140); }
        QPushButton:!hover { background-color: rgb(60, 60, 80); }
        QTabBar::tab:selected { 
            background: rgb(80, 80, 100);
            border: 1px solid rgb(140, 140, 180); 
            border-bottom-color: none; 
            border-top-left-radius: 1px;
            border-top-right-radius: 1px;
            min-width: 60px;
            padding: 4px;
        }
        QTabBar::tab:hover { background: rgb(100, 100, 140); }
        QPushButton#table_btn { background-color: none; border: none; }
        QPushButton#table_btn:enabled { color: cyan; }
        QPushButton#table_btn:disabled { color: none; }
        QPushButton#table_btn:hover:!pressed { background-color: rgb(80, 80, 140); }
        QPushButton#table_btn:!hover { background-color: none; }
    """
    )

    app.setPalette(_cobalt_palette())


def _cobalt_palette() -> qtg.QPalette:
    base_color = qtg.QColor(15, 15, 25)
    alternate_color = qtg.QColor(35, 35, 50)
    tooltip_background_color = qtg.QColor(25, 25, 25)
    link_color = qtg.QColor(42, 130, 218)
    highlight_background_color = qtg.QColor(42, 130, 218)

    color_lkp = {
        (qtg.QPalette.Window,): alternate_color,
        (qtg.QPalette.WindowText,): qtc.Qt.white,
        (qtg.QPalette.Base,): base_color,
        (qtg.QPalette.AlternateBase,): alternate_color,
        (qtg.QPalette.ToolTipBase,): tooltip_background_color,
        (qtg.QPalette.ToolTipText,): qtc.Qt.white,
        (qtg.QPalette.Text,): qtc.Qt.white,
        (qtg.QPalette.Button,): alternate_color,
        (qtg.QPalette.ButtonText,): qtc.Qt.white,
        (qtg.QPalette.BrightText,): qtc.Qt.red,
        (qtg.QPalette.Link,): link_color,
        (qtg.QPalette.Highlight,): highlight_background_color,
        (qtg.QPalette.HighlightedText,): base_color,
        (qtg.QPalette.Active, qtg.QPalette.Button): alternate_color,
        (qtg.QPalette.Disabled, qtg.QPalette.ButtonText): qtc.Qt.darkGray,
        (qtg.QPalette.Disabled, qtg.QPalette.WindowText): qtc.Qt.darkGray,
        (qtg.QPalette.Disabled, qtg.QPalette.Text): qtc.Qt.darkGray,
        (qtg.QPalette.Disabled, qtg.QPalette.Light): alternate_color,
    }

    palette = qtg.QPalette()
    for selector, color in color_lkp.items():
        palette.setColor(*selector, color)  # type: ignore

    return palette
