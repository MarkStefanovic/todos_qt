from __future__ import annotations


__all__ = ("Unspecified",)


class Unspecified:
    _instance: Unspecified | None = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Unspecified, cls).__new__(cls)
        return cls._instance

    def __eq__(self, __value):
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
