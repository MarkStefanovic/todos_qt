import logging
import typing

import pytest
import sqlmodel as sm

from src import adapter

logger = logging.getLogger("test")


@pytest.fixture(scope="function")
def session() -> typing.Generator[sm.Session, None, None]:
    engine = adapter.db.get_engine(url="sqlite://", echo=True)
    session = sm.Session(engine)
    yield session
    session.close()
    #
    # sm.SQLModel.metadata.create_all
    # fp = pathlib.Path("testdb.sqlite")
    # fp.unlink(missing_ok=True)
    # yield fp
    # fp.unlink(missing_ok=True)
