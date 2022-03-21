from PyQt5 import QtWidgets as qtw

__all__ = ("confirm", "error_message")


def error_message(*, message: str, title: str = "Error") -> None:
    msg = qtw.QMessageBox()
    msg.setIcon(qtw.QMessageBox.Critical)
    msg.setInformativeText(message)
    msg.setWindowTitle(title)
    msg.exec_()


def confirm(*, question: str, title: str = "Confirm") -> bool:
    # noinspection PyUnresolvedReferences,PyTypeChecker
    if qtw.QMessageBox.question(None, title, question) == qtw.QMessageBox.StandardButton.Yes:
        return True
    return False
