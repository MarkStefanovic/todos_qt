import enum

__all__ = ("FrequencyType",)


class FrequencyType(str, enum.Enum):
    Daily = "Daily"
    Easter = "Easter"
    Irregular = "Irregular"
    Monthly = "Monthly"
    Once = "Once"
    Weekly = "Weekly"
    XDays = "XDays"
    Yearly = "Yearly"

    def __str__(self) -> str:
        return str.__str__(self)
