from __future__ import annotations

import dataclasses
import typing

import pydantic

from src.domain import exceptions

__all__ = (
    "Row",
    "Rows",
)

Row = typing.Tuple[typing.Any, ...]


class Rows:
    def __init__(
        self,
        *,
        column_names: typing.Iterable[str],
        rows: typing.Iterable[Row],
    ):
        self._column_names = list(column_names)
        self._rows = list(rows)

    @property
    def column_names(self) -> typing.List[str]:
        return self._column_names

    @property
    def first_value(self) -> typing.Optional[typing.Any]:
        if self._rows and self._rows[0]:
            return self._rows[0][0]
        return None

    @classmethod
    def from_dicts(
        cls, /, rows: typing.List[typing.Dict[str, typing.Hashable]]
    ) -> Rows:
        column_names = sorted(rows[0].keys())
        new_rows = [tuple(v for _, v in sorted(row.items())) for row in rows]
        return Rows(column_names=column_names, rows=new_rows)

    def as_dicts(self) -> typing.List[typing.Dict[str, typing.Hashable]]:
        return [dict(sorted(zip(self._column_names, row))) for row in self._rows]

    def as_tuples(self) -> typing.List[Row]:
        return self._rows

    def as_dtos(
        self, /, domain_type: typing.Type[typing.Any]
    ) -> typing.List[typing.Any]:
        if hasattr(domain_type, "__dataclass_fields__"):
            fields: typing.Dict[str, dataclasses.Field] = domain_type.__dataclass_fields__  # type: ignore
            field_names = {fld_name for fld_name in fields.keys()}
        elif issubclass(domain_type, pydantic.BaseModel):
            field_names = set(domain_type.__fields__.keys())
        else:
            raise exceptions.InvalidDtoType(cls=self.__class__)

        extra_fields = set(self._column_names) - field_names
        if extra_fields:
            row_dicts: typing.Iterable[typing.Dict[str, typing.Hashable]] = (
                {k: v for k, v in row.items() if k in field_names}
                for row in self.as_dicts()
            )
        else:
            row_dicts = self.as_dicts()
        return [domain_type(**d) for d in row_dicts]

    def __eq__(self, other: typing.Any) -> bool:
        if other.__class__ is self.__class__:
            other = typing.cast(Rows, other)
            return self._rows == other._rows
        else:
            return NotImplemented

    def __hash__(self) -> int:
        return hash(tuple(row) for row in self._rows)

    def __repr__(self) -> str:
        return f"<Rows: {len(self._rows)} items>"

    def __str__(self) -> str:
        return str(self._rows)
