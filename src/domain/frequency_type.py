import enum

__all__ = ("FrequencyType",)


class FrequencyType(enum.Enum):
    Daily = "Daily"
    Easter = "Easter"
    Irregular = "Irregular"
    Monthly = "Monthly"
    Once = "Once"
    Weekly = "Weekly"
    XDays = "XDays"
    Yearly = "Yearly"
