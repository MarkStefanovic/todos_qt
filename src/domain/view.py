import typing

__all__ = ("View",)

State = typing.TypeVar("State")


class View(typing.Protocol[State]):
    def get_state(self) -> State:
        raise NotImplementedError

    def set_state(self, /, state: State) -> None:
        raise NotImplementedError
