import dataclasses
import datetime

from src import adapter, domain

import sqlmodel as sm

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


def test_round_trip(session: sm.Session):
    repo = adapter.DbCategoryRepository(session=session)

    repo.add(category=CATEGORY_1)
    repo.add(category=CATEGORY_2)
    repo.add(category=CATEGORY_3)

    session.commit()

    assert len(repo.get_active()) == 2  # 1 is deleted

    updated_category = dataclasses.replace(
        CATEGORY_1,
        note="Updated note 1."
    )

    repo.update(category=updated_category)

    session.commit()

    assert repo.get(category_id=CATEGORY_1.category_id).note == "Updated note 1."

    assert len(repo.get_active()) == 2

    print(f"{repo.get_active()=}")

    repo.delete(category_id=CATEGORY_3.category_id)

    session.commit()

    assert len(repo.get_active()) == 1

