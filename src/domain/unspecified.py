import dataclasses

__all__ = ("Unspecified",)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


@dataclasses.dataclass(frozen=True)
class Unspecified(metaclass=Singleton):
    ...

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Unspecified):
            return True
        return False

    def __repr__(self) -> str:
        return "<Unspecified>"


if __name__ == "__main__":
    x: str | Unspecified = "test"

    print(x is Unspecified)

    print(x)

    y: str | Unspecified = Unspecified()

    print(y == Unspecified())

    print(y)

    print("z")

    z: str | Unspecified = Unspecified()

    print(y is z)
