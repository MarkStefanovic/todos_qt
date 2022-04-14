import enum

__all__ = ("FrequencyType",)


class FrequencyType(enum.Enum):
    Daily = enum.auto()
    Easter = enum.auto()
    MemorialDay = enum.auto()
    Irregular = enum.auto()
    Monthly = enum.auto()
    Once = enum.auto()
    Weekly = enum.auto()
    XDays = enum.auto()
    Yearly = enum.auto()
