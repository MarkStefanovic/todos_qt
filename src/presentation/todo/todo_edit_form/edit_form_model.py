import datetime
import typing

import pydantic
from PyQt5 import QtCore as qtc

from src import service, domain
from src.domain import exceptions

__all__ = ("TodoEditFormModel",)


class TodoEditFormModel(qtc.QObject):
    validation_error_occurred = qtc.pyqtSignal(str)
    exception_occurred = qtc.pyqtSignal(str)

    def __init__(
        self,
        *,
        edit_mode: domain.EditMode,
        todo_service: service.TodoService,
        todo_id: typing.Optional[int] = None,
    ):
        if not isinstance(edit_mode, domain.EditMode):
            raise exceptions.DeveloperError(
                f"mode should be an instance of domain.EditMode, but got {edit_mode!r}."
            )

        if edit_mode == edit_mode.ADD and todo_id is not None:
            raise exceptions.DeveloperError(
                "If the mode is 'add', then then todo_id should be None."
            )
        elif edit_mode == edit_mode.EDIT and todo_id is None:
            raise exceptions.DeveloperError(
                "A todo_id should be passed in to TodoEditFormModel when mode = 'edit'."
            )

        super().__init__()

        self._edit_mode = edit_mode
        self._service = todo_service

        if edit_mode == domain.EditMode.EDIT:
            assert todo_id is not None
            self._initial_state = todo_service.get_id(todo_id).to_dto()
        else:
            self._initial_state = domain.TodoDTO.default()

        self._advance_days = self._initial_state.advance_days
        self._category = self._initial_state.category.value
        self._date_added = self._initial_state.date_added
        self._date_completed = self._initial_state.date_completed
        self._days = self._initial_state.days
        self._description = self._initial_state.description
        self._frequency = self._initial_state.frequency.value
        self._month = self._initial_state.month
        self._month_day = self._initial_state.month_day
        self._note = self._initial_state.note
        self._start_date = self._initial_state.start_date
        self._week_day = self._initial_state.week_day
        self._week_number = self._initial_state.week_number
        self._year = self._initial_state.year

    @property
    def advance_days(self) -> int:
        return self._advance_days

    @property
    def category(self) -> str:
        return self._category

    @property
    def category_options(self) -> typing.List[str]:
        return ["reminder", "todo"]

    @property
    def date_added(self) -> typing.Optional[datetime.date]:
        return self._date_added

    @property
    def date_completed(self) -> typing.Optional[datetime.date]:
        return self._date_completed

    @property
    def days(self) -> typing.Optional[int]:
        return self._days

    @property
    def description(self) -> str:
        return self._description

    @property
    def edit_mode(self) -> domain.EditMode:
        return self._edit_mode

    @property
    def frequency(self) -> str:
        return self._frequency

    @property
    def frequency_options(self) -> typing.List[str]:
        return [
            "daily",
            # "easter",
            "irregular",
            "monthly",
            "once",
            "weekly",
            "xdays",
            "yearly",
        ]

    @property
    def month(self) -> typing.Optional[int]:
        return self._month

    @property
    def month_day(self) -> typing.Optional[int]:
        return self._month_day

    @property
    def note(self) -> str:
        return self._note

    # def reset(self) -> None:
    #     self._advance_days = self._initial_state.advance_days
    #     self._category = self._initial_state.category.value
    #     self._date_added = self._initial_state.date_added
    #     self._date_completed = self._date_completed
    #     self._days = self._initial_state.days
    #     self._description = self._initial_state.description
    #     self._frequency = self._initial_state.frequency.value
    #     self._month = self._initial_state.month
    #     self._month_day = self._initial_state.month_day
    #     self._note = self._initial_state.note
    #     self._start_date = self._initial_state.start_date
    #     self._week_day = self._initial_state.week_day
    #     self._week_number = self._initial_state.week_number
    #     self._year = self._initial_state.year

    def save(self) -> None:
        try:
            dto = domain.TodoDTO(
                id=self._initial_state.id,
                advance_days=self.advance_days,
                date_added=self.date_added,
                date_completed=self.date_completed,
                days=self.days,
                description=self.description,
                month=self.month,
                month_day=self.month_day,
                note=self.note,
                start_date=self.start_date,
                category=domain.TodoCategory(self.category),
                week_day=self.week_day,
                week_number=self.week_number,
                year=self.year,
                frequency=domain.FrequencyDbName(self.frequency),
            )
        except pydantic.ValidationError as e:
            self.validation_error_occurred.emit(str(e))
        except Exception as e:
            self.exception_occurred.emit(str(e))
        else:
            try:
                todo = dto.to_domain()
                if self._edit_mode == domain.EditMode.ADD:
                    print(f"Adding {todo}...")
                    self._service.add_todo(todo)
                else:
                    print(f"Updating {todo}...")
                    self._service.update_todo(todo)
            except Exception as e:
                self.exception_occurred.emit(str(e))

    def set_advance_days(self, /, advance_days: int) -> None:
        self._advance_days = advance_days

    def set_category(self, /, category: str) -> None:
        self._category = category

    def set_date_added(self, /, date_added: datetime.date) -> None:
        self._date_added = date_added

    def set_date_completed(self, /, date_completed: datetime.date) -> None:
        self._date_completed = date_completed

    def set_days(self, days: int) -> None:
        self._days = days

    def set_description(self, description: str) -> None:
        self._description = description

    def set_frequency(self, frequency: str) -> None:
        self._frequency = frequency

    def set_month(self, month: int) -> None:
        self._month = month

    def set_month_day(self, month_day: int) -> None:
        self._month_day = month_day

    def set_note(self, note: str) -> None:
        self._note = note

    @property
    def start_date(self) -> typing.Optional[datetime.date]:
        return self._start_date

    def set_start_date(self, start_date: datetime.date) -> None:
        self._start_date = start_date

    def set_week_day(self, week_day: int) -> None:
        self._week_day = week_day

    def set_week_number(self, week_number: int) -> None:
        self._week_number = week_number

    def set_year(self, year: int) -> None:
        self._year = year

    @property
    def week_day(self) -> typing.Optional[int]:
        return self._week_day

    @property
    def week_number(self) -> typing.Optional[int]:
        return self._week_number

    @property
    def year(self) -> typing.Optional[int]:
        return self._year
