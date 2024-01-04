import datetime

# noinspection PyPep8Naming
from PyQt6 import QtCore as qtc, QtWidgets as qtw
from loguru import logger

from src import domain
from src.presentation.category.form import requests
from src.presentation.category.form.state import CategoryFormState
from src.presentation.shared.theme import font, icons

__all__ = ("CategoryForm",)


class CategoryForm(qtw.QWidget):
    def __init__(
        self,
        *,
        form_requests: requests.CategoryFormRequests,
        parent: qtw.QWidget | None = None,
    ):
        super().__init__(parent=parent)

        self._form_requests = form_requests

        back_btn_icon = icons.back_btn_icon(parent=self)
        self.back_btn = qtw.QPushButton(back_btn_icon, "")
        self.back_btn.setFixedWidth(font.BOLD_FONT_METRICS.height() + 8)

        name_lbl = qtw.QLabel("Name")
        name_lbl.setFont(font.BOLD_FONT)
        # name_lbl.setFixedWidth(font.BOLD_FONT_METRICS.width("  Name  "))
        self._name_txt = qtw.QLineEdit()
        self._name_txt.setMaximumWidth(800)

        save_btn_icon = icons.save_btn_icon(parent=self)
        self.save_btn = qtw.QPushButton(save_btn_icon, "")
        self.save_btn.setFixedWidth(font.BOLD_FONT_METRICS.height() + 8)

        note_lbl = qtw.QLabel("Note")
        note_lbl.setFont(font.BOLD_FONT)
        self._note_txt = qtw.QTextEdit()
        self._note_txt.setMaximumWidth(800)
        self._note_txt.setMaximumHeight(font.DEFAULT_FONT_METRICS.height() * 8 + 12)

        layout = qtw.QGridLayout()
        layout.addWidget(self.back_btn, 0, 0, alignment=qtc.Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(name_lbl, 1, 0)
        layout.addWidget(self._name_txt, 1, 1)
        layout.addWidget(note_lbl, 2, 0)
        layout.addWidget(self._note_txt, 2, 1)
        layout.addWidget(self.save_btn, 3, 1, alignment=qtc.Qt.AlignmentFlag.AlignRight)
        layout.addItem(qtw.QSpacerItem(0, 0, qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Expanding), 4, 2)
        self.setLayout(layout)

        self._category_id: str = ""
        self._date_added: datetime.datetime = datetime.datetime.now()
        self._date_updated: datetime.datetime | None = None

        # noinspection PyUnresolvedReferences
        self.back_btn.clicked.connect(self._on_back_btn_clicked)
        # noinspection PyUnresolvedReferences
        self.save_btn.clicked.connect(self._on_save_btn_clicked)

    def get_state(self) -> CategoryFormState | domain.Error:
        try:
            return CategoryFormState(
                category_id=self._category_id,
                name=self._name_txt.text(),
                note=self._note_txt.toPlainText(),
                date_added=self._date_added,
                date_updated=self._date_updated,
            )
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.get_state() failed: {e!s}")

            return domain.Error.new(str(e))

    def save(self) -> None | domain.Error:
        try:
            state = self.get_state()
            if isinstance(state, domain.Error):
                return state

            category = state.to_domain()

            self._form_requests.save.emit(requests.Save(category=category))

            return None
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.save() failed: {e!s}")

            return domain.Error.new(str(e))

    def set_state(self, /, state: CategoryFormState) -> None | domain.Error:
        try:
            self._category_id = state.category_id
            self._name_txt.setText(state.name)
            self._note_txt.setText(state.note)
            self._date_added = state.date_added
            self._date_updated = state.date_updated

            return None
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.set_state({state=!r}) failed: {e!s}")

            return domain.Error.new(str(e), state=state)

    def _on_back_btn_clicked(self, /, _: bool) -> None:
        logger.debug(f"{self.__class__.__name__}._on_back_btn_clicked()")

        self._form_requests.back.emit()

    def _on_save_btn_clicked(self, /, _: bool) -> None:
        logger.debug(f"{self.__class__.__name__}._on_save_btn_clicked()")

        category = domain.Category(
            category_id=self._category_id,
            name=self._name_txt.text(),
            note=self._note_txt.toPlainText(),
            date_added=self._date_added,
            date_updated=self._date_updated,
            date_deleted=None,
        )

        request = requests.Save(category=category)

        self._form_requests.save.emit(request)
