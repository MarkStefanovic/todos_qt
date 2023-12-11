from __future__ import annotations

import dataclasses
import typing

__all__ = ("Option",)

T = typing.TypeVar("T")


@dataclasses.dataclass(frozen=True, kw_only=True)
class Option(typing.Generic[T]):
    _value: T | None
    _is_none: bool

    def is_none(self) -> bool:
        return self._is_none

    def is_some(self) -> bool:
        return not self._is_none

    @staticmethod
    def none() -> Option[T]:
        return Option(_value=None, _is_none=True)

    @staticmethod
    def some(value: T, /) -> Option[T]:
        return Option(_value=value, _is_none=False)

    def value(self) -> T:
        if self._is_none:
            raise Exception(
                "Attempted to call value() on an Option that is None, did you forget to check is_some() first?"
            )

        return typing.cast(T, self._value)

    def __repr__(self) -> str:
        if self._is_none:
            return "Option::None"

        return f"Some [ value: {self._value!r} ]"


if __name__ == "__main__":
    o1 = Option.some("test")
    print(o1)
    print(repr(o1))
    print(o1.value())

    o2: Option[str | None] = Option.none()
    print(o2)
    print(repr(o2))
    if o2.is_some():
        print(o2.value())

    print(o2.value())
