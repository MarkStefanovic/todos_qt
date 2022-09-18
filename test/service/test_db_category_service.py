import dataclasses
import datetime

import sqlalchemy as sa

from src import domain, service

# noinspection DuplicatedCode
CATEGORY_1 = domain.Category(
    category_id="1" * 32,
    name="Category 1",
    note="Test Note 1",
    date_added=datetime.datetime(2010, 1, 2, 3, 4, 5, 6),
    date_updated=None,
    date_deleted=None,
)

CATEGORY_2 = domain.Category(
    category_id="2" * 32,
    name="Category 2",
    note="Test Note 2",
    date_added=datetime.datetime(2011, 2, 3, 4, 5, 6, 7),
    date_updated=None,
    date_deleted=None,
)

CATEGORY_3 = domain.Category(
    category_id="3" * 32,
    name="Category 3",
    note="Test Note 3",
    date_added=datetime.datetime(2011, 2, 3, 4, 5, 7, 8),
    date_updated=datetime.datetime(2011, 2, 3, 4, 6, 7, 8),
    date_deleted=None,
)


def test_round_trip(engine: sa.engine.Engine):
    category_service = service.CategoryService(engine=engine)

    category_service.add(category=CATEGORY_1)
    category_service.add(category=CATEGORY_2)
    category_service.add(category=CATEGORY_3)

    assert len(category_service.all()) == 3

    updated_category = dataclasses.replace(
        CATEGORY_1,
        note="Updated note 1."
    )

    category_service.update(category=updated_category)

    assert category_service.get(category_id=CATEGORY_1.category_id).note == "Updated note 1."

    assert len(category_service.all()) == 3

    category_service.delete(category_id=CATEGORY_3.category_id)

    assert len(category_service.all()) == 2

