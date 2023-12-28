# css ref: https://doc.qt.io/qt-6/stylesheet-examples.html

# noinspection PyPep8Naming
from PyQt6 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa: F401

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

        QPushButton {
            font-weight: bold;
            background-color: none;
            color: cyan;
            border: none;
        }
        
        QHeaderView, QLabel, QMainWindow, QStackedWidget, QStatusBar, QTableView, QTabBar, QTabWidget { border: none; }
        
        /* Scrollbar - Horizontal */
        QScrollBar:horizontal {
            border: none;
            background-color: rgb(80, 80, 100);
            height: 20px;
        }
        QScrollBar::handle:horizontal {
            background: cyan;
            min-width: 20px;
        }
        QScrollBar::add-line:horizontal {
            border: none;
        }
        QScrollBar::sub-line:horizontal {
            border: none;
        }
        
        /* Scrollbar - Vertical */
        QScrollBar:vertical {
            border: none;
            background-color: rgb(80, 80, 100);
            width: 20px;
        }
        QScrollBar::handle:vertical {
            background: cyan;
            min-width: 20px;
        }
        QScrollBar::add-line:vertical {
            border: none;
        }
        QScrollBar::sub-line:vertical {
            border: none;
        }
        
        QStatusBar {
            background-color: rgb(25, 25, 40);
        }
        
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
        QTabBar::tab { 
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
        
        QHeaderView::section { 
            background-color: rgb(35, 35, 50);
            font-weight: bold; 
            border-left: 1px solid rgb(80, 80, 100);
            border-right: 1px solid rgb(80, 80, 100);
            padding: 4px;
            min-height: 24px;
        }
        QTableCornerButton::section { 
            background-color: rgb(15, 15, 25);
        }
        QTableView::item {
            border-left: 1px solid rgb(25, 25, 40);
            padding: 4px;
            min-height: 20px;
        }
        QTableView::item:hover { background-color: rgb(80, 80, 140); }
        
        QPushButton:hover { background-color: rgb(80, 80, 140); }
        QPushButton:pressed { background-color: rgb(80, 80, 140); }
        
        QComboBox {
            border: none;
            combobox-popup: 0;
            color: cyan;
            background-color: rgb(35, 35, 50);
            border-radius: 4px;
            min-width: 6em;
        }
        QComboBox::drop-down {
            width: 0px;
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
