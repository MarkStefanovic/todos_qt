from __future__ import annotations

import enum

__all__ = ("Month",)


class Month(enum.Enum):
    January = 1
    February = 2
    March = 3
    April = 4
    May = 5
    June = 6
    July = 7
    August = 8
    September = 9
    October = 10
    November = 11
    December = 12

    @staticmethod
    def from_int(month_num: int) -> Month:
        return {
            1: Month.January,
            2: Month.February,
            3: Month.March,
            4: Month.April,
            5: Month.May,
            6: Month.June,
            7: Month.July,
            8: Month.August,
            9: Month.September,
            10: Month.October,
            11: Month.November,
            12: Month.December,
        }[month_num]

    def to_int(self) -> int:
        return self.value

    def __str__(self) -> str:
        return {
            1: "Jan",
            2: "Feb",
            3: "Mar",
            4: "Apr",
            5: "May",
            6: "Jun",
            7: "Jul",
            8: "Aug",
            9: "Sep",
            10: "Oct",
            11: "Nov",
            12: "Dec",
        }[self.value]
