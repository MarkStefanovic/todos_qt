import datetime
import typing

from PyQt6 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw  # noqa
from loguru import logger

from src import domain
from src.presentation.category_selector import CategorySelectorWidget
from src.presentation.shared import widgets
from src.presentation.shared.theme import font, icons
from src.presentation.shared.widgets import DateEditor
from src.presentation.todo.view.form import requests
from src.presentation.todo.view.form.irregular.state import IrregularFrequencyFormState
from src.presentation.todo.view.form.irregular.view import IrregularFrequencyForm
from src.presentation.todo.view.form.monthly.state import MonthlyFrequencyFormState
from src.presentation.todo.view.form.monthly.view import MonthlyFrequencyForm
from src.presentation.todo.view.form.once.state import OnceFrequencyFormState
from src.presentation.todo.view.form.once.view import OnceFrequencyForm
from src.presentation.todo.view.form.state import TodoFormState
from src.presentation.todo.view.form.weekly.state import WeeklyFrequencyFormState
from src.presentation.todo.view.form.weekly.view import WeeklyFrequencyForm
from src.presentation.todo.view.form.xdays.state import XDaysFrequencyFormState
from src.presentation.todo.view.form.xdays.view import XDaysFrequencyForm
from src.presentation.todo.view.form.yearly.state import YearlyFrequencyFormState
from src.presentation.todo.view.form.yearly.view import YearlyFrequencyForm
from src.presentation.user_selector.widget import UserSelectorWidget

__all__ = ("TodoFormView",)


# noinspection DuplicatedCode
class TodoFormView(qtw.QWidget):
    def __init__(
        self,
        *,
        form_requests: requests.TodoFormRequests,
        category_selector: CategorySelectorWidget,
        user_selector: UserSelectorWidget,
        parent: qtw.QWidget | None = None,
    ):
        super().__init__(parent=parent)

        label_width = font.BOLD_FONT_METRICS.boundingRect("    Advance Days    ").width()

        self._requests: typing.Final[requests.TodoFormRequests] = form_requests
        self._category_selector: typing.Final[CategorySelectorWidget] = category_selector
        self._user_selector: typing.Final[UserSelectorWidget] = user_selector

        description_lbl = qtw.QLabel("Description")
        description_lbl.setFont(font.BOLD_FONT)
        description_lbl.setFixedWidth(label_width)
        self._description_txt = qtw.QLineEdit()
        self._description_txt.setMaximumWidth(800)

        advance_days_lbl = qtw.QLabel("Advance Days")
        advance_days_lbl.setFont(font.BOLD_FONT)
        advance_days_lbl.setFixedWidth(label_width)
        self._advance_days_sb = qtw.QSpinBox()
        self._advance_days_sb.setMinimum(0)
        self._advance_days_sb.setFixedWidth(font.DEFAULT_FONT_METRICS.boundingRect("   9999   ").width())

        expire_days_lbl = qtw.QLabel("Expire Days")
        expire_days_lbl.setFont(font.BOLD_FONT)
        expire_days_lbl.setFixedWidth(label_width)
        self._expire_days_sb = qtw.QSpinBox()
        self._expire_days_sb.setMinimum(1)
        self._expire_days_sb.setFixedWidth(font.DEFAULT_FONT_METRICS.boundingRect("   9999   ").width())

        user_lbl = qtw.QLabel("User")
        user_lbl.setFont(font.BOLD_FONT)
        user_lbl.setFixedWidth(label_width)

        category_lbl = qtw.QLabel("Category")
        category_lbl.setFont(font.BOLD_FONT)
        category_lbl.setFixedWidth(label_width)

        note_lbl = qtw.QLabel("Note")
        note_lbl.setFont(font.BOLD_FONT)
        note_lbl.setFixedWidth(label_width)
        self._note_txt = qtw.QTextEdit(parent=self)
        self._note_txt.setMaximumWidth(800)

        start_date_lbl = qtw.QLabel("Start")
        start_date_lbl.setFont(font.BOLD_FONT)
        start_date_lbl.setFixedWidth(label_width)
        self._start_date_edit = DateEditor()

        frequency_lbl = qtw.QLabel("Frequency")
        frequency_lbl.setFont(font.BOLD_FONT)
        frequency_lbl.setFixedWidth(label_width)
        self._frequency_cbo: typing.Final[widgets.MapCBO[domain.FrequencyType]] = widgets.MapCBO()
        self._frequency_cbo.set_values(
            {
                domain.FrequencyType.Daily: "Daily",
                domain.FrequencyType.Easter: "Easter",
                domain.FrequencyType.Irregular: "Irregular",
                domain.FrequencyType.MemorialDay: "Memorial Day",
                domain.FrequencyType.Monthly: "Monthly",
                domain.FrequencyType.Once: "Once",
                domain.FrequencyType.Weekly: "Weekly",
                domain.FrequencyType.XDays: "XDays",
                domain.FrequencyType.Yearly: "Yearly",
            }
        )
        self._frequency_cbo.set_value(domain.FrequencyType.Daily)
        self._frequency_cbo.value_changed.connect(self._frequency_changed)
        self._frequency_cbo.setFixedWidth(font.DEFAULT_FONT_METRICS.boundingRect("   Irregular   ").width())

        self._irregular_frequency_form = IrregularFrequencyForm(label_width=label_width, parent=self)
        self._monthly_frequency_form = MonthlyFrequencyForm(label_width=label_width, parent=self)
        self._one_off_frequency_form = OnceFrequencyForm(label_width=label_width, parent=self)
        self._weekly_frequency_form = WeeklyFrequencyForm(label_width=label_width, parent=self)
        self._xdays_frequency_form = XDaysFrequencyForm(label_width=label_width, parent=self)
        self._yearly_frequency_form = YearlyFrequencyForm(label_width=label_width, parent=self)

        empty_subform_dummy = qtw.QWidget()
        empty_subform_dummy.setVisible(False)
        empty_subform_dummy.setStyleSheet("border: none;")
        empty_subform_dummy.setFixedHeight(0)

        self._frequency_subform_layout = qtw.QStackedLayout()
        self._frequency_subform_layout.addWidget(empty_subform_dummy)
        self._frequency_subform_layout.addWidget(self._irregular_frequency_form)
        self._frequency_subform_layout.addWidget(self._monthly_frequency_form)
        self._frequency_subform_layout.addWidget(self._one_off_frequency_form)
        self._frequency_subform_layout.addWidget(self._weekly_frequency_form)
        self._frequency_subform_layout.addWidget(self._xdays_frequency_form)
        self._frequency_subform_layout.addWidget(self._yearly_frequency_form)

        back_btn_icon = icons.back_btn_icon(parent=self)
        self.back_btn = qtw.QPushButton(back_btn_icon, "")
        self.back_btn.setMinimumWidth(font.BOLD_FONT_METRICS.height() + 8)
        self.back_btn.setToolTip("Back to Dashboard")

        save_btn_icon = icons.save_btn_icon(parent=self)
        self.save_btn = qtw.QPushButton(save_btn_icon, "")
        self.save_btn.setMinimumWidth(font.BOLD_FONT_METRICS.height() + 8)
        self.save_btn.setToolTip("Save")
        self.save_btn.setIconSize(qtc.QSize(20, 20))
        self.save_btn.setFixedSize(30, 30)

        save_btn_layout = qtw.QHBoxLayout()
        save_btn_layout.addStretch()
        save_btn_layout.addWidget(self.save_btn)

        form_layout = qtw.QFormLayout()
        form_layout.addRow(self.back_btn, save_btn_layout)
        form_layout.addRow(description_lbl, self._description_txt)
        form_layout.addRow(start_date_lbl, self._start_date_edit)
        form_layout.addRow(advance_days_lbl, self._advance_days_sb)
        form_layout.addRow(expire_days_lbl, self._expire_days_sb)
        form_layout.addRow(user_lbl, self._user_selector)
        form_layout.addRow(category_lbl, self._category_selector)
        form_layout.addRow(note_lbl, self._note_txt)
        form_layout.addRow(frequency_lbl, self._frequency_cbo)

        form_layout_wrapper = qtw.QHBoxLayout()
        form_layout_wrapper.addLayout(form_layout)
        form_layout_wrapper.addStretch()

        main_layout = qtw.QGridLayout()
        main_layout.addLayout(form_layout_wrapper, 0, 0)
        main_layout.addLayout(self._frequency_subform_layout, 1, 0)
        main_layout.addItem(
            qtw.QSpacerItem(0, 0, qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Expanding), 2, 1
        )

        self.setLayout(main_layout)

        self._todo_id = ""
        self._template_todo_id: str | None = None
        self._date_added = datetime.datetime.now()
        self._date_updated: datetime.datetime | None = None
        self._last_completed: datetime.date | None = None
        self._prior_completed: datetime.date | None = None
        self._last_completed_by: domain.User | None = None
        self._prior_completed_by: domain.User | None = None

        # noinspection PyUnresolvedReferences
        self.back_btn.clicked.connect(self._on_back_btn_clicked)
        # noinspection PyUnresolvedReferences
        self.save_btn.clicked.connect(self._on_save_btn_clicked)

    def get_state(self) -> TodoFormState | domain.Error:
        try:
            frequency = self._frequency_cbo.get_value()
            if frequency is None:
                return domain.Error.new("No frequency was selected.")

            irregular_frequency_form_state: IrregularFrequencyFormState | domain.Unspecified | domain.Error = (
                domain.Unspecified()
            )
            monthly_frequency_form_state: MonthlyFrequencyFormState | domain.Unspecified | domain.Error = (
                domain.Unspecified()
            )
            once_frequency_form_state: OnceFrequencyFormState | domain.Unspecified | domain.Error = domain.Unspecified()
            weekly_frequency_form_state: WeeklyFrequencyFormState | domain.Unspecified | domain.Error = (
                domain.Unspecified()
            )
            xdays_frequency_form_state: XDaysFrequencyFormState | domain.Unspecified | domain.Error = (
                domain.Unspecified()
            )
            yearly_frequency_form_state: YearlyFrequencyFormState | domain.Unspecified | domain.Error = (
                domain.Unspecified()
            )

            match frequency:
                case domain.FrequencyType.Daily | domain.FrequencyType.Easter | domain.FrequencyType.MemorialDay:
                    pass
                case domain.FrequencyType.Irregular:
                    irregular_frequency_form_state = self._irregular_frequency_form.get_state()
                    if isinstance(irregular_frequency_form_state, domain.Error):
                        return irregular_frequency_form_state
                case domain.FrequencyType.Monthly:
                    monthly_frequency_form_state = self._monthly_frequency_form.get_state()
                    if isinstance(monthly_frequency_form_state, domain.Error):
                        return monthly_frequency_form_state
                case domain.FrequencyType.Once:
                    once_frequency_form_state = self._one_off_frequency_form.get_state()
                    if isinstance(once_frequency_form_state, domain.Error):
                        return once_frequency_form_state
                case domain.FrequencyType.Weekly:
                    weekly_frequency_form_state = self._weekly_frequency_form.get_state()
                    if isinstance(weekly_frequency_form_state, domain.Error):
                        return weekly_frequency_form_state
                case domain.FrequencyType.XDays:
                    xdays_frequency_form_state = self._xdays_frequency_form.get_state()
                    if isinstance(xdays_frequency_form_state, domain.Error):
                        return xdays_frequency_form_state
                case domain.FrequencyType.Yearly:
                    yearly_frequency_form_state = self._yearly_frequency_form.get_state()
                    if isinstance(yearly_frequency_form_state, domain.Error):
                        return yearly_frequency_form_state
                case _:
                    raise domain.Error.new(f"Unhandled FrequencyType, {frequency!r}.")

            if isinstance(irregular_frequency_form_state, domain.Error):
                return irregular_frequency_form_state

            if isinstance(monthly_frequency_form_state, domain.Error):
                return monthly_frequency_form_state

            if isinstance(once_frequency_form_state, domain.Error):
                return once_frequency_form_state

            if isinstance(weekly_frequency_form_state, domain.Error):
                return weekly_frequency_form_state

            if isinstance(xdays_frequency_form_state, domain.Error):
                return xdays_frequency_form_state

            if isinstance(yearly_frequency_form_state, domain.Error):
                return yearly_frequency_form_state

            return TodoFormState(
                todo_id=self._todo_id,
                template_todo_id=self._template_todo_id,
                user=self._user_selector.get_selected_item(),
                advance_days=self._advance_days_sb.value(),
                expire_days=self._expire_days_sb.value(),
                category=self._category_selector.selected_item(),
                description=self._description_txt.text(),
                frequency_name=frequency,
                note=self._note_txt.toPlainText(),
                # note=self._note_txt.get_value(),
                start_date=self._start_date_edit.get_value() or datetime.date(1900, 1, 1),
                date_added=self._date_added,
                date_updated=self._date_updated,
                last_completed=self._last_completed,
                prior_completed=self._prior_completed,
                last_completed_by=self._last_completed_by,
                prior_completed_by=self._prior_completed_by,
                irregular_frequency_form_state=irregular_frequency_form_state,
                monthly_frequency_form_state=monthly_frequency_form_state,
                once_frequency_form_state=once_frequency_form_state,
                weekly_frequency_form_state=weekly_frequency_form_state,
                xdays_frequency_form_state=xdays_frequency_form_state,
                yearly_frequency_form_state=yearly_frequency_form_state,
                focus_description=domain.Unspecified(),
            )
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.get_state() failed: {e!s}")
            return domain.Error.new(str(e))

    def set_state(self, /, state: TodoFormState) -> None | domain.Error:
        try:
            if not isinstance(state.todo_id, domain.Unspecified):
                self._todo_id = state.todo_id

            if not isinstance(state.template_todo_id, domain.Unspecified):
                self._template_todo_id = state.template_todo_id

            if not isinstance(state.date_added, domain.Unspecified):
                self._date_added = state.date_added

            if not isinstance(state.date_updated, domain.Unspecified):
                self._date_updated = state.date_updated

            if not isinstance(state.last_completed, domain.Unspecified):
                self._last_completed = state.last_completed

            if not isinstance(state.last_completed_by, domain.Unspecified):
                self._last_completed_by = state.last_completed_by

            if not isinstance(state.prior_completed, domain.Unspecified):
                self._prior_completed = state.prior_completed

            if not isinstance(state.prior_completed_by, domain.Unspecified):
                self._prior_completed_by = state.prior_completed_by

            if not isinstance(state.user, domain.Unspecified):
                self._user_selector.select_item(state.user)

            if not isinstance(state.description, domain.Unspecified):
                self._description_txt.setText(state.description)

            if not isinstance(state.advance_days, domain.Unspecified):
                self._advance_days_sb.setValue(state.advance_days)

            if not isinstance(state.expire_days, domain.Unspecified):
                self._expire_days_sb.setValue(state.expire_days)

            if not isinstance(state.frequency_name, domain.Unspecified):
                self._advance_days_sb.setMaximum(_get_maximum_advance_days_for_frequency(state.frequency_name))
                self._expire_days_sb.setMaximum(_get_maximum_expire_days_for_frequency(state.frequency_name))

                if state.frequency_name in (
                    domain.FrequencyType.Daily,
                    domain.FrequencyType.Easter,
                    domain.FrequencyType.MemorialDay,
                ):
                    self._frequency_subform_layout.setCurrentIndex(0)

                if state.frequency_name == domain.FrequencyType.Daily:
                    self._advance_days_sb.setEnabled(False)
                    self._expire_days_sb.setEnabled(False)
                else:
                    self._advance_days_sb.setEnabled(True)
                    self._expire_days_sb.setEnabled(True)

            if not isinstance(state.category, domain.Unspecified):
                self._category_selector.select_item(state.category)

            if not isinstance(state.note, domain.Unspecified):
                self._note_txt.setText(state.note)
                # self._note_txt.set_value(state.note)

            if not isinstance(state.start_date, domain.Unspecified):
                self._start_date_edit.set_value(state.start_date)

            if not isinstance(state.frequency_name, domain.Unspecified):
                self._frequency_cbo.set_value(state.frequency_name)

            if not isinstance(state.irregular_frequency_form_state, domain.Unspecified):
                self._irregular_frequency_form.set_state(state.irregular_frequency_form_state)

            if not isinstance(state.monthly_frequency_form_state, domain.Unspecified):
                self._monthly_frequency_form.set_state(state.monthly_frequency_form_state)

            if not isinstance(state.once_frequency_form_state, domain.Unspecified):
                self._one_off_frequency_form.set_state(state.once_frequency_form_state)

            if not isinstance(state.weekly_frequency_form_state, domain.Unspecified):
                self._weekly_frequency_form.set_state(state.weekly_frequency_form_state)

            if not isinstance(state.xdays_frequency_form_state, domain.Unspecified):
                self._xdays_frequency_form.set_state(state.xdays_frequency_form_state)

            if not isinstance(state.yearly_frequency_form_state, domain.Unspecified):
                self._yearly_frequency_form.set_state(state.yearly_frequency_form_state)

            if not isinstance(state.categories, domain.Unspecified):
                self._category_selector.set_items(state.categories)

            if not isinstance(state.users, domain.Unspecified):
                self._user_selector.set_items(state.users)

            if not isinstance(state.focus_description, domain.Unspecified):
                if state.focus_description:
                    self._description_txt.setFocus()
                else:
                    self._description_txt.clearFocus()

            return None
        except Exception as e:
            logger.error(f"{self.__class__.__name__}.set_state({state=!r}) failed: {e!s}")
            return domain.Error.new(str(e), state=state)

    def _frequency_changed(self) -> None:
        frequency = self._frequency_cbo.get_value()

        if frequency is None:
            return None

        self._advance_days_sb.setEnabled(frequency != domain.FrequencyType.Daily)
        self._expire_days_sb.setEnabled(frequency != domain.FrequencyType.Daily)
        self._advance_days_sb.setMaximum(_get_maximum_advance_days_for_frequency(frequency))
        self._expire_days_sb.setMaximum(_get_maximum_expire_days_for_frequency(frequency))

        match frequency:
            case domain.FrequencyType.Daily:
                self._advance_days_sb.setValue(0)
                self._expire_days_sb.setValue(1)
                self._frequency_subform_layout.setCurrentIndex(0)
            case domain.FrequencyType.Easter:
                self._advance_days_sb.setValue(30)
                self._expire_days_sb.setValue(90)
                self._frequency_subform_layout.setCurrentIndex(0)
            case domain.FrequencyType.Irregular:
                self._advance_days_sb.setValue(30)
                self._expire_days_sb.setValue(90)
                self._frequency_subform_layout.setCurrentIndex(1)
            case domain.FrequencyType.MemorialDay:
                self._advance_days_sb.setValue(30)
                self._expire_days_sb.setValue(90)
                self._frequency_subform_layout.setCurrentIndex(0)
            case domain.FrequencyType.Monthly:
                self._advance_days_sb.setValue(0)
                self._expire_days_sb.setValue(27)
                self._frequency_subform_layout.setCurrentIndex(2)
            case domain.FrequencyType.Once:
                self._advance_days_sb.setValue(0)
                self._expire_days_sb.setValue(99)
                self._frequency_subform_layout.setCurrentIndex(3)
            case domain.FrequencyType.Weekly:
                self._advance_days_sb.setValue(0)
                self._expire_days_sb.setValue(5)
                self._frequency_subform_layout.setCurrentIndex(4)
            case domain.FrequencyType.XDays:
                self._advance_days_sb.setValue(0)
                self._expire_days_sb.setValue(9)
                self._frequency_subform_layout.setCurrentIndex(5)
            case domain.FrequencyType.Yearly:
                self._advance_days_sb.setValue(30)
                self._expire_days_sb.setValue(90)
                self._frequency_subform_layout.setCurrentIndex(6)
            case _:
                self._requests.error.emit(domain.Error.new(f"Unrecognized frequency: {frequency!r}."))  # type: ignore

    def _on_back_btn_clicked(self, /, _: bool) -> None:
        logger.debug(f"{self.__class__.__name__}._on_back_btn_clicked()")

        self._requests.back.emit()

    def _on_save_btn_clicked(self, /, _: bool) -> None:
        logger.debug(f"{self.__class__.__name__}._on_save_btn_clicked()")

        todo_state = self.get_state()
        if isinstance(todo_state, domain.Error):
            self._requests.error.emit(todo_state)
            return None

        todo = todo_state.to_domain()
        if isinstance(todo, domain.Error):
            logger.error(f"{self.__class__.__name__}._on_save_btn_clicked() failed: {todo!s}")
            self._requests.error.emit(domain.Error.new(str(todo), todo=todo))
            return None

        self._requests.save.emit(requests.SaveRequest(todo=todo))


def _get_maximum_advance_days_for_frequency(frequency: domain.FrequencyType, /) -> int:
    match frequency:
        case domain.FrequencyType.Daily:
            return 0
        case domain.FrequencyType.Once | domain.FrequencyType.XDays:
            return 9999
        case domain.FrequencyType.Easter:
            return 363
        case domain.FrequencyType.MemorialDay:
            return 363
        case domain.FrequencyType.Irregular:
            return 363
        case domain.FrequencyType.Monthly:
            return 27
        case domain.FrequencyType.Weekly:
            return 6
        case domain.FrequencyType.Yearly:
            return 363


def _get_maximum_expire_days_for_frequency(frequency: domain.FrequencyType, /) -> int:
    match frequency:
        case domain.FrequencyType.Daily:
            return 1
        case domain.FrequencyType.Once | domain.FrequencyType.XDays:
            return 9999
        case domain.FrequencyType.Easter:
            return 363
        case domain.FrequencyType.MemorialDay:
            return 363
        case domain.FrequencyType.Irregular:
            return 363
        case domain.FrequencyType.Monthly:
            return 27
        case domain.FrequencyType.Weekly:
            return 6
        case domain.FrequencyType.Yearly:
            return 363
