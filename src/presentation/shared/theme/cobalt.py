# noinspection PyPep8Naming
from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa: F401

from src.presentation.shared.theme import font

__all__ = ("apply_theme",)


def apply_theme(app: qtw.QApplication) -> None:
    app.setStyleSheet(
        """
        QWidget {
            background-color: rgb(15, 15, 25);
            alternate-background-color: rgb(35, 35, 50);
            color: white;
            selection-color: cyan;
            selection-background-color: rgb(80, 80, 100);
            padding: 4px;
            border-radius: 4px;
            border: 1px solid rgb(35, 35, 50);
        }
        QWidget:disabled {
            color: rgb(15, 15, 25);
            selection-background-color: orange;
            selection-color: green;
        }
        QHeaderView:section { 
            background-color: rgb(35, 35, 50);
            font-weight: bold; 
        }
        QPushButton {
            font-weight: bold;
            background-color: none;
            color: cyan;
            border: none;
        }
        QHeaderView, QMainWindow, QStatusBar, QTableView { border: none; }
        QTableView:item {
            border: 0px;
            padding: 4px;
            min-height: 20px;
        }
        QTableView:item:hover { background-color: rgb(80, 80, 140); }
        QPushButton:hover { background-color: rgb(80, 80, 140); }
        QPushButton:pressed { background-color: rgb(80, 80, 140); }
        QTabBar { 
            font-weight: bold;
            border-top: none; 
            border-bottom: 1px solid rgb(35, 35, 50); 
            border-left: none; 
            border-right: none; 
        }
        QTabBar:tab { 
            min-height: 30px;
            min-width: 100px;
            border: none;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
        }
        QTabBar:tab:selected {
            background: rgb(80, 80, 100);
        }
        QTabBar::tab:hover { background: rgb(100, 100, 140); }
        QLabel { border: none; }
        QComboBox {
            border: none;
            combobox-popup: 0;
            color: cyan;
            background-color: rgb(35, 35, 50);
        }
        QCheckBox, QLineEdit, QTextEdit {
            border: none;
            color: cyan;
            background-color: rgb(35, 35, 50);
        }
        QCheckBox::indicator,
        QGroupBox::indicator,
        QAbstractItemView::indicator,
        QRadioButton::indicator {
            height: 16px;
            width: 16px;
        }
        """
    )

    app.setFont(font.DEFAULT_FONT)
