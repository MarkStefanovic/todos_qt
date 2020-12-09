from __future__ import annotations

import datetime
import enum


class Weekday(enum.IntEnum):
    Sunday = 1
    Monday = 2
    Tuesday = 3
    Wednesday = 4
    Thursday = 5
    Friday = 6
    Saturday = 7

    @property
    def display_name(self) -> str:
        return {
            Weekday.Monday: "Monday",
            Weekday.Tuesday: "Tuesday",
            Weekday.Wednesday: "Wednesday",
            Weekday.Thursday: "Thursday",
            Weekday.Friday: "Friday",
            Weekday.Saturday: "Saturday",
            Weekday.Sunday: "Sunday",
        }[self]

    @staticmethod
    def from_date(dt: datetime.date) -> Weekday:
        return {
            0: Weekday.Monday,
            1: Weekday.Tuesday,
            2: Weekday.Wednesday,
            3: Weekday.Thursday,
            4: Weekday.Friday,
            5: Weekday.Saturday,
            6: Weekday.Sunday,
        }[dt.weekday()]

    @property
    def py_weekday(self) -> int:
        return {
            Weekday.Monday: 0,
            Weekday.Tuesday: 1,
            Weekday.Wednesday: 2,
            Weekday.Thursday: 3,
            Weekday.Friday: 4,
            Weekday.Saturday: 5,
            Weekday.Sunday: 6,
        }[self]

    @property
    def short_name(self) -> str:
        return {
            Weekday.Monday: "Mon",
            Weekday.Tuesday: "Tue",
            Weekday.Wednesday: "Wed",
            Weekday.Thursday: "Thu",
            Weekday.Friday: "Fri",
            Weekday.Saturday: "Sat",
            Weekday.Sunday: "Sun",
        }[self]

    def __str__(self) -> str:
        return self.display_name
