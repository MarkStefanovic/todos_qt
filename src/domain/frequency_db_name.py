import enum
import typing


class FrequencyDbName(str, enum.Enum):
    # value: typing.Union[
    #     typing.Literal["daily"],
    #     typing.Literal["easter"],
    #     typing.Literal["irregular"],
    #     typing.Literal["monthly"],
    #     typing.Literal["once"],
    #     typing.Literal["weekly"],
    #     typing.Literal["xdays"],
    #     typing.Literal["yearly"],
    # ]

    DAILY = "daily"
    EASTER = "easter"
    IRREGULAR = "irregular"
    MONTHLY = "monthly"
    ONCE = "once"
    WEEKLY = "weekly"
    XDAYS = "xdays"
    YEARLY = "yearly"

    def __str__(self) -> str:
        return str.__str__(self)
