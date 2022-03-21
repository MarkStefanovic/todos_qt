import traceback
import typing

from PyQt5 import QtCore as qtc

__all__ = ("Worker",)

State = typing.TypeVar("State")


class StatusSignals(qtc.QObject):
    error = qtc.pyqtSignal(tuple)
    running = qtc.pyqtSignal()
    success = qtc.pyqtSignal(object)


class Worker(typing.Generic[State], qtc.QObject):
    def __init__(
        self,
        *,
        thread_pool: qtc.QThreadPool,
        transformer: typing.Callable[[State], State],
        on_error: typing.Callable[[Exception], None] | None = None,
        on_start: typing.Callable[[], None] | None = None,
        on_success: typing.Callable[[State], None] | None = None,
    ):
        super().__init__()

        self._thread_pool = thread_pool
        self._transformer = transformer
        self._status_signals = StatusSignals()

        if on_error is not None:
            # noinspection PyUnresolvedReferences
            self._status_signals.error.connect(on_error)

        if on_start is not None:
            # noinspection PyUnresolvedReferences
            self._status_signals.running.connect(on_start)

        if on_success is not None:
            # noinspection PyUnresolvedReferences
            self._status_signals.success.connect(on_success)

    def start(self, *, state: State) -> None:
        job = Job(state=state, transformer=self._transformer, status_signals=self._status_signals)
        self._thread_pool.start(job)


class Job(qtc.QRunnable):
    def __init__(
        self,
        *,
        state: State,
        transformer: typing.Callable[[State], State],
        status_signals: StatusSignals,
    ):
        super().__init__()

        self.setAutoDelete(False)

        self._state = state
        self._transformer = transformer
        self._status_signals = status_signals

    def run(self) -> None:
        try:
            # noinspection PyUnresolvedReferences
            self._status_signals.running.emit()
            state = self._transformer(self._state)
            # noinspection PyUnresolvedReferences
            self._status_signals.success.emit(state)
        except Exception as e:
            # noinspection PyUnresolvedReferences
            self._status_signals.error.emit((e, traceback.format_exc()))
