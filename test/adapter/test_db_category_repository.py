import dataclasses
import datetime

from src import adapter, domain

import sqlalchemy as sa


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
    date_deleted=datetime.datetime(2011, 2, 4, 5, 6, 7, 8),
)

CATEGORY_3 = domain.Category(
    category_id="3" * 32,
    name="Category 3",
    note="Test Note 3",
    date_added=datetime.datetime(2011, 2, 3, 4, 5, 7, 8),
    date_updated=datetime.datetime(2011, 2, 3, 4, 6, 7, 8),
    date_deleted=None,
)


def test_round_trip(schema: str | None, engine: sa.Engine) -> None:
    with engine.begin() as con:  # type: sa.Connection
        assert adapter.category_repo.add(schema=schema, con=con, category=CATEGORY_1) is None
        assert adapter.category_repo.add(schema=schema, con=con, category=CATEGORY_2) is None
        assert adapter.category_repo.add(schema=schema, con=con, category=CATEGORY_3) is None

        categories = adapter.category_repo.where(schema=schema, con=con, active=True)
        assert not isinstance(categories, domain.Error)

        assert len(categories) == 2  # 1 has already been deleted

        updated_category = dataclasses.replace(CATEGORY_1, note="Updated note 1.")

        adapter.category_repo.update(schema=schema, con=con, category=updated_category)

        category = adapter.category_repo.get(schema=schema, con=con, category_id=CATEGORY_1.category_id)
        assert isinstance(category, domain.Category)

        assert category.note == "Updated note 1."

        categories = adapter.category_repo.where(schema=schema, con=con, active=True)
        assert isinstance(categories, list)

        assert len(categories) == 2

        assert adapter.category_repo.delete(schema=schema, con=con, category_id=CATEGORY_3.category_id)

        categories = adapter.category_repo.where(schema=schema, con=con, active=True)
        assert isinstance(categories, list)
        assert len(categories) == 1
