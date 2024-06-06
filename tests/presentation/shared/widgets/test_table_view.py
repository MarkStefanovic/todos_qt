import dataclasses
import datetime
import random

import hypothesis
from hypothesis import strategies
from pytestqt.qtbot import QtBot

from src.presentation.shared import theme
from src.presentation.shared.widgets import table_view


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class Row:
    date_col: datetime.date
    datetime_col: datetime.datetime
    int_col: int
    text_col: str


@hypothesis.settings(
    deadline=None,
    suppress_health_check=[hypothesis.HealthCheck.function_scoped_fixture],
)
@hypothesis.given(
    rows=strategies.lists(
        strategies.builds(
            Row,
            date_col=strategies.dates(),
            datetime_col=strategies.datetimes(),
            int_col=strategies.integers(),
            text_col=strategies.text(),
        ),
        min_size=0,
        max_size=200,
    )
)
def test_view(rows: list[Row], qtbot: QtBot) -> None:
    rows = list({row.int_col: row for row in rows}.values())

    view: table_view.TableView[Row, int] = table_view.TableView(
        attrs=(
            table_view.date(
                name="date_col",
                display_name="Date",
            ),
            table_view.timestamp(
                name="datetime_col",
                display_name="Time",
            ),
            table_view.integer(
                name="int_col",
                display_name="Integer",
            ),
            table_view.text(
                name="text_col",
                display_name="Text",
            ),
        ),
        key_attr_name="int_col",
        normal_font=theme.font.DEFAULT_FONT,
        bold_font=theme.font.BOLD_FONT,
        parent=None,
        date_format="%m/%d/%Y",
        datetime_format="%m/%d/%Y %I:%M %p",
    )

    qtbot.addWidget(view)

    view.set_items(rows)

    assert view.items == rows

    model = view.model()
    assert model is not None

    assert model.rowCount() == len(rows)

    assert model.columnCount() == len(view._attrs)

    if rows:
        random_row_to_delete = random.choice(rows)

        view.delete_item(key=random_row_to_delete.int_col)

        assert not any(row for row in view.items if row.int_col == random_row_to_delete.int_col)

        assert model.rowCount() == len(rows) - 1

        if view.items:
            random_row_to_update = random.choice(view.items)

            view.update_item(
                dataclasses.replace(
                    random_row_to_update,
                    date_col=random_row_to_update.date_col + datetime.timedelta(days=1),
                )
            )

            updated_item = view.get_item(key=random_row_to_update.int_col)

            assert updated_item is not None

            assert updated_item.date_col == random_row_to_update.date_col + datetime.timedelta(days=1)
