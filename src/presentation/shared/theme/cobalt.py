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
            border: none;
        }
        QPushButton {
            font-weight: bold;
            background-color: none;
            color: cyan;
            border: none;
        }
        QHeaderView, QLabel, QMainWindow, QStatusBar, QTableView, QTabBar, QTabWidget { border: none; }
        
        QTabWidget:pane {
            background-color: none;
            border: none;
        }
        QTabBar { 
            font-weight: bold;
            border-top: none; 
            border-left: none; 
            border-right: none; 
            border-bottom: none;
            background-color: none;
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
        
        QHeaderView, QHeaderView::section {
            border-radius: 0px;
            background-color: rgb(35, 35, 50);
        }
        QTableCornerButton:section { 
            background-color: rgb(35, 35, 50);
        }
        QTableView:item {
            border: 0px;
            padding: 4px;
            min-height: 20px;
        }
        QTableView:item:hover { background-color: rgb(80, 80, 140); }
        
        QPushButton:hover { background-color: rgb(80, 80, 140); }
        QPushButton:pressed { background-color: rgb(80, 80, 140); }
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
