import enum


class EditMode(str, enum.Enum):
    ADD = "add"
    EDIT = "edit"

    def __str__(self) -> str:
        return str.__str__(self)
